# Create Executive Presentation

## Overview

Generate an executive-style HTML slide presentation summarizing the transformation analysis results. Uses the [frontend-slides](https://github.com/zarazhangrui/frontend-slides) skill to produce a polished, animation-rich presentation with zero dependencies.

## Usage

```
/transformation-consultant:create-presentation <recommendations> [analysis]
```

## Arguments

- **recommendations** — Path to the optimization recommendations markdown file (e.g., `outputs/recommendations/ap-recommendations.md`)
- **analysis** (optional) — Path to the process analysis markdown file for additional context (e.g., `outputs/analysis/ap-analysis.md`)

## Prerequisites

The `frontend-slides` skill must be installed:

```bash
# Install the frontend-slides skill
git clone https://github.com/zarazhangrui/frontend-slides.git ~/.claude/skills/frontend-slides
```

## Workflow

### Step 1: Load Source Materials

1. Read the recommendations file
2. Read the analysis file (if provided)
3. Extract key data points:
   - Process name
   - Executive summary and key metrics
   - Top recommendations with ROI figures
   - Implementation roadmap phases
   - Total estimated savings and investment
   - Pain point highlights

### Step 2: Prepare Slide Content

Structure the presentation into these slides:

1. **Title Slide** — Process name + "Transformation Recommendations"
2. **Executive Summary** — 3-4 bullet overview of current state and opportunity
3. **Key Metrics** — Current volume, cycle time, annual cost, estimated savings, payback period
4. **Top Pain Points** — 3-5 highest-impact pain points from the analysis
5. **Quick Wins (0-3 Months)** — Top 2-3 quick win recommendations with expected impact
6. **Medium-Term Improvements (3-6 Months)** — Top 2-3 medium-term recommendations
7. **Long-Term Transformations (6-12+ Months)** — Top 1-2 strategic initiatives
8. **Implementation Roadmap** — Phased timeline visualization (Phase 1, 2, 3)
9. **Investment & ROI** — Total investment, annual savings, payback period, 3-year NPV
10. **Next Steps** — Recommended immediate actions for stakeholders

### Step 3: Generate Presentation

1. Invoke the `frontend-slides` skill with the prepared slide content
2. Request a professional, executive-appropriate theme (suggest: Swiss Modern, Vintage Editorial, or Split Pastel)
3. Select from the three visual previews presented
4. Generate the full HTML presentation

### Step 4: Save and Deliver

1. Save the HTML file to `[output_dir]/presentations/[process-name]-executive-summary.html`
2. Open the presentation in the browser
3. Report: slide count, theme used, file path

## Output

- **Executive Presentation** — Self-contained HTML file with embedded CSS/JS, animations, and professional styling. Opens directly in any browser with no dependencies.

## Slide Content Guidelines

- **Keep it executive-level**: No technical jargon, focus on business impact and ROI
- **Lead with numbers**: Every slide should have quantified impact where possible
- **Respect viewport limits**: 4-6 bullets per slide maximum, no scrolling
- **Visual hierarchy**: Use the recommendation priority scores to order content
- **Actionable close**: End with concrete next steps, not vague suggestions

## Example

```
# After running the full pipeline
/transformation-consultant:create-presentation outputs/recommendations/ap-recommendations.md outputs/analysis/ap-analysis.md
```

This will generate an executive presentation summarizing the AP process transformation recommendations.

## Important Note

This command requires the `frontend-slides` skill to be installed separately. The presentation distills detailed recommendations into executive-friendly slides — it is not a replacement for the full recommendations document. Both should be shared with stakeholders: the presentation for alignment meetings, the full document for implementation planning.
