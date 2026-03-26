"""
BPMN generator component.

This component generates BPMN 2.0 XML from process analysis using
the bpmn-generation skill.
"""

from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET
from ...interfaces.component import BaseComponent, ComponentResult


class BPMNGenerator(BaseComponent):
    """
    Component for generating BPMN 2.0 XML from process analysis.

    Implements the bpmn-generation skill.
    """

    @property
    def component_name(self) -> str:
        """Return human-readable component name."""
        return "BPMN Generation"

    @property
    def skill_path(self) -> Path:
        """Return path to SKILL.md file for this component."""
        return Path(__file__).parent.parent.parent.parent / "skills" / "bpmn-generation" / "SKILL.md"

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate that input is a process analysis markdown.

        Args:
            input_data: Expected to be analysis markdown text

        Returns:
            True if valid

        Raises:
            ValueError: If input is invalid
        """
        if not isinstance(input_data, str):
            raise ValueError(f"Input must be string, got {type(input_data)}")
        if not input_data.strip():
            raise ValueError("Analysis text cannot be empty")

        # Check for required sections
        required_sections = ["## Process Steps", "## Actors and Roles", "## Decision Points"]
        missing_sections = [s for s in required_sections if s not in input_data]
        if missing_sections:
            if len(missing_sections) == 1:
                raise ValueError(f"Analysis missing required section: {missing_sections[0]}")
            else:
                raise ValueError(
                    f"Analysis missing {len(missing_sections)} required sections: "
                    f"{', '.join(missing_sections)}"
                )

        return True

    def _validate_bpmn_xml(self, bpmn_text: str) -> tuple[bool, str]:
        """
        Validate BPMN XML structure.

        Args:
            bpmn_text: BPMN XML text to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Parse XML
            root = ET.fromstring(bpmn_text)

            # Check namespace
            bpmn_ns = "http://www.omg.org/spec/BPMN/20100524/MODEL"
            if bpmn_ns not in root.tag:
                return False, f"Invalid BPMN namespace. Root tag: {root.tag}"

            # Check for process
            process = root.find(f".//{{{bpmn_ns}}}process")
            if process is None:
                return False, "No process element found"

            # Check for start and end events
            start_events = root.findall(f".//{{{bpmn_ns}}}startEvent")
            if not start_events:
                return False, "No start event found"

            end_events = root.findall(f".//{{{bpmn_ns}}}endEvent")
            if not end_events:
                return False, "No end event found"

            # Count elements for reporting
            tasks = root.findall(f".//{{{bpmn_ns}}}task")
            gateways = root.findall(f".//{{{bpmn_ns}}}exclusiveGateway")
            lanes = root.findall(f".//{{{bpmn_ns}}}lane")
            flows = root.findall(f".//{{{bpmn_ns}}}sequenceFlow")

            message = f"Valid BPMN XML - {len(tasks)} tasks, {len(gateways)} gateways, {len(lanes)} lanes, {len(flows)} flows"
            return True, message

        except ET.ParseError as e:
            return False, f"XML parsing error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def process(self, input_data: str, **kwargs) -> ComponentResult:
        """
        Generate BPMN 2.0 XML from process analysis.

        Args:
            input_data: Process analysis markdown
            **kwargs: Optional parameters:
                - include_apqc: Whether to include APQC activities reference (default True)

        Returns:
            ComponentResult with BPMN XML in data field
        """
        try:
            # Validate input
            self.validate_input(input_data)

            # Load skill prompt
            skill_prompt = self._load_skill_prompt()

            # Prepare system messages
            system_messages = [{"type": "text", "text": skill_prompt}]

            # Load APQC activities reference (cached)
            include_apqc = kwargs.get('include_apqc', True)
            if include_apqc:
                from ...skills.skill_manager import SkillManager
                manager = SkillManager()
                apqc_content = manager.load_domain_knowledge('bpmn-generation', 'apqc-activities.md')
                system_messages.append({
                    "type": "text",
                    "text": f"# APQC Level 4 Activities Reference\n\n{apqc_content}",
                    "cache_control": {"type": "ephemeral"}
                })

            # Prepare user message
            user_message = f"Generate BPMN 2.0 XML for the following process analysis:\n\n{input_data}"

            # Call Claude
            bpmn_text, api_metadata = self._call_claude(
                user_message=user_message,
                system_messages=system_messages,
                max_tokens=16000,
                temperature=0
            )

            # Extract XML from markdown code blocks if present
            if '```xml' in bpmn_text:
                bpmn_text = bpmn_text.split('```xml')[1].split('```')[0].strip()
            elif '```' in bpmn_text:
                bpmn_text = bpmn_text.split('```')[1].split('```')[0].strip()

            # Validate BPMN XML
            is_valid, validation_message = self._validate_bpmn_xml(bpmn_text)

            if not is_valid:
                return ComponentResult(
                    success=False,
                    data=bpmn_text,  # Return generated XML anyway for debugging
                    metadata={
                        **api_metadata,
                        "component": self.component_name,
                        "validation_error": validation_message
                    },
                    error=f"BPMN validation failed: {validation_message}"
                )

            # Return result
            return ComponentResult(
                success=True,
                data=bpmn_text,
                metadata={
                    **api_metadata,
                    "component": self.component_name,
                    "xml_length": len(bpmn_text),
                    "validation": validation_message
                }
            )

        except ValueError as e:
            return ComponentResult(
                success=False,
                data=None,
                metadata={"component": self.component_name},
                error=f"Validation error: {str(e)}"
            )
        except Exception as e:
            return ComponentResult(
                success=False,
                data=None,
                metadata={"component": self.component_name},
                error=f"Processing error: {str(e)}"
            )
