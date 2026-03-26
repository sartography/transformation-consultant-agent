"""
Integration tests for the modular pipeline architecture.

This demonstrates migrating from direct API calls to component-based architecture.
"""

import pytest
from pathlib import Path
from dotenv import load_dotenv
import os

from src.main import (
    create_full_pipeline,
    create_analysis_pipeline,
    create_bpmn_pipeline
)
from src.components.input.transcript_processor import TranscriptProcessor
from src.components.generation.bpmn_generator import BPMNGenerator
from src.components.optimization.recommendation_engine import RecommendationEngine

# Load environment
load_dotenv("config/.env")


@pytest.fixture
def api_key():
    """Get API key from environment."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    return key


@pytest.fixture
def sample_transcript():
    """Load sample transcript."""
    transcript_path = Path("data/sample-transcripts/ap-process.txt")
    if not transcript_path.exists():
        pytest.skip(f"Sample transcript not found: {transcript_path}")
    return transcript_path.read_text(encoding='utf-8')


@pytest.fixture
def sample_analysis():
    """Load sample analysis."""
    analysis_path = Path("outputs/analysis/example-01-ap-analysis-test.md")
    if not analysis_path.exists():
        pytest.skip(f"Sample analysis not found: {analysis_path}")
    return analysis_path.read_text(encoding='utf-8')


class TestComponentIndividual:
    """Test individual components in isolation."""

    def test_transcript_processor(self, api_key, sample_transcript):
        """Test transcript analysis component."""
        component = TranscriptProcessor(api_key=api_key)
        result = component.process(sample_transcript)

        assert result.success
        assert result.data is not None
        assert "## Process Steps" in result.data
        assert "## Actors and Roles" in result.data
        assert result.metadata["input_tokens"] > 0
        assert result.metadata["output_tokens"] > 0

    def test_bpmn_generator(self, api_key, sample_analysis):
        """Test BPMN generation component."""
        component = BPMNGenerator(api_key=api_key)
        result = component.process(sample_analysis)

        assert result.success
        assert result.data is not None
        assert "<?xml" in result.data
        assert "bpmn:definitions" in result.data or "bpmn2:definitions" in result.data
        assert "Valid BPMN XML" in result.metadata["validation"]

    def test_recommendation_engine(self, api_key, sample_analysis):
        """Test optimization recommendation component."""
        component = RecommendationEngine(
            api_key=api_key,
            model="claude-opus-4-5-20251101"
        )

        business_context = """
        Industry: Manufacturing
        Budget: $200K
        Priority: Reduce AP cycle time
        """

        result = component.process(
            sample_analysis,
            business_context=business_context
        )

        assert result.success
        assert result.data is not None
        # Check for some expected sections (may vary)
        assert "Executive Summary" in result.data or "Summary" in result.data


class TestPipelineIntegration:
    """Test pipeline execution."""

    def test_analysis_pipeline(self, api_key, sample_transcript):
        """Test transcript → analysis pipeline."""
        pipeline = create_analysis_pipeline(api_key=api_key)
        result = pipeline.execute(sample_transcript)

        assert result.success
        assert "Transcript Analysis" in result.outputs
        assert len(result.errors) == 0

    @pytest.mark.slow
    def test_full_pipeline(self, api_key, sample_transcript):
        """Test full transcript → analysis → BPMN → recommendations pipeline."""
        pipeline = create_full_pipeline(api_key=api_key)
        result = pipeline.execute(sample_transcript)

        # Check success
        assert result.success
        assert len(result.errors) == 0

        # Check all outputs present
        assert "Transcript Analysis" in result.outputs
        assert "BPMN Generation" in result.outputs
        assert "Process Optimization" in result.outputs

        # Validate outputs
        analysis = result.outputs["Transcript Analysis"]
        assert "## Process Steps" in analysis

        bpmn = result.outputs["BPMN Generation"]
        assert "<?xml" in bpmn

        recommendations = result.outputs["Process Optimization"]
        # Recommendations should have some content
        assert len(recommendations) > 100

    def test_pipeline_with_save(self, api_key, sample_transcript, tmp_path):
        """Test pipeline execution with output saving."""
        pipeline = create_full_pipeline(api_key=api_key)
        result = pipeline.execute(sample_transcript)

        # Save outputs
        output_dir = tmp_path / "outputs"
        result.save_outputs(output_dir)

        # Verify files created
        assert (output_dir / "transcript-analysis-analysis.md").exists()
        assert (output_dir / "bpmn-generation.bpmn").exists()
        assert (output_dir / "process-optimization-recommendations.md").exists()
        assert (output_dir / "pipeline-metadata.json").exists()


class TestComponentValidation:
    """Test component input validation."""

    def test_transcript_processor_validation(self, api_key):
        """Test TranscriptProcessor input validation."""
        component = TranscriptProcessor(api_key=api_key)

        # Test empty string
        result = component.process("")
        assert not result.success
        assert "empty" in result.error.lower()

        # Test too short
        result = component.process("short")
        assert not result.success
        assert "short" in result.error.lower()

    def test_bpmn_generator_validation(self, api_key):
        """Test BPMNGenerator input validation."""
        component = BPMNGenerator(api_key=api_key)

        # Test missing required sections
        result = component.process("# Some analysis\n\nBut missing required sections")
        assert not result.success
        assert "missing" in result.error.lower() and "required section" in result.error.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
