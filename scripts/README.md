# Scripts Directory

This folder contains all Python automation scripts for the RFP Analysis Agent. These scripts are **auto-executed by Claude** - users don't run them directly.

## 🔧 Core Scripts

### `setup_vector_db.py`
**Purpose**: Creates vector database from RFP documents  
**Auto-executed**: When `./output/.vector_ready` doesn't exist  
**Function**: Converts any file type (PDF, Word, Excel, MD) to searchable chunks
```bash
# Auto-executed by agent
python3 scripts/setup_vector_db.py --input="./Input" --output="./output"
```

### `vector_query.py` 
**Purpose**: Retrieves relevant chunks for analysis  
**Auto-executed**: Before each extraction/analysis prompt  
**Function**: Semantic search to find targeted content
```bash
# Auto-executed by agent for each prompt type
python3 scripts/vector_query.py --query="requirements specifications" --section="requirements" --top_k=15
```

### `vector_query_templates.py`
**Purpose**: Dynamic query generation  
**Usage**: Customize search terms for different RFP types  
**Function**: Generates optimized queries for various analysis categories
```bash
# Generate custom query
python3 scripts/vector_query_templates.py requirements --terms "SOW deliverables acceptance"
```

## 🧪 Testing Scripts

### `test_vector_concept.py`
**Purpose**: Validates vector database functionality without heavy dependencies  
**Usage**: Test document processing and retrieval  
**Function**: Simulates vector operations with word similarity
```bash
python3 scripts/test_vector_concept.py ./Input
```

### `test_auto_execution.py`  
**Purpose**: Validates complete auto-execution workflow  
**Usage**: Verify all command paths and integration  
**Function**: Simulates full agent workflow execution
```bash
python3 scripts/test_auto_execution.py
```

### `demo_vector_workflow.py`
**Purpose**: Demonstrates capabilities and benefits  
**Usage**: Show system features and performance  
**Function**: Educational demo of vector integration
```bash
python3 scripts/demo_vector_workflow.py
```

## 🔗 Integration with Prompts

All prompts automatically reference these scripts:

### Extraction Prompts
- `Requirements Prompt.md` → `vector_query.py` (requirements chunks)
- `Timeline Prompt.md` → `vector_query.py` (timeline chunks)  
- `Questions Prompt.md` → `vector_query.py` (question chunks)
- `Evaluation Prompt.md` → `vector_query.py` (evaluation chunks)

### Analysis Prompts
- `Pain points Prompt.md` → `vector_query.py` (challenge chunks)
- `Inconsistency Prompt.md` → `vector_query.py` (conflict chunks)
- `Win themes Prompt.md` → `vector_query.py` (competitive chunks)
- `Pricing Prompt.md` → `vector_query.py` (pricing chunks)

## 📋 Script Dependencies

### Auto-Installed Libraries
```python
# Vector database and ML
chromadb>=1.3.0
sentence-transformers>=2.0.0
torch>=1.11.0

# Document processing
PyPDF2>=3.0.0
python-docx>=1.0.0
pandas>=1.5.0
openpyxl>=3.0.0
```

### Installation (Automatic)
Scripts auto-install dependencies when first run:
```python
def install_dependencies():
    os.system("pip install --break-system-packages chromadb sentence-transformers PyPDF2 python-docx pandas openpyxl")
```

## ⚙ Configuration

### Vector Database Settings
- **Embedding Model**: `all-mpnet-base-v2`
- **Chunk Size**: 500-1000 characters  
- **Chunk Overlap**: 200 characters
- **Default Retrieval**: 10-15 chunks per query

### Query Templates
Located in `vector_query_templates.py`:
```python
QUERY_TEMPLATES = {
    'requirements': {
        'primary': "requirements specifications mandatory must have features",
        'alternatives': ["technical functional requirements", "compliance specifications"],
        'section_filter': 'requirements'
    }
    # ... additional templates
}
```

## 🐛 Troubleshooting

### Script Execution Issues
```bash
# Check Python availability
which python3

# Test script accessibility  
python3 scripts/test_vector_concept.py --help

# Verify dependencies
python3 -c "import chromadb; print('Dependencies OK')"
```

### Common Solutions
- **Permission errors**: Ensure write access to `output/` folder
- **Import errors**: Scripts auto-install dependencies on first run
- **Path errors**: All references updated to use `scripts/` prefix

## 📈 Performance

### Benchmarks
- **Setup Time**: 1-3 minutes for 100MB+ RFPs (one-time)
- **Query Speed**: Sub-second retrieval of relevant chunks
- **Memory Usage**: ~500MB during processing, ~50MB cached
- **Storage**: ~10MB vector database per 100MB documents

---

**All scripts are designed for automatic execution by Claude. Users interact only with the main `rfp_analyze_starter.md` prompt.**