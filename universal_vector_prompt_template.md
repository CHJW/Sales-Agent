# Universal Vector-Enhanced Prompt Template

## How to Use This Template

**For any RFP analysis prompt:**

1. **Replace `{CATEGORY}`** with your analysis type: requirements, timeline, evaluation, pricing, technical, questions, competitors, pain_points, win_themes, inconsistencies

2. **Customize search terms** by running:
   ```bash
   python3 scripts/vector_query_templates.py {CATEGORY} --terms "your custom words here" --top_k=15
   ```

3. **Use generated header** in your prompt:
   ```bash
   python3 scripts/vector_query_templates.py {CATEGORY} --header > temp_header.md
   ```

---

## Universal Template:

```markdown
## Input Preparation (Vector Database Retrieval)

**BEFORE PROCESSING:** Retrieve relevant {CATEGORY} chunks from vector database:

### Step 0: Check for Vector Database
```bash
if [ -f "./output/.vector_ready" ]; then
    echo "✅ Using existing vector database"  
else
    echo "🔄 Setting up vector database..."
    python3 scripts/setup_vector_db.py --input="./Input" --output="./output"
fi
```

### Step 1: Query {CATEGORY} Content  
```bash
# Generate dynamic query based on your needs:
python3 scripts/vector_query_templates.py {CATEGORY} --top_k=10

# OR with custom terms:
python3 scripts/vector_query_templates.py {CATEGORY} --terms "your specific keywords here" --top_k=15

# OR with alternatives for broader search:
python3 scripts/vector_query_templates.py {CATEGORY} --alternatives --top_k=20
```

### Step 2: Execute Generated Query
```bash
# Copy and run the generated command, for example:
python3 scripts/vector_query.py --query="your generated query" --section="{section}" --top_k=10 --output="temp_{CATEGORY}_context.md"
```

### Step 3: Use Retrieved Content as Input
**INPUT TEXT:** [Contents of temp_{CATEGORY}_context.md]

---

## [Your Original Prompt Content Here]

## Additional Vector Benefits:
- **Flexible Queries:** Adapt search terms for specific RFPs
- **Expandable Results:** Increase `top_k` for more context  
- **Section Filtering:** Focus on specific document sections
- **Source Tracing:** Each result links back to original chunks
```

## Pre-built Query Examples:

### Requirements Analysis:
```bash
# Basic requirements
python3 scripts/vector_query_templates.py requirements

# Compliance focused  
python3 scripts/vector_query_templates.py requirements --terms "mandatory compliance must shall"

# Technical requirements
python3 scripts/vector_query_templates.py requirements --terms "technical specifications system requirements"
```

### Timeline Analysis:
```bash
# Standard timeline
python3 scripts/vector_query_templates.py timeline

# Implementation focused
python3 scripts/vector_query_templates.py timeline --terms "implementation deployment go-live phases"

# Deadline focused
python3 scripts/vector_query_templates.py timeline --terms "deadline submission due date cutoff"
```

### Pricing Analysis:
```bash
# General pricing  
python3 scripts/vector_query_templates.py pricing

# Cost structure
python3 scripts/vector_query_templates.py pricing --terms "cost structure pricing model rates"

# Payment terms
python3 scripts/vector_query_templates.py pricing --terms "payment terms invoicing billing"
```

## Benefits of Dynamic Queries:

✅ **Adaptable** - Customize for any RFP type or industry  
✅ **Expandable** - Add more search terms as needed  
✅ **Contextual** - Different queries for different analysis depths  
✅ **Intelligent** - Built-in alternatives for comprehensive coverage  
✅ **Traceable** - Source links maintained for verification