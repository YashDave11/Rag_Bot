#!/usr/bin/env python3
"""
Simple test version of the MongoDB AI agent
"""

import json
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

def test_agent():
    """Simple test function"""
    try:
        print("🤖 Testing MongoDB AI Assistant...")
        
        # Setup Gemini
        api_key = "AIzaSyCl5ubFeNTdeqmWPu4iYOc97dec6fuCHcc"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini configured")
        
        # Load data
        data_dir = Path(__file__).parent / "data"
        with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
            vector_data = json.load(f)
        print(f"✅ Loaded {len(vector_data)} documents")
        
        # Load embedding model
        embedding_model = SentenceTransformer("thenlper/gte-small")
        print("✅ Embedding model loaded")
        
        # Test question
        question = "What are MongoDB best practices?"
        print(f"\n🔍 Testing question: {question}")
        
        # Get embeddings and search
        query_embedding = embedding_model.encode(question)
        
        # Simple search - just get first 3 docs
        top_docs = vector_data[:3]
        
        # Prepare context
        context_parts = []
        for doc in top_docs:
            title = doc.get('title', 'Unknown')
            body = doc.get('body', '')[:500]  # Limit content
            context_parts.append(f"Title: {title}\nContent: {body}")
        
        context = "\n\n".join(context_parts)
        
        # Simple prompt
        prompt = f"""You are a MongoDB expert. Answer this question based on the provided context.

Question: {question}

Context:
{context}

Provide a clear, helpful answer with bullet points and examples where appropriate."""

        print("🧠 Generating response...")
        response = model.generate_content(prompt)
        
        print(f"\n🤖 Response:")
        print(response.text)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent()