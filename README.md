# Transformation Consultant

An AI-powered business process transformation consultant plugin for Claude. Analyze process transcripts, generate BPMN 2.0 diagrams, and produce optimization recommendations with ROI analysis.

## Overview

This plugin gives Claude deep expertise in business process transformation consulting. It can:

- **Analyze process transcripts** from interviews and walkthroughs to extract structured process information
- **Generate BPMN 2.0 diagrams** with APQC Level 4 activity consolidation for clean, standardized visualizations
- **Produce optimization recommendations** with automation opportunities, technology recommendations, ROI analysis, and implementation roadmaps

## Installation

```bash
claude plugins add knowledge-work-plugins/transformation-consultant
```

## Commands

| Command | Description |
|---------|-------------|
| `/transformation-consultant:analyze-transcript` | Analyze a business process transcript and extract structured process information |
| `/transformation-consultant:generate-bpmn` | Generate a BPMN 2.0 XML diagram from a process analysis |
| `/transformation-consultant:optimize-process` | Generate optimization recommendations with ROI analysis |
| `/transformation-consultant:full-transformation` | Run the complete pipeline: transcript analysis, BPMN generation, and optimization |
| `/transformation-consultant:create-presentation` | Generate an executive HTML slide presentation from recommendations |

## Skills

| Skill | Description |
|-------|-------------|
| `transcript-analysis` | Domain expertise in extracting structured process information from conversational transcripts |
| `bpmn-generation` | BPMN 2.0 diagram generation with APQC Level 4 activity consolidation and validation |
| `process-optimization` | Business process optimization consulting with prioritization frameworks and ROI analysis |

Skills activate automatically when Claude detects relevant context in the conversation.

## Example Workflows

### Full Transformation (Recommended)

Run the complete pipeline on a process transcript:

```
/transformation-consultant:full-transformation data/sample-transcripts/ap-process.txt
```

This produces three outputs:
1. **Process Analysis** — Structured breakdown of steps, actors, decisions, and pain points
2. **BPMN Diagram** — Valid BPMN 2.0 XML ready for visualization
3. **Optimization Recommendations** — Prioritized improvements with ROI estimates

### Step-by-Step Analysis

For more control, run each step individually:

```
# Step 1: Analyze the transcript
/transformation-consultant:analyze-transcript data/sample-transcripts/ap-process.txt

# Step 2: Generate BPMN from the analysis
/transformation-consultant:generate-bpmn outputs/analysis/ap-analysis.md

# Step 3: Get optimization recommendations
/transformation-consultant:optimize-process outputs/analysis/ap-analysis.md
```

### Executive Presentation

After running the pipeline, generate an executive slide deck:

```
/transformation-consultant:create-presentation outputs/recommendations/ap-recommendations.md outputs/analysis/ap-analysis.md
```

This uses the [frontend-slides](https://github.com/zarazhangrui/frontend-slides) skill to produce a polished HTML presentation. Requires the skill to be installed separately — see `commands/create-presentation.md` for setup.

### With Business Context

Provide additional context for more targeted recommendations:

```
/transformation-consultant:optimize-process outputs/analysis/ap-analysis.md "Industry: Healthcare, Budget: $500K, Team size: 12 FTEs, Priority: reduce cycle time"
```

## MCP Integration

> **Note:** For connector setup and configuration details, see [CONNECTORS.md](./CONNECTORS.md).

This plugin can connect to external tools via MCP servers configured in `.mcp.json`:

- **Slack** — Share results with team channels
- **Microsoft 365** — Read transcripts from SharePoint, save outputs to shared libraries

## Sample Data

The `data/sample-transcripts/` directory includes example transcripts for testing:

- `ap-process.txt` — Accounts Payable invoice processing walkthrough
- `gl-month-end-close.txt` — General Ledger month-end close process

## Python Backup Mode

This project also includes a standalone Python implementation for programmatic execution. See [SETUP.md](SETUP.md) for Python setup instructions.

```bash
# Run via Python CLI
python -m src.main data/sample-transcripts/ap-process.txt outputs/test
```

```python
# Run via Python API
from src.main import run_full_transformation

result = run_full_transformation(
    transcript_path="data/sample-transcripts/ap-process.txt",
    output_dir="outputs/my-analysis"
)
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation of the Python component architecture.

## Contributing

Feedback and suggestions welcome! Fork the repo, edit the markdown/JSON files, and submit a PR.

## License

[MIT](LICENSE)
