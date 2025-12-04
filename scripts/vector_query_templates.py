#!/usr/bin/env python3
"""
Dynamic Vector Query Generator
Creates flexible, context-aware queries for RFP analysis
"""

import os
import argparse

# Base query templates with alternatives
QUERY_TEMPLATES = {
    'requirements': {
        'primary': "requirements specifications mandatory must have features criteria deliverables",
        'alternatives': [
            "shall should may requirements compliance specifications",
            "mandatory optional desired features functionality capabilities", 
            "technical functional non-functional requirements constraints",
            "deliverables outputs expectations outcomes objectives"
        ],
        'section_filter': 'requirements'
    },
    
    'timeline': {
        'primary': "deadline timeline schedule submission dates milestones",
        'alternatives': [
            "schedule timing calendar phases stages",
            "deadlines due dates cutoff submission timeline",
            "milestones phases deliveries implementation schedule",
            "duration timeframe period project timeline"
        ],
        'section_filter': 'timeline'
    },
    
    'evaluation': {
        'primary': "evaluation scoring criteria selection process assessment",
        'alternatives': [
            "scoring weighting points evaluation methodology",
            "selection criteria assessment evaluation framework", 
            "scoring rubric evaluation matrix assessment criteria",
            "comparative evaluation selection process methodology"
        ],
        'section_filter': 'evaluation'
    },
    
    'pricing': {
        'primary': "pricing cost budget payment commercial terms",
        'alternatives': [
            "cost price budget financial commercial",
            "payment terms invoicing billing costs",
            "commercial pricing structure cost model",
            "budget allocation financial requirements costs"
        ],
        'section_filter': 'pricing'
    },
    
    'technical': {
        'primary': "technical architecture system specifications infrastructure",
        'alternatives': [
            "technology technical architecture design specifications",
            "system infrastructure platform technical requirements",
            "technical specifications implementation architecture",
            "technology stack infrastructure technical design"
        ],
        'section_filter': 'technical'
    },
    
    'questions': {
        'primary': "questions inquiries clarifications RFI responses",
        'alternatives': [
            "questions inquiries clarifications queries requests",
            "RFI requests information clarification questions",
            "inquiries clarifications questions responses answers",
            "questions concerns clarifications information requests"
        ],
        'section_filter': None  # Questions can be in any section
    },
    
    'competitors': {
        'primary': "competitors competition competitive analysis comparison",
        'alternatives': [
            "competitive analysis competitor comparison market",
            "competition competitive landscape market analysis",
            "competitors competitive positioning market share",
            "competitive intelligence market competitors analysis"
        ],
        'section_filter': None
    },
    
    'pain_points': {
        'primary': "challenges issues concerns problems difficulties",
        'alternatives': [
            "problems issues challenges concerns difficulties",
            "pain points problems challenges issues risks",
            "concerns difficulties challenges problems obstacles",
            "issues risks problems concerns challenges"
        ],
        'section_filter': None
    },
    
    'win_themes': {
        'primary': "competitive advantage themes positioning differentiation",
        'alternatives': [
            "competitive advantage differentiation positioning strengths",
            "value proposition competitive themes advantages",
            "differentiation competitive positioning unique value",
            "competitive strengths advantages themes positioning"
        ],
        'section_filter': None
    },
    
    'inconsistencies': {
        'primary': "inconsistencies conflicts contradictions discrepancies",
        'alternatives': [
            "inconsistencies contradictions conflicts discrepancies",
            "conflicts contradictions inconsistent discrepancies",
            "discrepancies inconsistencies conflicts contradictions",
            "contradictions conflicts inconsistent information"
        ],
        'section_filter': None
    }
}

def generate_query_command(category, custom_terms=None, top_k=10, include_alternatives=False):
    """Generate dynamic vector query command"""
    
    if category not in QUERY_TEMPLATES:
        available = ", ".join(QUERY_TEMPLATES.keys())
        raise ValueError(f"Unknown category '{category}'. Available: {available}")
    
    template = QUERY_TEMPLATES[category]
    
    # Build query
    if custom_terms:
        # User provided custom terms
        query = " ".join(custom_terms)
    else:
        # Use primary template
        query = template['primary']
        
        # Optionally add alternatives for broader search
        if include_alternatives:
            for alt in template['alternatives'][:2]:  # Add first 2 alternatives
                query += f" {alt}"
    
    # Build command
    cmd_parts = [
        "python3 vector_query.py",
        f'--query="{query}"',
        f"--top_k={top_k}",
        f'--output="temp_{category}_context.md"'
    ]
    
    # Add section filter if specified
    if template['section_filter']:
        cmd_parts.insert(-1, f'--section="{template["section_filter"]}"')
    
    return " ".join(cmd_parts)

def generate_prompt_header(category, custom_terms=None, top_k=10):
    """Generate the vector retrieval header for any prompt"""
    
    query_cmd = generate_query_command(category, custom_terms, top_k)
    
    header = f"""## Input Preparation (Vector Database Retrieval)

**BEFORE PROCESSING:** Retrieve relevant {category} chunks from vector database:

### Step 0: Check for Vector Database
```bash
# Check if vector database exists
if [ -f "./output/.vector_ready" ]; then
    echo "✅ Using existing vector database"
else
    echo "🔄 Setting up vector database..."
    python3 setup_vector_db.py --input="./Input" --output="./output"
fi
```

### Step 1: Query {category.title()} Content
```bash
# Retrieve {category}-focused chunks instead of processing entire documents
{query_cmd}
```

### Step 2: Use Retrieved Content as Input
**INPUT TEXT:** [Contents of temp_{category}_context.md - the most relevant {category} chunks]

### Optional: Expand Search (if insufficient results)
```bash
# If initial query returns insufficient content, try broader search:"""

    # Add alternative queries
    if category in QUERY_TEMPLATES:
        for i, alt_query in enumerate(QUERY_TEMPLATES[category]['alternatives'][:2], 1):
            alt_cmd = generate_query_command(category, alt_query.split(), top_k)
            header += f"""
# Alternative {i}: {alt_query}
{alt_cmd}"""

    header += f"""
```

---
"""
    return header

def main():
    parser = argparse.ArgumentParser(description='Generate dynamic vector queries')
    parser.add_argument('category', choices=list(QUERY_TEMPLATES.keys()), 
                       help='Analysis category')
    parser.add_argument('--terms', nargs='+', help='Custom search terms (overrides template)')
    parser.add_argument('--top_k', type=int, default=10, help='Number of chunks to retrieve')
    parser.add_argument('--alternatives', action='store_true', help='Include alternative queries')
    parser.add_argument('--header', action='store_true', help='Generate full prompt header')
    
    args = parser.parse_args()
    
    if args.header:
        print(generate_prompt_header(args.category, args.terms, args.top_k))
    else:
        print(generate_query_command(args.category, args.terms, args.top_k, args.alternatives))

if __name__ == "__main__":
    main()