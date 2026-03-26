"""
Main entry point for transformation consultant agent.

Provides high-level functions for common workflows and pipeline creation.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from .pipeline import Pipeline, PipelineResult


def setup_logging(level: str = "INFO"):
    """
    Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


# Module logger
logger = logging.getLogger(__name__)
from .components.input.transcript_processor import TranscriptProcessor
from .components.generation.bpmn_generator import BPMNGenerator
from .components.optimization.recommendation_engine import RecommendationEngine

# Load environment variables
load_dotenv("config/.env")


def get_api_key() -> str:
    """
    Get Anthropic API key from environment.

    Returns:
        API key string

    Raises:
        ValueError: If ANTHROPIC_API_KEY not found in environment
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    return api_key


def create_full_pipeline(api_key: Optional[str] = None,
                        model: str = "claude-sonnet-4-5-20250929") -> Pipeline:
    """
    Create the full transformation consultant pipeline.

    Pipeline flow: Transcript → Analysis → BPMN → Recommendations

    Args:
        api_key: Anthropic API key (defaults to env var)
        model: Claude model to use for transcript and BPMN (Opus used for recommendations)

    Returns:
        Configured pipeline ready for execution
    """
    if api_key is None:
        api_key = get_api_key()

    # Create pipeline
    pipeline = Pipeline(name="Full Transformation Consultant Pipeline")

    # Add components
    pipeline.add_component(
        TranscriptProcessor(api_key=api_key, model=model),
        config={}
    )

    pipeline.add_component(
        BPMNGenerator(api_key=api_key, model=model),
        config={"include_apqc": True}
    )

    # Recommendation engine receives the analysis (from component 1), not the BPMN
    pipeline.add_component(
        RecommendationEngine(api_key=api_key, model="claude-opus-4-5-20251101"),
        config={"input_from": "Transcript Analysis"}
    )

    return pipeline


def create_analysis_pipeline(api_key: Optional[str] = None,
                             model: str = "claude-sonnet-4-5-20250929") -> Pipeline:
    """
    Create analysis-only pipeline.

    Pipeline flow: Transcript → Analysis

    Args:
        api_key: Anthropic API key (defaults to env var)
        model: Claude model to use

    Returns:
        Configured pipeline ready for execution
    """
    if api_key is None:
        api_key = get_api_key()

    pipeline = Pipeline(name="Transcript Analysis Pipeline")
    pipeline.add_component(
        TranscriptProcessor(api_key=api_key, model=model),
        config={}
    )

    return pipeline


def create_bpmn_pipeline(api_key: Optional[str] = None,
                        model: str = "claude-sonnet-4-5-20250929") -> Pipeline:
    """
    Create BPMN generation pipeline.

    Pipeline flow: Analysis → BPMN

    Args:
        api_key: Anthropic API key (defaults to env var)
        model: Claude model to use

    Returns:
        Configured pipeline ready for execution
    """
    if api_key is None:
        api_key = get_api_key()

    pipeline = Pipeline(name="BPMN Generation Pipeline")
    pipeline.add_component(
        BPMNGenerator(api_key=api_key, model=model),
        config={"include_apqc": True}
    )

    return pipeline


def run_full_transformation(transcript_path: Path,
                           output_dir: Path,
                           api_key: Optional[str] = None,
                           business_context: Optional[str] = None) -> PipelineResult:
    """
    High-level function to run full transformation from transcript to recommendations.

    Args:
        transcript_path: Path to transcript text file
        output_dir: Directory to save outputs
        api_key: Anthropic API key (defaults to env var)
        business_context: Optional context for optimization (industry, budget, etc.)

    Returns:
        PipelineResult with all outputs
    """
    # Load transcript
    transcript = Path(transcript_path).read_text(encoding='utf-8')

    # Create pipeline
    pipeline = create_full_pipeline(api_key=api_key)

    # Add business context if provided
    if business_context:
        # Update recommendation engine config
        pipeline.component_configs[2]['business_context'] = business_context

    # Execute
    logger.info("Starting full transformation pipeline")
    logger.info("Input: %s", transcript_path)
    logger.info("Output: %s", output_dir)

    result = pipeline.execute(transcript)

    # Save outputs
    if result.success:
        result.save_outputs(output_dir)
        logger.info("SUCCESS: Outputs saved to %s", output_dir)
    else:
        logger.error("FAILED: %s", result.errors)

    return result


def main():
    """Command-line interface for running the transformation pipeline."""
    import sys

    # Setup logging for CLI usage
    setup_logging(os.getenv("LOG_LEVEL", "INFO"))

    if len(sys.argv) < 2:
        print("Usage: python -m src.main <transcript_path> [output_dir]")
        sys.exit(1)

    transcript_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/generated"

    result = run_full_transformation(
        transcript_path=transcript_path,
        output_dir=output_dir
    )

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
