#!/usr/bin/env python3
"""
RFP Vector Database Setup Script
Chunks and indexes RFP documents for intelligent retrieval
"""

import os
import sys
import glob
import argparse
import json
from pathlib import Path
import re
from datetime import datetime

def install_dependencies():
    """Install required packages if not available"""
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
        import PyPDF2
        from docx import Document
        import pandas as pd
    except ImportError as e:
        print(f"🚨 Missing dependency: {e}")
        print("Installing required packages...")
        os.system("pip install chromadb sentence-transformers PyPDF2 python-docx pandas openpyxl")
        print("✅ Dependencies installed. Please run the script again.")
        sys.exit(1)

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        import PyPDF2
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        print(f"⚠️  Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from Word document"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"⚠️  Error reading DOCX {file_path}: {e}")
        return ""

def extract_text_from_excel(file_path):
    """Extract text from Excel file"""
    try:
        import pandas as pd
        text = ""
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            text += f"## Sheet: {sheet_name}\n\n"
            text += df.to_string(index=False) + "\n\n"
        return text
    except Exception as e:
        print(f"⚠️  Error reading Excel {file_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    """Extract text from various file formats"""
    file_path = Path(file_path)
    
    if file_path.suffix.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_path.suffix.lower() in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        return extract_text_from_excel(file_path)
    elif file_path.suffix.lower() == '.md':
        return file_path.read_text(encoding='utf-8')
    elif file_path.suffix.lower() == '.txt':
        return file_path.read_text(encoding='utf-8')
    else:
        print(f"⚠️  Unsupported file format: {file_path}")
        return ""

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

def intelligent_chunk_document(file_path, chunk_size=1000, overlap=200):
    """Chunk document intelligently based on content structure"""
    print(f"📄 Processing: {os.path.basename(file_path)}")
    
    text = extract_text_from_file(file_path)
    if not text.strip():
        print(f"⚠️  No text extracted from {file_path}")
        return []
    
    chunks = []
    
    # Split by sections first (headers, numbered items, etc.)
    sections = re.split(r'\n\s*(?=\d+\.|\#\#?|\*\*|[A-Z][A-Z\s]+:)', text)
    
    for section in sections:
        if not section.strip():
            continue
            
        # If section is small enough, keep as single chunk
        if len(section) <= chunk_size:
            chunks.append({
                'text': section.strip(),
                'metadata': {
                    'source_file': os.path.basename(file_path),
                    'section_type': detect_section_type(section),
                    'chunk_size': len(section),
                    'full_file_path': str(file_path)
                }
            })
        else:
            # Split large sections into smaller chunks with overlap
            words = section.split()
            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunk_text = ' '.join(chunk_words)
                
                chunks.append({
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

def setup_vector_database(input_folder, output_folder):
    """Main function to setup vector database"""
    print("🚀 Setting up RFP Vector Database...")
    
    # Install dependencies
    install_dependencies()
    
    # Import after installation
    import chromadb
    from sentence_transformers import SentenceTransformer
    
    # Create output directory
    os.makedirs(output_folder, exist_ok=True)
    vector_db_path = os.path.join(output_folder, '.vector_db')
    
    # Initialize ChromaDB
    print("🔧 Initializing vector database...")
    client = chromadb.PersistentClient(path=vector_db_path)
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("rfp_chunks")
        print("🗑️  Cleared existing vector database")
    except:
        pass
    
    collection = client.get_or_create_collection("rfp_chunks")
    
    # Load embedding model
    print("🤖 Loading embedding model...")
    model = SentenceTransformer('all-mpnet-base-v2')
    
    # Process all files in input folder
    input_files = glob.glob(os.path.join(input_folder, "*"))
    input_files = [f for f in input_files if os.path.isfile(f) and not f.startswith('.')]
    
    if not input_files:
        print(f"⚠️  No files found in {input_folder}")
        return False
    
    print(f"📂 Found {len(input_files)} files to process")
    
    all_chunks = []
    chunk_metadata = []
    
    # Process each file
    for file_path in input_files:
        chunks = intelligent_chunk_document(file_path)
        all_chunks.extend(chunks)
    
    if not all_chunks:
        print("⚠️  No chunks created. Check your input files.")
        return False
    
    print(f"🔍 Generated {len(all_chunks)} total chunks")
    print("🧠 Creating embeddings...")
    
    # Create embeddings and add to vector database
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        
        # Extract texts and metadata
        texts = [chunk['text'] for chunk in batch]
        metadatas = [chunk['metadata'] for chunk in batch]
        
        # Create embeddings
        embeddings = model.encode(texts).tolist()
        
        # Generate IDs
        ids = [f"chunk_{i + j}" for j in range(len(batch))]
        
        # Add to collection
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Processed batch {i//batch_size + 1}/{(len(all_chunks)-1)//batch_size + 1}")
    
    # Save metadata for reference
    metadata_file = os.path.join(output_folder, '.vector_index.json')
    with open(metadata_file, 'w') as f:
        json.dump({
            'created': datetime.now().isoformat(),
            'total_chunks': len(all_chunks),
            'source_files': [os.path.basename(f) for f in input_files],
            'chunk_stats': {
                section_type: len([c for c in all_chunks if c['metadata']['section_type'] == section_type])
                for section_type in set(c['metadata']['section_type'] for c in all_chunks)
            }
        }, f, indent=2)
    
    # Create ready flag
    ready_file = os.path.join(output_folder, '.vector_ready')
    with open(ready_file, 'w') as f:
        f.write(f"Vector database ready - {datetime.now().isoformat()}")
    
    print("🎉 Vector database setup complete!")
    print(f"📊 Stats:")
    print(f"   - Total chunks: {len(all_chunks)}")
    print(f"   - Source files: {len(input_files)}")
    print(f"   - Database path: {vector_db_path}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Setup RFP Vector Database')
    parser.add_argument('--input', required=True, help='Input folder containing RFP documents')
    parser.add_argument('--output', default='./output', help='Output folder for vector database')
    parser.add_argument('--force', action='store_true', help='Force rebuild even if database exists')
    
    args = parser.parse_args()
    
    # Check if already exists
    ready_file = os.path.join(args.output, '.vector_ready')
    if os.path.exists(ready_file) and not args.force:
        print("✅ Vector database already exists. Use --force to rebuild.")
        return
    
    success = setup_vector_database(args.input, args.output)
    if success:
        print("✅ Ready to run RFP analysis!")
    else:
        print("❌ Setup failed. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()