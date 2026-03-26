# Analyze Process Transcript

## Overview

Analyze a business process transcript from an interview or walkthrough and extract structured process information suitable for BPMN modeling and optimization.

## Usage

```
/transformation-consultant:analyze-transcript <transcript>
```

## Arguments

- **transcript** — The process transcript text (pasted directly) or a file path to a transcript file (e.g., `data/sample-transcripts/ap-process.txt`)

## Workflow

### 1. Load Transcript

- If a file path is provided, read the transcript from the file
- If text is pasted directly, use it as-is
- Verify the transcript is at least 100 characters and appears to describe a business process

### 2. Analyze Transcript

Using the **transcript-analysis** skill and its domain knowledge examples, analyze the transcript to extract:

- All process steps in sequential order
- Actors and roles involved
- Decision points with conditions and outcomes
- Systems and tools used
- Pain points, inefficiencies, and challenges
- Timing and duration information
- Exceptional cases and workarounds

### 3. Generate Structured Output

Produce a structured markdown document following this format:

```
# Process Analysis: [Process Name]

## Executive Summary
## Process Steps (with Actor, Description, Input, Output, Duration, Pain Points per step)
## Actors and Roles (table)
## Decision Points (with Location, Condition, Outcomes, Decision Maker)
## Systems and Tools (table)
## Pain Points and Inefficiencies (Critical Issues + Inefficiencies)
## Process Metrics (Total Steps, Decision Points, Actors, Pain Points, Manual Steps, Systems)
## Notes and Observations
```

### 4. Save Output

- Save the analysis as a markdown file (e.g., `outputs/analysis/[process-name]-analysis.md`)
- Confirm the file was saved and provide a summary of key findings:
  - Process name
  - Number of steps, actors, decision points, and pain points identified
  - Top 3 pain points found

## Output

1. **Process Analysis Document** — Complete structured markdown analysis
2. **Summary** — Key metrics and top findings
3. **Next Steps** — Suggest running `/transformation-consultant:generate-bpmn` or `/transformation-consultant:optimize-process` with the analysis output

## Important Note

This command analyzes process transcripts to extract structured information. The quality of the analysis depends on the detail and clarity of the source transcript. All outputs should be reviewed by process stakeholders for accuracy before use in decision-making.
