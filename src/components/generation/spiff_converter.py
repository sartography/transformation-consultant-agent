"""
SpiffWorkflow BPMN converter component.

Converts standard BPMN 2.0 XML into executable SpiffWorkflow diagrams
by adding extension elements, converting task types, writing Python
gateway conditions, and generating JSON schemas for user tasks.

After generation, the BPMN is validated using SpiffWorkflow's own parser
and BpmnValidator. If validation fails, the error is fed back to Claude
for a targeted fix, repeating up to MAX_FIX_ATTEMPTS times.
"""

from pathlib import Path
from typing import Any
import json
import logging
import xml.etree.ElementTree as ET
from ...interfaces.component import BaseComponent, ComponentResult

logger = logging.getLogger(__name__)

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
SPIFF_NS = "http://spiffworkflow.org/bpmn/schema/1.0/core"

OUTPUT_DELIMITER_BPMN = "===BPMN_XML==="
OUTPUT_DELIMITER_SCHEMAS = "===SCHEMA_FILES==="

MAX_FIX_ATTEMPTS = 3


def _spiff_validate(bpmn_xml: str) -> tuple[bool, str]:
    """
    Parse and validate BPMN XML using SpiffWorkflow's BpmnParser + BpmnValidator.

    The XML declaration line is stripped before passing to the parser because
    SpiffWorkflow's add_bpmn_str uses lxml, which rejects encoding declarations
    on Unicode strings.

    Returns:
        (is_valid, message) — message is the error string on failure, or a
        summary of task/gateway counts on success.
    """
    try:
        from SpiffWorkflow.bpmn.parser import BpmnParser, BpmnValidator
        from SpiffWorkflow.bpmn.parser.ValidationException import ValidationException
    except ImportError:
        return False, (
            "SpiffWorkflow is not installed. "
            "Run: pip install SpiffWorkflow"
        )

    # lxml rejects '<?xml ... encoding="UTF-8"?>' on a Unicode str
    clean = bpmn_xml
    if clean.lstrip().startswith("<?xml"):
        clean = clean[clean.index("?>") + 2:].lstrip()

    try:
        parser = BpmnParser(validator=BpmnValidator())
        parser.add_bpmn_str(clean)
        process_ids = parser.get_process_ids()
        return True, f"SpiffWorkflow validation passed — processes: {process_ids}"
    except ValidationException as e:
        return False, f"BPMN schema validation error: {e}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


class SpiffConverter(BaseComponent):
    """
    Component for converting standard BPMN 2.0 XML to SpiffWorkflow-executable format.

    Takes BPMN XML as input and returns converted BPMN XML plus any required
    JSON schema files for user task forms.

    Validation loop:
        1. Claude generates the SpiffWorkflow BPMN.
        2. SpiffWorkflow's BpmnParser + BpmnValidator parses it.
        3. If invalid, the error is sent back to Claude for a targeted fix.
        4. Steps 2-3 repeat up to MAX_FIX_ATTEMPTS times.
    """

    @property
    def component_name(self) -> str:
        return "SpiffWorkflow BPMN Converter"

    @property
    def skill_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "skills" / "spiff-conversion" / "SKILL.md"

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate that input is a BPMN 2.0 XML string.

        Raises:
            ValueError: If input is not valid BPMN XML
        """
        if not isinstance(input_data, str):
            raise ValueError(f"Input must be string, got {type(input_data)}")
        if not input_data.strip():
            raise ValueError("BPMN XML cannot be empty")

        try:
            root = ET.fromstring(input_data)
        except ET.ParseError as e:
            raise ValueError(f"Input is not valid XML: {e}")

        if BPMN_NS not in root.tag:
            raise ValueError(
                f"Input does not appear to be BPMN 2.0 XML (missing namespace {BPMN_NS})"
            )

        if root.find(f".//{{{BPMN_NS}}}process") is None:
            raise ValueError("No <bpmn:process> element found in input")

        return True

    def _parse_response(self, response_text: str) -> tuple[str, dict]:
        """
        Parse Claude's structured response into BPMN XML and schema files dict.

        Returns:
            (bpmn_xml, schema_files_dict)
        """
        bpmn_xml = ""
        schema_files = {}

        if OUTPUT_DELIMITER_BPMN not in response_text:
            # Fix-pass responses contain only BPMN XML (no schema section)
            bpmn_xml = response_text.strip()
            if '```xml' in bpmn_xml:
                bpmn_xml = bpmn_xml.split('```xml')[1].split('```')[0].strip()
            elif '```' in bpmn_xml:
                bpmn_xml = bpmn_xml.split('```')[1].split('```')[0].strip()
            return bpmn_xml, schema_files

        parts = response_text.split(OUTPUT_DELIMITER_BPMN, 1)
        remainder = parts[1]

        if OUTPUT_DELIMITER_SCHEMAS in remainder:
            bpmn_part, schema_part = remainder.split(OUTPUT_DELIMITER_SCHEMAS, 1)
        else:
            bpmn_part = remainder
            schema_part = "{}"

        bpmn_xml = bpmn_part.strip()
        if '```xml' in bpmn_xml:
            bpmn_xml = bpmn_xml.split('```xml')[1].split('```')[0].strip()
        elif '```' in bpmn_xml:
            bpmn_xml = bpmn_xml.split('```')[1].split('```')[0].strip()

        schema_text = schema_part.strip()
        if '```json' in schema_text:
            schema_text = schema_text.split('```json')[1].split('```')[0].strip()
        elif '```' in schema_text:
            schema_text = schema_text.split('```')[1].split('```')[0].strip()

        try:
            schema_files = json.loads(schema_text) if schema_text else {}
        except json.JSONDecodeError:
            schema_files = {}

        return bpmn_xml, schema_files

    def _fix_with_claude(
        self,
        bpmn_xml: str,
        error_message: str,
        system_messages: list,
        attempt: int,
    ) -> str:
        """
        Ask Claude to fix a specific SpiffWorkflow validation error.

        Returns the corrected BPMN XML string (schema files are not regenerated).
        """
        fix_message = (
            f"The BPMN XML you produced failed SpiffWorkflow validation "
            f"(attempt {attempt} of {MAX_FIX_ATTEMPTS}).\n\n"
            f"**Validation error:**\n```\n{error_message}\n```\n\n"
            f"Fix the error in the BPMN XML below and return **only the corrected "
            f"BPMN XML** — no delimiters, no schema files, no explanation.\n\n"
            f"**BPMN XML to fix:**\n\n{bpmn_xml}"
        )

        logger.info(
            "SpiffWorkflow validation failed (attempt %d/%d): %s — asking Claude to fix",
            attempt, MAX_FIX_ATTEMPTS, error_message[:120]
        )

        response_text, _ = self._call_claude(
            user_message=fix_message,
            system_messages=system_messages,
            max_tokens=16000,
            temperature=0,
        )

        fixed_bpmn, _ = self._parse_response(response_text)
        return fixed_bpmn

    def process(self, input_data: str, **kwargs) -> ComponentResult:
        """
        Convert standard BPMN XML to SpiffWorkflow-executable format.

        Pipeline:
            1. Claude converts the diagram (adding task types, spiff extensions,
               Python gateway conditions, and JSON schema stubs).
            2. SpiffWorkflow's BpmnParser + BpmnValidator validates the output.
            3. On failure, Claude fixes the specific error and validation repeats.
            4. After MAX_FIX_ATTEMPTS the best result is returned with success=False.

        Args:
            input_data: Standard BPMN 2.0 XML string

        Returns:
            ComponentResult with data as dict:
                {
                    "bpmn_xml": str,       # Converted (and validated) BPMN XML
                    "schema_files": dict,  # filename -> JSON object for each schema
                }
        """
        try:
            self.validate_input(input_data)

            skill_prompt = self._load_skill_prompt()
            system_messages = [{"type": "text", "text": skill_prompt}]

            # --- Initial generation ---
            user_message = (
                "Convert the following standard BPMN 2.0 diagram into a "
                "SpiffWorkflow-executable diagram:\n\n" + input_data
            )

            response_text, api_metadata = self._call_claude(
                user_message=user_message,
                system_messages=system_messages,
                max_tokens=16000,
                temperature=0,
            )

            bpmn_xml, schema_files = self._parse_response(response_text)
            fix_attempts = 0

            # --- Validation + fix loop ---
            while True:
                is_valid, validation_message = _spiff_validate(bpmn_xml)

                if is_valid:
                    logger.info("SpiffWorkflow validation passed: %s", validation_message)
                    break

                fix_attempts += 1
                if fix_attempts > MAX_FIX_ATTEMPTS:
                    logger.warning(
                        "SpiffWorkflow validation still failing after %d fix attempts",
                        MAX_FIX_ATTEMPTS,
                    )
                    return ComponentResult(
                        success=False,
                        data={"bpmn_xml": bpmn_xml, "schema_files": schema_files},
                        metadata={
                            **api_metadata,
                            "component": self.component_name,
                            "fix_attempts": fix_attempts - 1,
                            "validation_error": validation_message,
                            "schema_file_count": len(schema_files),
                        },
                        error=(
                            f"SpiffWorkflow validation failed after "
                            f"{MAX_FIX_ATTEMPTS} fix attempts: {validation_message}"
                        ),
                    )

                bpmn_xml = self._fix_with_claude(
                    bpmn_xml, validation_message, system_messages, fix_attempts
                )

            return ComponentResult(
                success=True,
                data={"bpmn_xml": bpmn_xml, "schema_files": schema_files},
                metadata={
                    **api_metadata,
                    "component": self.component_name,
                    "xml_length": len(bpmn_xml),
                    "fix_attempts": fix_attempts,
                    "schema_file_count": len(schema_files),
                    "schema_filenames": list(schema_files.keys()),
                    "validation": validation_message,
                },
            )

        except ValueError as e:
            return ComponentResult(
                success=False,
                data=None,
                metadata={"component": self.component_name},
                error=f"Validation error: {e}",
            )
        except Exception as e:
            return ComponentResult(
                success=False,
                data=None,
                metadata={"component": self.component_name},
                error=f"Processing error: {e}",
            )
