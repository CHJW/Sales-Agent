Extract all dates and deadlines from this RFP into categorised tables.

REQUIRED CATEGORIES (always include):
1. RFP Process — submission, Q&A, briefings, addenda, offer validity, award
2. Contract Terms — term, extensions, start date, maximum duration

DYNAMIC CATEGORIES (include only if dates exist):
- Generate additional categories based on content (e.g., Transition-In, Ongoing Obligations, Historical, SLAs)
- Name categories descriptively based on the RFP content
- Omit any category with no dates

TABLE FORMAT (for each category):

### [Category Name]
| Date | Event/Milestone | Day Type | Source (page/section) | Notes |
|------|-----------------|----------|----------------------|-------|

COLUMN RULES:
- Date formats:
  - Explicit with time: HHMM D Mon YYYY (e.g., 1700 17 Dec 2025)
  - Explicit date only: D Mon YYYY (e.g., 22 Dec 2025)
  - Relative: [Trigger] + X [BD/CD] (e.g., Start Date + 90 BD, Award + 14 CD)
- Day Type: Calendar | Business | Unspecified
- Notes: Only if ambiguity, condition, or exception — leave blank if straightforward

ABBREVIATIONS:
- BD = Business Days
- CD = Calendar Days

Sort each table by date ascending (explicit dates first, then relative).

OUTPUT:
- Save as "Timelines.md" in the output folder.
- Tables only. No introduction, no summary, no commentary between tables.