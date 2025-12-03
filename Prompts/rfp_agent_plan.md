# RFP Analysis Agent - Parallel Execution Plan

## Prompt Organization Structure
```
Prompts/
├── Analysis/
│   ├── Competitor analysis Prompt.md
│   ├── Inconsistency Prompt.md
│   ├── Pain points Prompt.md
│   ├── Pricing Prompt.md          # Analyzes competitor pricing
│   └── win themes Prompt.md
├── Extraction/
│   ├── Evaluation Prompt.md
│   ├── Questions Prompt.md
│   ├── Requirements Prompt.md
│   └── Timeline Prompt.md
└── Summary/
    ├── Opportunity_Overview.md    # NEW
    ├── Go-no go Prompt.md         
    ├── Overall competitor analysis Prompt.md
    ├── Overall_Pricing.md         # NEW
    └── Executive_Summary.md       # NEW
```

## Parallel Execution Architecture

### Phase 0: Setup & Context
**Sequential**
1. **Opportunity_Overview.md** - Extract basic opportunity details
2. Collect user inputs (competitors, win themes, context)

### Phase 1: Extraction [PARALLEL]
**Run all simultaneously:**
- **Requirements.md** → `requirements_extract.md`
- **Questions.md** → `questions_extract.md`
- **Timeline.md** → `timeline_extract.md`
- **Evaluation.md** → `evaluation_extract.md`

*Wait for all extractions to complete*

### Phase 2A: Initial Analysis [PARALLEL]
**Run simultaneously:**
- **Pain points.md** → `pain_points_analysis.md`
- **Inconsistency.md** → `inconsistency_analysis.md`

### Phase 2B: Competitive & Pricing [PARALLEL]
**Run simultaneously after Phase 2A (per competitor):**
- **For each competitor, run both:**
  - **Competitor analysis.md** → `competitor_[NAME].md`
  - **Pricing.md** → `pricing_[NAME].md`
  
Example for 3 competitors:
- IBM: `competitor_IBM.md` + `pricing_IBM.md`
- Deloitte: `competitor_Deloitte.md` + `pricing_Deloitte.md`
- TCS: `competitor_TCS.md` + `pricing_TCS.md`

### Phase 3: Strategy Development
**Sequential (depends on Phase 2B):**
1. **Overall competitor analysis.md** → `overall_competitor_analysis.md`
2. **Overall_Pricing.md** → `overall_pricing_analysis.md`
3. **Win themes.md** → `win_themes.md`

### Phase 4: Decision & Summary
**Sequential:**
1. **Go-no go.md** → `go_no_go_decision.md`
2. **Executive_Summary.md** → `executive_summary.md`

## Execution Timeline Visualization
```
Time →
│
├─ Phase 0: Setup (Sequential)
│   └─ Opportunity Overview + User Inputs
│
├─ Phase 1: [========== PARALLEL EXTRACTION ==========]
│   ├─ Requirements ─────────────────┐
│   ├─ Questions ────────────────────┤
│   ├─ Timeline ─────────────────────┤
│   └─ Evaluation ───────────────────┴─→ Wait Gate
│
├─ Phase 2A: [===== PARALLEL ANALYSIS =====]
│   ├─ Pain Points ──────────┐
│   └─ Inconsistency ────────┴─→ Continue to 2B
│
├─ Phase 2B: [===== PARALLEL COMPETITIVE (2N analyses) =====]
│   ├─ Competitor 1 + Pricing 1 ──┐
│   ├─ Competitor 2 + Pricing 2 ──┤
│   ├─ Competitor 3 + Pricing 3 ──┤
│   └─ Competitor N + Pricing N ──┴─→ Wait Gate
│
├─ Phase 3: Strategy (Sequential)
│   ├─ Overall Competitor Analysis
│   ├─ Overall Pricing Analysis
│   └─ Win Themes
│
└─ Phase 4: Decision (Sequential)
    ├─ Go/No-Go Decision
    └─ Executive Summary
```

## Proposed New Prompts (Requiring Approval)

### 1. Overall_Pricing.md (Summary/)
```markdown
Consolidate all competitor pricing analyses and recommend Accenture's pricing strategy.

## Competitive Pricing Landscape

### Price Range Analysis
| Competitor | Estimated Bid Range | Pricing Strategy | Confidence |
|------------|-------------------|------------------|------------|
| [From individual pricing analyses] | $X.XM - $X.XM | [Aggressive/Value/Premium] | [L/M] |

### Average Market Price
- Mean: $X.XM
- Median: $X.XM
- Range: $X.XM - $X.XM

## Pricing Pressure Indicators
- Budget mentioned in RFP: [Yes/No - amount if stated]
- Weight of price in evaluation: [X%]
- Evidence of price sensitivity: [List indicators]

## Recommended Accenture Pricing Strategy

### Price Positioning
[ ] Below market (-X%) - Win at all costs
[ ] At market - Competitive positioning
[ ] Above market (+X%) - Value positioning

### Recommended Bid Range
- Minimum viable: $X.XM
- Target: $X.XM
- Walk-away: $X.XM

### Pricing Rationale
[2-3 paragraphs explaining the recommendation based on:]
- Competitive landscape
- Win probability vs margin trade-off
- Strategic importance
- Risk factors

### Pricing Levers
| Lever | Description | Impact |
|-------|-------------|--------|
| Offshore mix | Increase to X% | -$X.XM |
| Phasing | Front/back-load | Cashflow impact |
| Risk sharing | Outcome-based component | Client appeal |

OUTPUT: Save as "overall_pricing_analysis.md" in Output folder.
```

### 2. Opportunity_Overview.md (Summary/)
```markdown
Extract key opportunity information from the RFP:

## Opportunity Details
- Opportunity Name:
- Issuing Organization:
- Industry/Sector:
- Geographic Scope:
- Estimated Contract Value (if stated):
- Contract Type:
- Incumbent (if mentioned):

## Scope Summary
Provide 2-3 sentence summary of what is being procured.

## Key Stakeholders
List any named stakeholders/evaluation team members.

OUTPUT: Save as "opportunity_overview.md" in Output folder.
```

### 2. Executive_Summary.md (Summary/)
```markdown
Create executive summary incorporating all analysis outputs:

## Executive Summary

### Opportunity Overview
[From opportunity_overview.md]

### Strategic Fit
- Alignment with Accenture capabilities
- Market position implications
- Growth potential

### Competitive Landscape
[From overall_competitor_analysis.md]

### Win Probability Assessment
- Key strengths for this opportunity
- Main risks and mitigations
- Differentiation potential

### Win Themes
[From win_themes.md - top 3]

### Recommendation
[From go_no_go.md]

### Key Actions Required
- Immediate next steps
- Critical clarifications needed
- Resource mobilization

OUTPUT: Save as "executive_summary.md" in Output folder.
```

## Content for Empty Prompts

### Go-no go Prompt.md (Summary/)
```markdown
Synthesize all analysis outputs for pursuit decision:

## Go/No-Go Decision Framework

### Opportunity Score (0-100)
Score based on:
- Strategic alignment: /25
- Win probability: /25  
- Financial attractiveness: /25
- Risk/reward balance: /25

### Go Criteria Assessment
| Criterion | Met? | Evidence | Impact |
|-----------|------|----------|---------|
| Strategic fit | Y/N | | High/Med/Low |
| Revenue potential | Y/N | | High/Med/Low |
| Competitive position | Y/N | | High/Med/Low |
| Delivery capability | Y/N | | High/Med/Low |

### Recommendation
[ ] GO - Pursue with full resources
[ ] CONDITIONAL GO - Pursue with conditions: [list]
[ ] NO GO - Do not pursue

### Rationale
[2-3 paragraphs explaining decision]

OUTPUT: Save as "go_no_go_decision.md" in Output folder.
```

### Overall competitor analysis Prompt.md (Summary/)
```markdown
Consolidate individual competitor analyses:

## Competitive Landscape Overview

### Competitor Positioning Matrix
| Competitor | Key Strength | Main Weakness | Likely Strategy | Threat Level (H/M/L) |
|------------|--------------|---------------|-----------------|---------------------|

### Accenture's Competitive Position
- Unique advantages:
- Relative weaknesses:
- Differentiation opportunities:

### Recommended Positioning Strategy
Based on competitor analysis:
1. Lead messages:
2. Proof points to emphasize:
3. Competitor weaknesses to exploit:
4. Areas to defend/mitigate:

### Win Theme Alignment
Map competitive strategy to win themes.

OUTPUT: Save as "overall_competitor_analysis.md" in Output folder.
```

## Custom Command Implementation

```bash
# Command structure
rfp-analyze [options]

# Options:
--all                          # Run complete analysis
--phase <0-4>                  # Run specific phase
--prompt "<name>"              # Run specific prompt
--competitors "IBM,Deloitte"   # Set competitors (comma-separated)
--parallel-limit <n>           # Max parallel processes (default: 10)
--output-dir <path>           # Override Output folder
--resume                      # Resume from checkpoint
--validate                    # Validate outputs only
```

## State Management (.rfp-state.json)
```json
{
  "session": {
    "id": "uuid",
    "started": "timestamp",
    "rfp_name": ""
  },
  "execution": {
    "current_phase": 0,
    "phase_status": {
      "0": "completed",
      "1": "running",
      "2A": "pending",
      "2B": "pending",
      "3": "pending",
      "4": "pending"
    },
    "running_prompts": [],
    "completed_prompts": [],
    "failed_prompts": []
  },
  "user_inputs": {
    "competitors": [],
    "win_themes": [],
    "additional_context": ""
  },
  "outputs": {
    "extraction": {},
    "analysis": {},
    "summary": {}
  }
}
```

## Sequential Execution Fallback

If parallel agents are not available, execute in this order:

1. **Phase 0**: Opportunity Overview → User Inputs
2. **Phase 1**: Requirements → Questions → Timeline → Evaluation
3. **Phase 2A**: Pain Points → Inconsistency
4. **Phase 2B**: For each competitor:
   - Competitor Analysis [NAME]
   - Pricing [NAME]
5. **Phase 3**: Overall Competitor → Overall Pricing → Win Themes
6. **Phase 4**: Go/No-Go → Executive Summary

## Parallel Execution Benefits

1. **Time Savings**:
   - Phase 1: 4 extractions in parallel (4x faster)
   - Phase 2B: 2N analyses in parallel (2Nx faster)
   - Total time: ~35% of sequential execution

2. **Resource Optimization**:
   - Multiple AI agents working simultaneously
   - Better CPU/memory utilization
   - Reduced total execution time

3. **Dependency Management**:
   - Clear phase gates ensure data availability
   - No race conditions
   - Proper sequencing where needed

## Implementation Notes

1. **Error Handling**:
   - If any extraction fails, halt before Phase 2
   - Log failures but continue other parallel tasks
   - Retry mechanism for transient failures

2. **Output Organization**:
   ```
   Output/
   ├── extracts/
   ├── analysis/
   ├── summary/
   └── .rfp-state.json
   ```

3. **Progress Tracking**:
   - Real-time status updates
   - Phase completion notifications
   - Estimated time remaining

## Questions for Approval

1. **New Prompts**: Do you approve these 2 new prompts?
   - Opportunity_Overview.md
   - Executive_Summary.md (for Summary folder)

2. **Empty Prompt Content**: Do you approve the proposed content for:
   - Pricing Prompt.md
   - Go-no go Prompt.md
   - Overall competitor analysis Prompt.md

3. **Execution Order**: Does the parallel phased approach align with your workflow?

4. **Custom Command**: Any additional command options needed?