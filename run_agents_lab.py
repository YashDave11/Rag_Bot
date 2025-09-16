#!/usr/bin/env python3
"""
AI Agents Lab - MongoDB GenAI Developer Day
A simplified version of the notebook that can run without environment setup
"""

import os
import sys
import json
from pathlib import Path

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent / "utils"))

def main():
    print("🚀 MongoDB AI Agents Lab")
    print("=" * 50)
    
    # Check if we have the required data files
    data_dir = Path(__file__).parent / "data"
    required_files = [
        "mongodb_docs_embeddings.json",
        "mongodb_docs.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not (data_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required data files: {missing_files}")
        print("Please ensure the data files are in the 'data' directory")
        return
    
    print("✅ Data files found")
    
    # Check if we can import required packages
    try:
        from pymongo import MongoClient
        from sentence_transformers import SentenceTransformer
        from langchain.agents import tool
        from typing import List
        print("✅ Required packages imported successfully")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # For demo purposes, we'll create a mock setup
    print("\n📚 Setting up demo environment...")
    
    # Load sample data to show structure
    with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
        sample_data = json.load(f)
    
    print(f"✅ Loaded {len(sample_data)} documents with embeddings")
    print(f"Sample document keys: {list(sample_data[0].keys()) if sample_data else 'No data'}")
    
    # Show what the embedding model would look like
    print("\n🤖 Loading embedding model...")
    try:
        # This will download the model if not already cached
        embedding_model = SentenceTransformer("thenlper/gte-small")
        print("✅ Embedding model loaded successfully")
        
        # Test embedding
        test_text = "What are MongoDB best practices?"
        embedding = embedding_model.encode(test_text)
        print(f"✅ Test embedding generated: {len(embedding)} dimensions")
        
    except Exception as e:
        print(f"❌ Error loading embedding model: {e}")
        return
    
    # Show the tool structure that would be created
    print("\n🛠️  Agent Tools Structure:")
    print("1. get_information_for_question_answering - Uses vector search")
    print("2. get_page_content_for_summarization - Retrieves full page content")
    
    # Show what a complete setup would require
    print("\n📋 To run the complete lab, you would need:")
    print("1. MongoDB Atlas cluster with connection string")
    print("2. LLM provider API keys (AWS Bedrock, Google AI, or OpenAI)")
    print("3. Environment variables:")
    print("   - MONGODB_URI: Your MongoDB connection string")
    print("   - SERVERLESS_URL: Workshop serverless endpoint")
    print("   - API keys for your chosen LLM provider")
    
    print("\n🎯 Demo completed successfully!")
    print("The notebook is ready to run with proper environment setup.")

if __name__ == "__main__":
    main()