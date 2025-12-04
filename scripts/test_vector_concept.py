#!/usr/bin/env python3
"""
Simplified Vector Database Concept Test
Tests the chunking and retrieval logic without heavy dependencies
"""

import os
import re
import json
from pathlib import Path

def simple_text_similarity(text1, text2):
    """Simple word overlap similarity (substitute for embedding similarity)"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def detect_section_type(text):
    """Detect the type of section based on content"""
    text_lower = text.lower()
    
    # Keywords for different section types
    if any(keyword in text_lower for keyword in ['requirement', 'must', 'shall', 'mandatory', 'specification']):
        return 'requirements'
    elif any(keyword in text_lower for keyword in ['deadline', 'timeline', 'schedule', 'due date', 'milestone']):
        return 'timeline'
    elif any(keyword in text_lower for keyword in ['evaluation', 'scoring', 'criteria', 'selection', 'assessment']):
        return 'evaluation'
    elif any(keyword in text_lower for keyword in ['price', 'cost', 'budget', 'payment', 'fee']):
        return 'pricing'
    elif any(keyword in text_lower for keyword in ['technical', 'technology', 'system', 'architecture']):
        return 'technical'
    else:
        return 'general'

def simple_chunk_document(file_path, chunk_size=500):
    """Simple document chunking for testing"""
    print(f"📄 Processing: {os.path.basename(file_path)}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return []
    
    if not text.strip():
        print(f"⚠️  No text in {file_path}")
        return []
    
    chunks = []
    
    # Split by sections first (headers, numbered items, etc.)
    sections = re.split(r'\n\s*(?=\d+\.|\#\#?|\*\*|[A-Z][A-Z\s]+:)', text)
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
            
        # If section is small enough, keep as single chunk
        if len(section) <= chunk_size:
            chunks.append({
                'id': f"{os.path.basename(file_path)}_chunk_{len(chunks)}",
                'text': section.strip(),
                'metadata': {
                    'source_file': os.path.basename(file_path),
                    'section_type': detect_section_type(section),
                    'chunk_size': len(section),
                    'full_file_path': str(file_path)
                }
            })
        else:
            # Split large sections into smaller chunks
            words = section.split()
            chunk_words = chunk_size // 5  # Rough estimate: 5 chars per word
            
            for j in range(0, len(words), chunk_words):
                chunk_text = ' '.join(words[j:j + chunk_words])
                
                chunks.append({
                    'id': f"{os.path.basename(file_path)}_chunk_{len(chunks)}",
                    'text': chunk_text.strip(),
                    'metadata': {
                        'source_file': os.path.basename(file_path),
                        'section_type': detect_section_type(chunk_text),
                        'chunk_size': len(chunk_text),
                        'chunk_index': len(chunks),
                        'full_file_path': str(file_path)
                    }
                })
    
    print(f"✅ Created {len(chunks)} chunks from {os.path.basename(file_path)}")
    return chunks

def simple_vector_search(query, chunks, top_k=5):
    """Simple similarity search using word overlap"""
    print(f"🔍 Searching for: '{query}'")
    
    # Calculate similarity scores
    scored_chunks = []
    for chunk in chunks:
        similarity = simple_text_similarity(query, chunk['text'])
        scored_chunks.append((similarity, chunk))
    
    # Sort by similarity (descending)
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Return top k results
    results = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
    
    print(f"✅ Found {len(results)} relevant chunks")
    return results

def test_vector_concept(input_folder):
    """Test the vector database concept with RFP documents"""
    print("🚀 Testing Vector Database Concept...")
    
    # Find all files in input folder
    input_files = []
    for file_path in Path(input_folder).glob("*"):
        if file_path.is_file() and not file_path.name.startswith('.'):
            input_files.append(file_path)
    
    if not input_files:
        print(f"⚠️  No files found in {input_folder}")
        return False
    
    print(f"📂 Found {len(input_files)} files to process")
    
    # Process all files and create chunks
    all_chunks = []
    file_stats = {}
    
    for file_path in input_files:
        chunks = simple_chunk_document(file_path)
        all_chunks.extend(chunks)
        file_stats[str(file_path)] = len(chunks)
    
    print(f"\n📊 Chunking Summary:")
    print(f"   Total files: {len(input_files)}")
    print(f"   Total chunks: {len(all_chunks)}")
    
    # Show chunk distribution by section type
    section_counts = {}
    for chunk in all_chunks:
        section_type = chunk['metadata']['section_type']
        section_counts[section_type] = section_counts.get(section_type, 0) + 1
    
    print(f"   Chunks by section:")
    for section, count in section_counts.items():
        print(f"      {section}: {count}")
    
    # Test different queries
    test_queries = [
        "requirements specifications mandatory must have features",
        "deadline timeline schedule submission dates",
        "evaluation scoring criteria selection process",
        "pricing cost budget payment terms",
        "technical architecture system specifications"
    ]
    
    print(f"\n🧪 Testing Retrieval Queries:")
    
    for query in test_queries:
        print(f"\n" + "="*80)
        results = simple_vector_search(query, all_chunks, top_k=3)
        
        if results:
            print(f"📋 Top Results for '{query}':")
            for i, chunk in enumerate(results, 1):
                print(f"\n   {i}. Source: {chunk['metadata']['source_file']}")
                print(f"      Type: {chunk['metadata']['section_type']}")
                print(f"      Size: {chunk['metadata']['chunk_size']} chars")
                print(f"      Preview: {chunk['text'][:100]}...")
        else:
            print(f"   No relevant chunks found for '{query}'")
    
    # Save test results
    output_file = os.path.join(input_folder, '../output/vector_test_results.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            'test_summary': {
                'total_files': len(input_files),
                'total_chunks': len(all_chunks),
                'section_distribution': section_counts,
                'file_stats': file_stats
            },
            'sample_chunks': all_chunks[:5],  # Save first 5 chunks as samples
            'test_queries': test_queries
        }, f, indent=2)
    
    print(f"\n💾 Test results saved to: {output_file}")
    print(f"✅ Vector concept test completed successfully!")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python test_vector_concept.py <input_folder>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    
    if not os.path.exists(input_folder):
        print(f"❌ Input folder not found: {input_folder}")
        sys.exit(1)
    
    success = test_vector_concept(input_folder)
    if not success:
        sys.exit(1)