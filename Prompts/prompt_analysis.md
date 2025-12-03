# RFP Analysis Agent - Prompt Analysis & Engineering Plan

## Current State Analysis

### 1. Extraction Prompts (Foundation Layer)
These prompts extract raw data from RFP documents:

| Prompt | Purpose | Output Format | Key Features | Dependencies |
|--------|---------|---------------|--------------|--------------|
| **Requirements.md** | Extract all requirements into structured table | Excel-compatible table with Req_ID, Type, Category | - Mirrors source structure<br>- Handles batch mode for >50 reqs<br>- Preserves original wording | None |
| **Questions.md** | Extract all response items requiring vendor input | Detailed table with ID, Category, Source, Text, Response Type | - Comprehensive categorization (Technical/Pricing/Legal/Admin)<br>- Handles multiple file types<br>- Priority flagging system | None |
| **Timeline.md** | Extract all dates and deadlines | Categorized tables by type (RFP Process, Contract Terms, etc.) | - Handles relative and explicit dates<br>- Business vs Calendar days<br>- Dynamic category generation | None |
| **Evaluation.md** | Extract scoring/marking criteria | Tables matching source + strategic insights | - Preserves weights and scoring<br>- Identifies mandatory requirements<br>- Adds strategic analysis | None |

### 2. Analysis Prompts (Intelligence Layer)
These prompts analyze extracted data for insights:

| Prompt | Purpose | Output Format | Key Features | Dependencies |
|--------|---------|---------------|--------------|--------------|
| **Pain points.md** | Identify buyer pain points | Two sections: Explicit & Implicit | - Advanced linguistic analysis<br>- Signal type identification<br>- Confidence scoring | Requirements, Questions extracts |
| **Inconsistency.md** | Find contradictions/ambiguities | Categorized inconsistencies with severity | - Cross-document conflict detection<br>- Clarification questions<br>- Severity ranking | All extraction outputs |
| **Competitor analysis.md** | Analyze specific competitors | 4-column strategic table | - Strength/weakness mapping<br>- Counter-strategy development<br>- Evidence-based approach | User input (competitor names) |
| **Win themes.md** | Generate differentiated win themes | Accepted/Rejected/Potential themes | - Competitor differentiation test<br>- Client relevance mapping<br>- Proof point requirements | Pain points, Evaluation, Competitor analysis |
| **Pricing.md** | *(Empty - needs content)* | TBD | TBD | TBD |

### 3. Summary Prompts (Decision Layer)
These prompts synthesize analysis for decisions:

| Prompt | Purpose | Output Format | Key Features | Dependencies |
|--------|---------|---------------|--------------|--------------|
| **Go-no go.md** | *(Empty - needs content)* | TBD | TBD | All analysis outputs |
| **Overall competitor analysis.md** | *(Empty - needs content)* | TBD | TBD | All competitor analyses |

## Identified Gaps & Issues

### 1. Missing Content (Critical)
- **Pricing Prompt.md** - Empty file, needs pricing analysis framework
- **Go-no go Prompt.md** - Empty file, needs decision framework
- **Overall competitor analysis Prompt.md** - Empty file, needs consolidation framework

### 2. Missing Prompts (Recommended Additions)
- **Opportunity Summary** - Extract basic opportunity details (name, buyer, value, industry)
- **Risk Assessment** - Identify and categorize proposal risks
- **Resource Requirements** - Estimate effort and team needs
- **Compliance Matrix** - Generate compliance response framework
- **Executive Summary** - Synthesize key findings for leadership

### 3. Process Improvements Needed
- No state management between prompts (each runs independently)
- No validation/quality checks built in
- No handling for different RFP formats (PDF vs Excel vs Word)
- No progress tracking or error recovery

## Optimal Execution Order

### Phase 1: Foundation (Extract Raw Data)
1. **Opportunity Summary** *(new)* - Get basic context first
2. **Requirements.md** - Core requirements understanding
3. **Questions.md** - What needs answering
4. **Timeline.md** - When things are due
5. **Evaluation.md** - How we'll be scored

### Phase 2: Deep Analysis (Generate Insights)
6. **Pain points.md** - Understand buyer needs
7. **Inconsistency.md** - Identify clarification needs
8. **Pricing.md** *(needs content)* - Analyze pricing requirements
9. **Risk Assessment** *(new)* - Identify proposal risks

### Phase 3: Competitive Intelligence (Parallel)
10. **Competitor analysis.md** - Run parallel for each competitor

### Phase 4: Strategy Development
11. **Overall competitor analysis.md** *(needs content)* - Consolidate competitor insights
12. **Win themes.md** - Develop differentiated positioning

### Phase 5: Decision & Planning
13. **Resource Requirements** *(new)* - Estimate effort needed
14. **Go-no go.md** *(needs content)* - Make pursuit decision
15. **Executive Summary** *(new)* - Summarize for leadership

## Custom Command Structure

### Proposed Command: `rfp-analyze`

```bash
rfp-analyze [options]
```

### Options:
- `--input <path>` - Override default Input folder
- `--output <path>` - Override default Output folder
- `--competitors <list>` - Comma-separated competitor names
- `--themes <list>` - Pre-defined win themes to emphasize
- `--phase <1-5>` - Run specific phase only
- `--prompt <name>` - Run specific prompt only
- `--batch-size <n>` - For large requirement sets
- `--format <pdf|excel|word>` - Specify RFP format
- `--validate` - Run validation checks only
- `--resume` - Resume from last checkpoint

### State Management
Create `Output/.rfp-state.json` to track:
```json
{
  "session_id": "uuid",
  "started": "timestamp",
  "phase": 1,
  "completed_prompts": [],
  "user_inputs": {},
  "errors": [],
  "context": {}
}
```

## Recommended Next Steps

1. **Fill Empty Prompts**:
   - Design Pricing analysis prompt
   - Create Go/No-go decision framework
   - Build Overall competitor consolidation

2. **Create Missing Prompts**:
   - Opportunity Summary extractor
   - Risk Assessment analyzer
   - Resource Requirements estimator
   - Executive Summary generator

3. **Implement State Management**:
   - Design context passing between prompts
   - Add checkpoint/resume capability
   - Build error recovery

4. **Create Validation Framework**:
   - Output quality checks
   - Completeness validation
   - Cross-prompt consistency

5. **Build Custom Command**:
   - Implement `rfp-analyze` CLI
   - Add progress tracking
   - Enable parallel processing for competitors