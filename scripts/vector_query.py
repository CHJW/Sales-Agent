#!/usr/bin/env python3
"""
RFP Vector Query Script
Retrieves relevant chunks from vector database for RFP analysis
"""

import os
import sys
import argparse
import json
import hashlib
import time
from datetime import datetime

def get_query_debug_info(query_hash, query, chunk_count, total_time, db_time, model_time, search_time, section_filter=None):
    """Generate debug information for vector query"""
    return {
        'query_id': query_hash,
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'section_filter': section_filter,
        'results': {
            'chunks_found': chunk_count,
            'total_time_seconds': round(total_time, 3),
            'db_connection_time': round(db_time, 3),
            'model_load_time': round(model_time, 3),
            'search_time': round(search_time, 3)
        },
        'performance': {
            'chunks_per_second': round(chunk_count / total_time, 2) if total_time > 0 else 0,
            'search_efficiency': 'fast' if search_time < 0.1 else 'moderate' if search_time < 0.5 else 'slow'
        }
    }

def query_rfp_database(query, db_path, top_k=10, section_filter=None, enable_debug=True):
    """Query the RFP vector database for relevant chunks with caching debug info"""
    start_time = time.time()
    query_hash = hashlib.md5(f"{query}_{top_k}_{section_filter}".encode()).hexdigest()[:8]
    
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("🚨 Dependencies not found. Run setup_vector_db.py first.")
        sys.exit(1)
    
    if not os.path.exists(db_path):
        print(f"❌ Vector database not found at {db_path}")
        print("Run setup_vector_db.py first to create the database.")
        sys.exit(1)
    
    if enable_debug:
        print(f"🔍 [VECTOR-{query_hash}] Querying: '{query}'")
        print(f"📊 [VECTOR-{query_hash}] Filters: top_k={top_k}, section={section_filter}")
    
    # Connect to database
    db_connect_start = time.time()
    client = chromadb.PersistentClient(path=db_path)
    try:
        collection = client.get_collection("rfp_chunks")
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        sys.exit(1)
    
    db_connect_time = time.time() - db_connect_start
    if enable_debug:
        print(f"⚡ [VECTOR-{query_hash}] DB connection: {db_connect_time:.3f}s")
    
    # Load the same model used for embedding
    model_load_start = time.time()
    model = SentenceTransformer('all-mpnet-base-v2')
    model_load_time = time.time() - model_load_start
    
    if enable_debug:
        print(f"🧠 [VECTOR-{query_hash}] Model loading: {model_load_time:.3f}s")
    
    # Perform search with timing
    search_start = time.time()
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"section_type": section_filter} if section_filter else None
    )
    search_time = time.time() - search_start
    
    total_time = time.time() - start_time
    
    if not results['documents'][0]:
        if enable_debug:
            print(f"⚠️  [VECTOR-{query_hash}] No relevant chunks found (search: {search_time:.3f}s, total: {total_time:.3f}s)")
        return "", get_query_debug_info(query_hash, query, 0, total_time, db_connect_time, model_load_time, search_time, section_filter)
    
    chunk_count = len(results['documents'][0])
    if enable_debug:
        print(f"✅ [VECTOR-{query_hash}] Found {chunk_count} chunks (search: {search_time:.3f}s, total: {total_time:.3f}s)")
    
    # Format results for analysis
    retrieved_content = []
    
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        # Add separator and metadata
        chunk_header = f"\n{'='*80}\n"
        chunk_header += f"CHUNK {i+1} | Source: {metadata['source_file']} | Type: {metadata['section_type']}\n"
        chunk_header += f"{'='*80}\n"
        
        retrieved_content.append(chunk_header + doc)
    
    # Join all chunks
    final_content = "\n\n".join(retrieved_content)
    
    # Add summary header with debug info
    debug_info = get_query_debug_info(query_hash, query, chunk_count, total_time, db_connect_time, model_load_time, search_time, section_filter)
    summary_header = f"""# RETRIEVED RFP CONTENT
Query: {query}
Retrieved: {chunk_count} most relevant chunks
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Query ID: {query_hash}
Performance: {debug_info['performance']['search_efficiency']} ({total_time:.3f}s total)

{'='*100}
"""
    
    return summary_header + final_content, debug_info

def get_database_stats(db_path):
    """Get statistics about the vector database"""
    try:
        import chromadb
        
        if not os.path.exists(db_path):
            return None
        
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_collection("rfp_chunks")
        
        # Get collection info
        count = collection.count()
        
        # Load metadata if available
        metadata_file = os.path.join(os.path.dirname(db_path), '.vector_index.json')
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        return {
            'total_chunks': count,
            'metadata': metadata
        }
    except Exception as e:
        print(f"⚠️  Error getting database stats: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Query RFP Vector Database')
    parser.add_argument('--query', required=True, help='Search query for relevant content')
    parser.add_argument('--db', default='./output/.vector_db', help='Path to vector database')
    parser.add_argument('--output', help='Output file for retrieved content (optional)')
    parser.add_argument('--top_k', type=int, default=10, help='Number of chunks to retrieve')
    parser.add_argument('--section', choices=['requirements', 'timeline', 'evaluation', 'pricing', 'technical', 'general'], 
                       help='Filter by section type')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    # Show stats if requested
    if args.stats:
        stats = get_database_stats(args.db)
        if stats:
            print("📊 Vector Database Statistics:")
            print(f"   Total chunks: {stats['total_chunks']}")
            if 'metadata' in stats and stats['metadata']:
                print(f"   Created: {stats['metadata'].get('created', 'Unknown')}")
                print(f"   Source files: {len(stats['metadata'].get('source_files', []))}")
                if 'chunk_stats' in stats['metadata']:
                    print("   Chunks by section:")
                    for section, count in stats['metadata']['chunk_stats'].items():
                        print(f"      {section}: {count}")
        return
    
    # Perform query
    content, debug_info = query_rfp_database(args.query, args.db, args.top_k, args.section)
    
    # Save debug info to file
    debug_file = f"vector_query_debug_{debug_info['query_id']}.json"
    with open(debug_file, 'w') as f:
        json.dump(debug_info, f, indent=2)
    print(f"🔍 Debug info saved to {debug_file}")
    
    if args.output:
        # Save to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Content saved to {args.output}")
    else:
        # Print to stdout
        print("\n" + content)

if __name__ == "__main__":
    main()