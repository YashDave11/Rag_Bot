#!/usr/bin/env python3
"""
Update embeddings for college rules data
"""

import json
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

def update_embeddings():
    """Generate embeddings for college rules data"""
    print("🚀 Updating training data with college rules...")
    print("=" * 60)
    
    # Load the embedding model
    print("📥 Loading embedding model...")
    model = SentenceTransformer("thenlper/gte-small")
    print("✅ Model loaded successfully")
    
    # Load college rules data
    data_dir = Path(__file__).parent / "data"
    with open(data_dir / "mongodb_docs.json", "r") as f:
        college_data = json.load(f)
    
    print(f"📚 Loaded {len(college_data)} college rules")
    
    # Generate embeddings
    print("🔄 Generating embeddings...")
    for i, item in enumerate(college_data):
        # Combine question and answer for better context
        text_to_embed = f"Question: {item['question']} Answer: {item['answer']}"
        
        # Generate embedding
        embedding = model.encode(text_to_embed)
        item['embedding'] = embedding.tolist()
        
        print(f"  ✅ Generated embedding {i+1}/{len(college_data)}")
    
    # Save the data with embeddings
    output_file = data_dir / "mongodb_docs_embeddings.json"
    with open(output_file, "w") as f:
        json.dump(college_data, f, indent=2)
    
    print(f"✅ Embeddings saved to {output_file}")
    print(f"📊 Generated {len(college_data)} embeddings with {len(college_data[0]['embedding'])} dimensions each")
    
    print("\n🎯 Training data successfully updated!")
    print("Your chatbot now uses college rules instead of MongoDB docs!")

if __name__ == "__main__":
    try:
        update_embeddings()
        print("\n🎉 College training data update completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)