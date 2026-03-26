# Optimize Process

## Overview

Generate comprehensive optimization recommendations with ROI analysis for a business process, including automation opportunities, technology recommendations, and an implementation roadmap.

## Usage

```
/transformation-consultant:optimize-process <analysis> [business_context]
```

## Arguments

- **analysis** — The process analysis markdown (from `/transformation-consultant:analyze-transcript`) provided as pasted text or a file path (e.g., `outputs/analysis/ap-analysis.md`)
- **business_context** (optional) — Additional context such as industry, company size, budget constraints, team size, or strategic priorities

## Workflow

### 1. Load Analysis

- If a file path is provided, read the analysis from the file
- Verify the analysis contains the required sections: Process Steps, Pain Points and Inefficiencies
- If business context is provided, incorporate it into the analysis

### 2. Categorize Pain Points

Group all identified pain points into categories:

- **Manual/Repetitive Work** — Tasks suitable for automation
- **Integration Issues** — System disconnects requiring integration
- **Process Design Flaws** — Unnecessary steps, bottlenecks, sequential dependencies
- **Data Quality** — Errors, missing information, inconsistent data
- **User Experience** — Workarounds, complexity, training issues
- **Visibility/Control** — Lack of tracking, reporting, or monitoring

### 3. Identify Automation Opportunities

Evaluate each pain point for automation potential:

- **RPA** — Rule-based, repetitive, cross-system tasks
- **Intelligent Document Processing** — OCR, data extraction, classification
- **Workflow Automation** — Routing, notifications, approvals, status updates
- **API Integrations** — Real-time system-to-system data exchange
- **Business Rules Engines** — Complex decision logic automation
- **AI/ML Applications** — Pattern recognition, prediction, classification

### 4. Prioritize and Calculate ROI

For each recommendation:

- Score Impact (1-10) and Feasibility (1-10)
- Estimate time savings, error reduction, and cost avoidance
- Calculate implementation costs (software, services, internal labor)
- Determine payback period and 3-year NPV
- Classify as Quick Win (0-3 months), Medium-Term (3-6 months), or Long-Term (6-12+ months)

### 5. Generate Recommendations

Using the **process-optimization** skill, produce a comprehensive document with:

```
# Process Optimization Recommendations: [Process Name]

## Executive Summary (with Key Metrics)
## Quick Wins (0-3 Months) — each with problem, solution, tech, steps, benefits, ROI, risks
## Medium-Term Improvements (3-6 Months)
## Long-Term Transformations (6-12+ Months)
## Implementation Roadmap (3 phases with milestones)
## Technology Stack Recommendations (table with costs)
## Change Management Considerations
## Success Metrics and KPIs
## Risk Assessment Summary
## Appendix: Detailed Assumptions
```

### 6. Save Output

- Save as a markdown file (e.g., `outputs/recommendations/[process-name]-recommendations.md`)
- Provide a summary highlighting the top 3 recommendations and total estimated ROI

## Output

1. **Optimization Recommendations Document** — Complete structured markdown with all recommendations
2. **Executive Summary** — Top findings, total estimated savings, and recommended next steps
3. **Priority Matrix** — Quick reference of all recommendations ranked by impact and feasibility

## Important Note

This command provides optimization recommendations based on process analysis. ROI estimates use conservative assumptions but should be validated against your organization's actual costs and volumes. All recommendations should be reviewed by process owners and relevant stakeholders before implementation decisions are made.
