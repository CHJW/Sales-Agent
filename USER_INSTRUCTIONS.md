# RFP Analysis Agent - User Instructions

## Quick Start (3 Steps)

### Step 1: Add RFP Documents
- Put **any** RFP files in the `Input/` folder
- Supported formats: **PDF, Word (.docx), Excel (.xlsx), Markdown (.md)**
- Can be any size - no token limits!

### Step 2: Run the Analysis
- Copy the contents of `rfp_analyze_starter.md` 
- Paste into Claude Code
- Answer the user questions when prompted (competitive vs sole-source, competitors, etc.)

### Step 3: Get Results
- Agent automatically processes everything
- Outputs appear in `output/` folder
- Complete analysis with extracts, competitor analysis, and recommendations

## What Happens Automatically

**You don't run any commands** - Claude handles everything:

✅ **Auto-detects** if vector database setup is needed  
✅ **Auto-converts** PDF/Word/Excel files to searchable text  
✅ **Auto-queries** relevant document sections for each analysis step  
✅ **Auto-processes** only relevant content (no token limits)  
✅ **Auto-generates** all required outputs  

## File Support

| Format | Support | Notes |
|--------|---------|-------|
| PDF | ✅ Full | Text extraction + tables |
| Word (.docx) | ✅ Full | Complete document processing |
| Excel (.xlsx) | ✅ Full | All sheets processed |
| Markdown (.md) | ✅ Full | Direct processing |
| Images (JPG/PNG) | 🔄 Future | OCR planned |

## Analysis Outputs

The agent generates:

### 📋 **Extraction Phase**
- `requirements_extract.md` - All requirements in structured tables
- `timeline_extract.md` - All dates, deadlines, and milestones
- `questions_extract.md` - Questions requiring responses
- `evaluation_extract.md` - Scoring criteria and selection process

### 📊 **Analysis Phase**  
- `pain_points_analysis.md` - Client challenges and pain points
- `inconsistency_analysis.md` - Document conflicts requiring clarification
- `win_themes.md` - Competitive positioning recommendations
- `competitor_[NAME].md` - Analysis for each competitor (if competitive bid)
- `pricing_[NAME].md` - Pricing strategy for each competitor

### 📈 **Summary Phase**
- `opportunity_overview.md` - Executive summary of opportunity
- `go_no_go_decision.md` - Bid recommendation with reasoning
- `executive_summary.md` - Complete analysis summary
- `overall_competitor_analysis.md` - Competitive landscape overview
- `overall_pricing_analysis.md` - Pricing strategy recommendations

## Key Benefits

🚫 **No Token Limits** - Process RFPs of any size  
⚡ **Faster Analysis** - Only relevant sections processed  
🎯 **Better Accuracy** - Semantic search finds related content  
📱 **Any File Type** - PDF, Word, Excel automatically handled  
🔄 **Same Workflow** - No learning curve, same prompts  
📍 **Source Tracing** - Every result linked to source document  

## Troubleshooting

### If Analysis Fails:
1. **Check Input Files** - Ensure files are in `Input/` folder
2. **Check Python** - Agent needs Python 3.x available
3. **Check Permissions** - Ensure write access to `output/` folder
4. **Check File Types** - Use supported formats (PDF, Word, Excel, MD)

### If Vector Setup Fails:
- Agent will auto-retry setup
- Large files may take a few minutes to process
- Check available disk space in `output/` folder

### For Large RFPs (100+ MB):
- Setup may take 2-3 minutes initially
- Subsequent analyses are fast (database cached)
- Consider breaking very large files into sections

## Advanced Usage

### Custom Search Terms:
If default queries don't capture your RFP content well:
1. Note which sections need better coverage
2. Modify the auto-execute commands in individual prompt files
3. Add your domain-specific keywords to the queries

### Competitive vs Sole-Source:
- **Competitive**: Full competitor analysis generated
- **Sole-Source**: Competitor analysis skipped, focus on win themes

### Multiple Competitors:
- List all known competitors when prompted
- Individual analysis generated for each
- Overall competitive summary provided

## Support

For issues or improvements:
- Check the `execution_debug_report.md` in output folder
- Review any error messages in Claude's response  
- Ensure all files are in supported formats
- Verify Python dependencies are available

---

**Ready to analyze unlimited-size RFPs with no token constraints! 🚀**