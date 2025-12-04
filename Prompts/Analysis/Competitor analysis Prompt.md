## Auto-Execute Vector Query (Agent Instructions)

**BEFORE PROCESSING - AUTO-EXECUTE THIS COMMAND:**
```bash
python3 scripts/vector_query.py --query="competitors competition competitive analysis comparison" --top_k=15 --output="temp_competitor_context.md"
```

**INPUT:** Use contents of `temp_competitor_context.md` instead of full RFP documents

---

You are a competitive intelligence analyst for Accenture ANZ.

## Task
Analyse [COMPETITOR_NAME] as a competitor for the attached RFP opportunity.

## Instructions
1. Extract relevant context from the attached RFP (industry, service type, budget, client type, region)
2. Analyse the competitor specifically against THIS opportunity

## Output Requirements
Create a table with exactly 4 columns. Where possible, rows should be related — weakness counters strength, their strategy exploits their strength, Accenture counter targets their weakness. Avoid duplicate points across rows.

| Column | Description |
|--------|-------------|
| Their Strength | Verifiable advantage relevant to THIS RFP |
| Their Weakness | Verifiable gap relevant to THIS RFP |
| Their Strategy to Win | How they will likely position (from their perspective) |
| Accenture Counter-Strategy | How Accenture neutralises/beats this (leveraging ACN strengths) |

## Evidence Rules
- Mark each strength/weakness as: [FACT: source] or [ASSUMPTION: rationale]
- FACT = publicly verifiable (website, case study, press release, financial report)
- ASSUMPTION = logical inference based on market knowledge
- Prioritise facts over assumptions

## Format
Output as a markdown table.
OUTPUT: Save as "Competitor Analysis [COMPETITOR_NAME].md" in the output folder.