# Full Transformation Analysis

## Overview

Run the complete transformation consulting pipeline: analyze a process transcript, generate a BPMN diagram, and produce optimization recommendations — all in one command.

## Usage

```
/transformation-consultant:full-transformation <transcript> [output_dir]
```

## Arguments

- **transcript** — The process transcript text (pasted directly) or a file path to a transcript file (e.g., `data/sample-transcripts/ap-process.txt`)
- **output_dir** (optional) — Directory to save all outputs (defaults to `outputs/`)

## Workflow

### Step 1: Analyze Transcript

Using the **transcript-analysis** skill:

1. Read/load the transcript
2. Extract all process steps, actors, decision points, systems, pain points, timing, and exceptions
3. Produce a structured process analysis markdown document
4. Save to `[output_dir]/analysis/[process-name]-analysis.md`
5. Report: process name, step count, actor count, decision point count, pain point count

### Step 2: Generate BPMN Diagram

Using the **bpmn-generation** skill and APQC activities reference:

1. Take the analysis from Step 1 as input
2. Consolidate detailed steps into APQC Level 4 activities (target 5-10)
3. Generate valid BPMN 2.0 XML with swimlanes, gateways, and complete flow
4. Validate XML structure (unique IDs, connected elements, proper namespaces)
5. Save to `[output_dir]/bpmn-diagrams/[process-name].bpmn`
6. Report: activity count, gateway count, lane count

### Step 3: Generate Optimization Recommendations

Using the **process-optimization** skill:

1. Take the analysis from Step 1 as input
2. Categorize pain points and identify automation opportunities
3. Prioritize recommendations by impact and feasibility
4. Calculate ROI estimates for each recommendation
5. Produce implementation roadmap with phased approach
6. Save to `[output_dir]/recommendations/[process-name]-recommendations.md`
7. Report: number of recommendations, total estimated savings, payback period

### Step 4: Summary Report

After all three steps complete, provide a consolidated summary:

```
## Transformation Analysis Complete

### Process: [Process Name]

### Outputs Generated:
1. Process Analysis: [file path]
2. BPMN Diagram: [file path]
3. Optimization Recommendations: [file path]

### Key Findings:
- [X] process steps identified across [Y] actors
- [Z] pain points found, [W] automation opportunities identified
- Top 3 recommendations:
  1. [Recommendation] — Est. savings: $[X]/year
  2. [Recommendation] — Est. savings: $[X]/year
  3. [Recommendation] — Est. savings: $[X]/year
- Total estimated annual savings: $[X]
- Recommended implementation investment: $[X]
- Expected payback period: [X] months

### Next Steps:
- Review the process analysis with stakeholders for accuracy
- Open the BPMN diagram in a viewer (bpmn.io, Camunda Modeler) to validate the flow
- Prioritize recommendations with leadership based on strategic alignment
- Generate an executive presentation: `/transformation-consultant:create-presentation [recommendations-path] [analysis-path]`
```

## Output

1. **Process Analysis** — Structured markdown document
2. **BPMN 2.0 Diagram** — Valid XML file for visualization
3. **Optimization Recommendations** — Comprehensive recommendations with ROI
4. **Summary Report** — Consolidated findings and next steps

## Example

```
/transformation-consultant:full-transformation data/sample-transcripts/ap-process.txt outputs/ap-transformation
```

This will analyze the Accounts Payable process transcript and save all outputs to `outputs/ap-transformation/`.

## Important Note

This command runs three analysis steps sequentially. Each step builds on the previous one. The full pipeline typically produces 3 output files. All outputs should be reviewed by qualified professionals and process stakeholders before use in decision-making.
