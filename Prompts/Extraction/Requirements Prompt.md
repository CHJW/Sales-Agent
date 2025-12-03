## Task
Extract all requirements from the attached RFP/RFI document(s) into a structured table.

## Pre-Check (Complete First)
1. Scan document(s) and estimate total requirement count
2. Identify terminology used (e.g., "requirements", "specifications", "criteria", "deliverables")
3. Identify existing table structure/columns in source document
4. If estimated requirements > 50: STOP and recommend section-by-section batching with section list

## Output Format
OUTPUT: Save as "Requirements.md" in the output folder.
Excel-compatible table that:

**Step 1 — Mirror Source Structure**
- Replicate ALL columns exactly as they appear in RFP
- Preserve all original data, wording, and formatting
- Do not paraphrase or summarize any field

**Step 2 — Add Standard Columns (if not already present)**
| Column | Add If Missing | Values |
|--------|----------------|--------|
| Req_ID | If no unique identifier exists | Generate sequential (R001, R002...) |
| Type | If not indicated | Mandatory / Desirable / Optional / Unspecified |
| Category | If not indicated | Technical / Commercial / Compliance / Operational / Other |

## Rules
- Extract ALL requirements including optional/desirable
- Preserve original wording exactly — do not paraphrase
- If source has columns not listed above, KEEP THEM
- If type/category ambiguous, use best fit
- After output, state: 
  - "Source columns: [list]"
  - "Added columns: [list]"
  - "Total: [X] requirements extracted. Verify count against source."

## Batch Mode (If Recommended)
Provide section list for user to specify which section(s) to process per iteration.