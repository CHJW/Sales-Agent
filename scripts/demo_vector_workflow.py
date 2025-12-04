#!/usr/bin/env python3
"""
Demo: Vector-Enhanced RFP Analysis Workflow
Shows how vector database integration works with existing prompts
"""

import os
import sys
from pathlib import Path

def demo_vector_workflow():
    """Demonstrate the complete vector-enhanced workflow"""
    
    print("🚀 Vector-Enhanced RFP Analysis Demo")
    print("="*60)
    
    # Step 1: Check existing setup
    print("\n📂 Step 1: Check Current Setup")
    input_files = list(Path("./Input").glob("*"))
    input_files = [f for f in input_files if f.is_file()]
    
    print(f"   Found {len(input_files)} RFP documents:")
    for file in input_files[:5]:  # Show first 5
        print(f"      - {file.name}")
    if len(input_files) > 5:
        print(f"      ... and {len(input_files) - 5} more")
    
    # Step 2: Vector Database Setup
    print("\n🔧 Step 2: Vector Database Setup")
    vector_ready = Path("./output/.vector_ready").exists()
    
    if vector_ready:
        print("   ✅ Vector database already exists")
    else:
        print("   🔄 Would run: python3 setup_vector_db.py --input='./Input' --output='./output'")
        print("   📝 This creates semantic chunks from all RFP documents")
    
    # Step 3: Show chunking results from test
    print("\n📊 Step 3: Document Chunking Results")
    try:
        import json
        with open("./output/vector_test_results.json", "r") as f:
            data = json.load(f)
        
        stats = data["test_summary"]
        print(f"   📄 Total chunks created: {stats['total_chunks']}")
        print(f"   📂 From {stats['total_files']} documents")
        print(f"   📋 Chunk distribution:")
        
        for section, count in stats["section_distribution"].items():
            print(f"      • {section}: {count} chunks")
            
    except FileNotFoundError:
        print("   ⚠️  Run test_vector_concept.py first to see chunking results")
    
    # Step 4: Query Demonstration
    print("\n🔍 Step 4: Smart Query Examples")
    
    queries = {
        "Requirements": "requirements specifications mandatory must have features criteria",
        "Timeline": "deadline timeline schedule submission dates milestones",
        "Evaluation": "evaluation scoring criteria selection process assessment",
        "Pricing": "pricing cost budget payment terms commercial",
        "Technical": "technical architecture system specifications infrastructure"
    }
    
    for category, query in queries.items():
        print(f"\n   🎯 {category} Analysis:")
        print(f"      Query: '{query}'")
        print(f"      Command: python3 vector_query.py --query=\"{query}\" --section=\"{category.lower()}\" --top_k=10")
        print(f"      Result: Retrieves most relevant {category.lower()} chunks (manageable size)")
    
    # Step 5: Integration Benefits
    print("\n✨ Step 5: Vector Integration Benefits")
    
    benefits = [
        "🚫 No token limits - handles unlimited RFP size",
        "⚡ Faster processing - only relevant chunks analyzed", 
        "🎯 Better accuracy - semantic search finds related content",
        "📍 Source tracing - each result linked to original document",
        "🔄 Same prompts - existing workflow unchanged",
        "📱 Any file type - PDFs, Word, Excel → auto-converted"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")
    
    # Step 6: Workflow Comparison
    print(f"\n📊 Step 6: Before vs After Comparison")
    print(f"   {'Aspect':<20} {'Before (Full Docs)':<25} {'After (Vector DB)':<25}")
    print(f"   {'-'*20} {'-'*25} {'-'*25}")
    print(f"   {'Max RFP Size':<20} {'Limited by tokens':<25} {'Unlimited':<25}")
    print(f"   {'Processing Time':<20} {'Slow (large docs)':<25} {'Fast (relevant chunks)':<25}")
    print(f"   {'Accuracy':<20} {'Good':<25} {'Better (semantic)':<25}")
    print(f"   {'Setup':<20} {'None':<25} {'One-time chunking':<25}")
    print(f"   {'File Support':<20} {'Markdown only':<25} {'PDF/Word/Excel/MD':<25}")
    
    # Step 7: Usage Instructions
    print(f"\n📖 Step 7: How to Use")
    print(f"   1. Put any RFP files in ./Input/ folder")
    print(f"   2. Run: python3 setup_vector_db.py --input='./Input' --output='./output'")
    print(f"   3. Use modified prompts (they auto-query vector DB)")
    print(f"   4. Enjoy unlimited RFP processing! 🎉")
    
    print(f"\n✅ Demo Complete!")
    
    return True

if __name__ == "__main__":
    try:
        demo_vector_workflow()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)