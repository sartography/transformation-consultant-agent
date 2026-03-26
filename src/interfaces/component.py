"""
Base component interface for transformation consultant agent.

This module defines the abstract base class that all components must implement,
as well as the standard result format returned by component execution.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import time
import logging

# Module logger
logger = logging.getLogger(__name__)

# Pricing per million tokens (as of January 2025)
MODEL_PRICING = {
    "claude-sonnet-4-5-20250929": {
        "input": 3.00,   # $3.00 per million input tokens
        "output": 15.00  # $15.00 per million output tokens
    },
    "claude-opus-4-5-20251101": {
        "input": 15.00,  # $15.00 per million input tokens
        "output": 75.00  # $75.00 per million output tokens
    }
}


@dataclass
class ComponentResult:
    """Standard result format from component execution."""

    success: bool
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseComponent(ABC):
    """
    Base interface for all transformation consultant components.

    All components must implement this interface to ensure consistency
    in how they validate input, process data, and return results.
    """

    def __init__(self,
                 api_key: str,
                 model: str = "claude-sonnet-4-5-20250929",
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize component.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
            config: Component-specific configuration including:
                - max_retries: Maximum retry attempts (default 3)
                - base_delay: Base delay in seconds for backoff (default 1.0)
                - max_delay: Maximum delay in seconds (default 60.0)
        """
        self.api_key = api_key
        self.model = model
        self.config = config or {}
        self._client = None  # Lazy initialization

        # Retry configuration
        self.max_retries = self.config.get('max_retries', 3)
        self.base_delay = self.config.get('base_delay', 1.0)
        self.max_delay = self.config.get('max_delay', 60.0)

    @property
    @abstractmethod
    def component_name(self) -> str:
        """Return human-readable component name."""
        pass

    @property
    @abstractmethod
    def skill_path(self) -> Path:
        """Return path to SKILL.md file for this component."""
        pass

    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data before processing.

        Args:
            input_data: Input to validate

        Returns:
            True if valid

        Raises:
            ValueError: If input is invalid
        """
        pass

    @abstractmethod
    def process(self, input_data: Any, **kwargs) -> ComponentResult:
        """
        Execute the component's main processing logic.

        Args:
            input_data: Input data (type varies by component)
            **kwargs: Additional component-specific parameters

        Returns:
            ComponentResult with success status, data, and metadata
        """
        pass

    def _get_client(self):
        """Lazy initialization of Anthropic client."""
        if self._client is None:
            from anthropic import Anthropic
            self._client = Anthropic(api_key=self.api_key)
        return self._client

    def _load_skill_prompt(self) -> str:
        """Load SKILL.md content."""
        return self.skill_path.read_text(encoding='utf-8')

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> dict:
        """
        Calculate estimated cost for API call.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dict with cost breakdown and total
        """
        pricing = MODEL_PRICING.get(self.model, {
            "input": 3.00,  # Default to Sonnet pricing
            "output": 15.00
        })

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost

        return {
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6)
        }

    def _call_claude(self,
                     user_message: str,
                     system_messages: list,
                     max_tokens: int = 16000,
                     temperature: float = 0) -> tuple[str, dict]:
        """
        Call Claude API with retry logic and exponential backoff.

        Args:
            user_message: User message content
            system_messages: List of system message dicts
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            Tuple of (response_text, usage_metadata)

        Raises:
            RuntimeError: If API call fails after all retries
        """
        from anthropic import APIError, RateLimitError, APIConnectionError

        client = self._get_client()
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                response = client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_messages,
                    messages=[{"role": "user", "content": user_message}]
                )

                # Calculate cost
                cost_info = self._calculate_cost(
                    response.usage.input_tokens,
                    response.usage.output_tokens
                )

                metadata = {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "model": self.model,
                    "attempts": attempt + 1,
                    **cost_info
                }

                return response.content[0].text, metadata

            except RateLimitError as e:
                last_exception = e
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.warning(
                    "Rate limited (attempt %d/%d). Retrying in %.1f seconds...",
                    attempt + 1, self.max_retries, delay
                )
                time.sleep(delay)

            except APIConnectionError as e:
                last_exception = e
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.warning(
                    "Connection error (attempt %d/%d). Retrying in %.1f seconds...",
                    attempt + 1, self.max_retries, delay
                )
                time.sleep(delay)

            except APIError as e:
                # Don't retry on client errors (4xx except rate limits)
                if hasattr(e, 'status_code') and 400 <= e.status_code < 500:
                    raise RuntimeError(f"Claude API client error: {str(e)}")
                last_exception = e
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.warning(
                    "API error (attempt %d/%d). Retrying in %.1f seconds...",
                    attempt + 1, self.max_retries, delay
                )
                time.sleep(delay)

            except Exception as e:
                # Non-retryable errors
                raise RuntimeError(f"Claude API call failed: {str(e)}")

        # All retries exhausted
        raise RuntimeError(
            f"Claude API call failed after {self.max_retries} attempts: {str(last_exception)}"
        )
