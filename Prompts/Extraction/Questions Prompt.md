## Auto-Execute Vector Query (Agent Instructions)

**BEFORE PROCESSING - AUTO-EXECUTE THIS COMMAND:**
```bash
python3 scripts/vector_query.py --query="questions inquiries clarifications RFI responses" --top_k=12 --output="temp_questions_context.md"
```

**INPUT:** Use contents of `temp_questions_context.md` instead of full RFP documents

---

TASK: Extract all questions, requirements, and response items from the retrieved question chunks.

DEFINITIONS:
- "Response Item" = Anything requiring vendor input, including:
  - Direct questions (e.g., "Describe your approach to...")
  - Numbered requirements (e.g., "3.1.2 Vendor shall provide...")
  - Table cells expecting input (compliance matrices, pricing tables)
  - Implicit asks phrased as statements (e.g., "Experience in federal contracts is required")
  - Pricing requests (rates, totals, fee structures, cost breakdowns)
  - Legal/contractual items (certifications, representations, T&C acceptance, insurance)

CATEGORY TAGS:
- TECHNICAL — Solution, approach, methodology, experience
- PRICING — Rates, costs, fees, pricing models, payment terms
- LEGAL — Certifications, compliance, T&Cs, insurance, liability, reps & warranties
- ADMIN — Company info, references, formatting requirements
- ATTACHMENT — Documents to be submitted separately

EXTRACTION RULES:
1. Preserve original IDs/numbering exactly (e.g., "Question 5", "SEC001", row numbers)
2. If no ID exists, generate: [FileAbbrev]-[Section]-[Seq] (e.g., "PartD-Design-001")
3. For Excel: Each row requiring input = separate item; note sheet name + row
4. For tables: Extract requirement text AND constraints from adjacent columns
5. Include section/page/sheet reference for traceability
6. For pricing tables: Capture structure, units, and note any formulas expected
7. For legal/security items: Flag if signature/certification required vs informational
8. For multi-part questions with sub-bullets: Keep as single item, count sub-parts in Notes
9. For cross-references (e.g., "see Annexure D"): Flag with [XREF: target] in Notes

OUTPUT FORMAT:
| ID | Category | Source Location | Requirement/Question Text | Response Type | Constraints | Notes |
|----|----------|-----------------|---------------------------|---------------|-------------|-------|

RESPONSE TYPE VALUES:
- Narrative (open text)
- Yes/No
- Numeric (pricing, quantities, percentages)
- Selection (pick from options)
- Attachment (doc upload required)
- Table (structured response in template)
- Signature (requires authorised signatory)

CONSTRAINTS COLUMN (capture if specified):
- Word/page limits (e.g., "1,000 words max")
- Required sub-components (e.g., "must include 3 case studies")
- Format requirements (e.g., "use provided template")

HANDLING MULTIPLE FILES:
- Process each file sequentially
- Prefix IDs with filename abbreviation
- Flag cross-references between documents

PRIORITY FLAGS (add to Notes):
- [MANDATORY] — Explicitly marked required or "M"
- [SCORED] — Evaluation criteria item
- [PASS/FAIL] — Compliance gate
- [DESIRABLE] — Marked "Highly Desirable" or "HD"
- [CONDITIONAL] — Only applies in certain scenarios
- [XREF: filename] — References another document
- [n SUB-PARTS] — Multi-part question with n bullets

Be exhaustive. Include everything requiring vendor response, even if uncertain—flag uncertain items in Notes.

OUTPUT: Save as "questions_extract.md" in the output folder.
Note at end: "Extracted from [X] vector chunks covering questions and response requirements"