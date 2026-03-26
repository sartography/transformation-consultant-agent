"""
Recommendation engine component.

This component generates process optimization recommendations using
the process-optimization skill.
"""

from pathlib import Path
from typing import Any
from ...interfaces.component import BaseComponent, ComponentResult


class RecommendationEngine(BaseComponent):
    """
    Component for generating process optimization recommendations.

    Implements the process-optimization skill. Defaults to using Opus 4.5
    for better reasoning on complex business recommendations.
    """

    def __init__(self,
                 api_key: str,
                 model: str = "claude-opus-4-5-20251101",
                 config: dict = None):
        """
        Initialize recommendation engine.

        Args:
            api_key: Anthropic API key
            model: Claude model to use (defaults to Opus for better reasoning)
            config: Component-specific configuration
        """
        super().__init__(api_key, model, config)

    @property
    def component_name(self) -> str:
        """Return human-readable component name."""
        return "Process Optimization"

    @property
    def skill_path(self) -> Path:
        """Return path to SKILL.md file for this component."""
        return Path(__file__).parent.parent.parent.parent / "skills" / "process-optimization" / "SKILL.md"

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
        required_sections = ["## Process Steps", "## Pain Points"]
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

    def process(self, input_data: str, **kwargs) -> ComponentResult:
        """
        Generate optimization recommendations from process analysis.

        Args:
            input_data: Process analysis markdown
            **kwargs: Optional parameters:
                - business_context: Additional context (industry, budget, priorities)

        Returns:
            ComponentResult with recommendations markdown in data field
        """
        try:
            # Validate input
            self.validate_input(input_data)

            # Load skill prompt
            skill_prompt = self._load_skill_prompt()

            # Prepare system messages
            system_messages = [{"type": "text", "text": skill_prompt}]

            # Prepare user message
            business_context = kwargs.get('business_context', '')
            user_message = f"Please analyze this process and generate comprehensive optimization recommendations.\n\n"
            user_message += f"Process Analysis Document:\n{input_data}\n\n"

            if business_context:
                user_message += f"Additional Context:\n{business_context}\n\n"

            user_message += "Please provide specific technology recommendations, detailed ROI calculations, and a phased implementation roadmap."

            # Call Claude
            recommendations_text, api_metadata = self._call_claude(
                user_message=user_message,
                system_messages=system_messages,
                max_tokens=16000,
                temperature=0
            )

            # Validate output has key sections
            expected_sections = ["Executive Summary", "Quick Wins", "Implementation Roadmap"]
            missing_sections = [s for s in expected_sections if s not in recommendations_text]

            if missing_sections:
                warning = f"Recommendations missing sections: {', '.join(missing_sections)}"
            else:
                warning = None

            # Return result
            return ComponentResult(
                success=True,
                data=recommendations_text,
                metadata={
                    **api_metadata,
                    "component": self.component_name,
                    "model_used": self.model,
                    "warning": warning
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
