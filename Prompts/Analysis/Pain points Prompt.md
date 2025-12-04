## Auto-Execute Vector Query (Agent Instructions)

**BEFORE PROCESSING - AUTO-EXECUTE THIS COMMAND:**
```bash
python3 scripts/vector_query.py --query="challenges issues concerns problems difficulties" --top_k=15 --output="temp_pain_points_context.md"
```

**INPUT:** Use contents of `temp_pain_points_context.md` instead of full RFP documents

---

Analyse the retrieved RFP chunks for buyer pain points.

Pain points may appear as: challenges, desired outcomes, business objectives, project drivers, success criteria, or embedded in requirements. Invert positive framing (e.g., "improve efficiency" → current inefficiency is a pain point).

OUTPUT: Save as "pain_points_analysis.md" in the output folder.
Note at end: "Analyzed from [X] vector chunks covering pain points and challenges"
Output in two sections:

## 1. EXPLICIT PAIN POINTS
Pain points directly stated or clearly implied by objectives/outcomes.
| Pain Point | Evidence (quote/reference) | Section/Page | Reinforcement Signals |
|------------|---------------------------|--------------|----------------------|

## 2. IMPLICIT PAIN POINTS (INFERRED)
Pain points inferred from context, requirements, tone, or linguistic patterns. Go beyond content — examine HOW things are written, not just WHAT is written.
| Pain Point | Signal Type | Evidence | Reasoning | Confidence |
|------------|-------------|----------|-----------|------------|

Signal types to examine:
- REPETITION: Concepts/terms appearing 3+ times across sections
- EMPHASIS: "Must", "critical", "essential", "mandatory" language
- SPECIFICITY: Unusually detailed requirements (over-specification)
- TONE SHIFT: Formal language becoming emphatic or cautionary
- SECTION WEIGHT: Disproportionate length/detail vs other sections
- QUALIFYING LANGUAGE: Heavy caveats, double-negatives, conditional phrasing
- KNOWLEDGE GAPS: RFP asks vendors to "explain approach" or "describe methodology"
- VAGUENESS: Deliberately ambiguous areas (may indicate internal disagreement)

Guidelines:
- Explicit: Direct quotes or paraphrased facts only. Cite location. Note reinforcement signals if present (e.g., "REPETITION: mentioned 4x", "EMPHASIS: marked as mandatory").
- Implicit: State the signal type, provide specific evidence (quote or cite), explain reasoning for why this signal suggests the pain point.
- Flag confidence level: High/Medium/Low.
- Flag when implicit pain points reinforce explicit pain points (strong priority indicator).
- Prioritise accuracy over volume.

