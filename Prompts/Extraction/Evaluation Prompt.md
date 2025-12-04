## Auto-Execute Vector Query (Agent Instructions)

**BEFORE PROCESSING - AUTO-EXECUTE THIS COMMAND:**
```bash
python3 scripts/vector_query.py --query="evaluation scoring criteria selection process assessment" --section="evaluation" --top_k=12 --output="temp_evaluation_context.md"
```

**INPUT:** Use contents of `temp_evaluation_context.md` instead of full RFP documents

---

TASK: Extract evaluation/marking criteria from the retrieved evaluation chunks and provide strategic insights.

EXTRACT (preserve original structure and terminology):

1. SCORING/MARKING CRITERIA
   - Extract as-is: categories, weights, points, scales
   - Preserve section references
   - Use table format matching source document

2. MANDATORY/PASS-FAIL REQUIREMENTS
   - Requirements that must be met to qualify
   - Section references

3. SELECTION PROCESS (if stated)
   - Stages, timeline, decision points

OUTPUT FORMAT:
- Mirror source document structure where possible
- Use tables if source uses tables
- "Not specified" for absent elements — do not infer

OUTPUT: Save as "evaluation_extract.md" in the output folder.
Note at end: "Extracted from [X] vector chunks covering evaluation and selection criteria"

STRATEGIC INSIGHTS (add at end):
- Where is the weight concentrated? (technical vs price vs experience)
- Any unusual weightings or criteria?
- What does this reveal about client priorities?
- Red flags or areas needing clarification?