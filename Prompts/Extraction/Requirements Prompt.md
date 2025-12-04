## Input Preparation (Vector Database Retrieval)

**BEFORE PROCESSING:** Retrieve relevant requirement chunks from vector database:

### Step 0: Check for Vector Database
```bash
# Check if vector database exists
if [ -f "./output/.vector_ready" ]; then
    echo "✅ Using existing vector database"
else
    echo "🔄 Setting up vector database..."
    python3 scripts/setup_vector_db.py --input="./Input" --output="./output"
fi
```

### Step 1: Query Requirements Content
```bash
# Retrieve requirement-focused chunks instead of processing entire documents
python3 scripts/vector_query.py \
    --query="requirements specifications mandatory must have features criteria deliverables" \
    --db="./output/.vector_db" \
    --section="requirements" \
    --top_k=15 \
    --output="temp_requirements_context.md"
```

### Step 2: Use Retrieved Content as Input
**INPUT TEXT:** [Contents of temp_requirements_context.md - the most relevant requirement chunks]

---

## Task
Extract all requirements from the retrieved RFP requirement chunks into a structured table.

## Pre-Check (Complete First)
1. Review retrieved chunks and estimate total requirement count
2. Identify terminology used (e.g., "requirements", "specifications", "criteria", "deliverables")
3. Identify existing table structure/columns in source chunks
4. If estimated requirements > 50: Request broader retrieval or section filtering

## Output Format
OUTPUT: Save as "requirements_extract.md" in the output folder.
Excel-compatible table that:

**Step 1 — Mirror Source Structure**
- Replicate ALL columns exactly as they appear in RFP chunks
- Preserve all original data, wording, and formatting
- Do not paraphrase or summarize any field

**Step 2 — Add Standard Columns (if not already present)**
| Column | Add If Missing | Values |
|--------|----------------|--------|
| Req_ID | If no unique identifier exists | Generate sequential (R001, R002...) |
| Type | If not indicated | Mandatory / Desirable / Optional / Unspecified |
| Category | If not indicated | Technical / Commercial / Compliance / Operational / Other |
| Source_Chunk | Always add | Reference to source chunk for traceability |

## Rules
- Extract ALL requirements including optional/desirable from retrieved chunks
- Preserve original wording exactly — do not paraphrase
- If source has columns not listed above, KEEP THEM
- If type/category ambiguous, use best fit
- Add source chunk reference for each requirement for traceability
- After output, state: 
  - "Retrieved chunks: [X] chunks processed"
  - "Source columns: [list]"
  - "Added columns: [list]"
  - "Total: [X] requirements extracted from vector search"

## Vector Benefits
- **Focused Processing:** Only relevant requirement sections processed
- **No Token Limits:** Handles large RFPs by retrieving manageable chunks
- **Better Accuracy:** Semantic search finds requirements across document structure
- **Source Tracing:** Each requirement linked back to specific document chunks

## Fallback Mode
If vector database unavailable, process full documents as before:
- Use entire Input folder contents
- Follow original extraction rules
- Note: "Processed full documents (vector DB unavailable)"