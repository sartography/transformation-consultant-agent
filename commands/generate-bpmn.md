# Generate BPMN Diagram

## Overview

Generate a valid BPMN 2.0 XML diagram from a structured process analysis, using APQC Level 4 activity consolidation for clean, standardized diagrams.

## Usage

```
/transformation-consultant:generate-bpmn <analysis>
```

## Arguments

- **analysis** — The process analysis markdown (from `/transformation-consultant:analyze-transcript`) provided as pasted text or a file path (e.g., `outputs/analysis/ap-analysis.md`)

## Workflow

### 1. Load Analysis

- If a file path is provided, read the analysis from the file
- Verify the analysis contains the required sections: Process Steps, Actors and Roles, Decision Points
- Load the APQC activities reference from `skills/bpmn-generation/domain-knowledge/apqc-activities.md`

### 2. Map to APQC Activities

- Read all process steps from the analysis
- Identify logical groupings of steps that accomplish a single business activity
- Check decision points — never consolidate across decision boundaries
- Map grouped steps to APQC Level 4 standard activity names when the domain matches
- Target 5-10 APQC activities (not 15-20 individual steps)

### 3. Generate BPMN 2.0 XML

Using the **bpmn-generation** skill, generate valid BPMN 2.0 XML with:

- **Swimlanes**: One lane per actor from the Actors and Roles table
- **Tasks**: APQC Level 4 activities assigned to appropriate lanes
- **Gateways**: Exclusive gateways for each decision point, named as questions
- **Sequence Flows**: Connecting all elements with labeled decision paths
- **Start/End Events**: Named descriptively (e.g., "Invoice Received", "Payment Complete")
- **Diagram Section**: BPMNDiagram with shapes and edges for all elements

### 4. Validate Output

Before saving, verify:

- All elements have unique IDs
- All sequence flows have valid sourceRef and targetRef
- All tasks are assigned to lanes
- At least one start event and one end event exist
- No orphaned elements
- Gateway outgoing flows have labels
- XML is well-formed
- APQC consolidation applied (5-10 activities)

### 5. Save Output

- Save as a `.bpmn` file (e.g., `outputs/bpmn-diagrams/[process-name].bpmn`)
- Report the diagram contents: number of activities, gateways, lanes, and flows

## Output

1. **BPMN 2.0 XML File** — Complete, valid BPMN XML ready for visualization in tools like bpmn.io, Camunda Modeler, or Signavio
2. **Diagram Summary** — Activity count, gateway count, lane count, flow count
3. **Consolidation Map** — Which original steps were grouped into each APQC activity
4. **Next Steps** — Suggest running `/transformation-consultant:optimize-process` if not already done

## Important Note

This command generates BPMN diagrams for process visualization and documentation. The diagrams are not executable process definitions. Review the generated diagram in a BPMN viewer to verify accuracy before using in formal documentation or presentations.
