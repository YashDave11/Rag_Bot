#!/usr/bin/env python3
"""
Step-by-step demo of the AI Agents Lab
Run each section individually to understand the concepts
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

def step_1_setup():
    """Step 1: Setup prerequisites"""
    print("=" * 60)
    print("STEP 1: Setup Prerequisites")
    print("=" * 60)
    
    try:
        import os
        from pymongo import MongoClient
        print("✅ Required imports successful")
        
        # For demo, we'll skip the actual MongoDB connection
        print("✅ MongoDB client import successful")
        print("📝 Note: In real implementation, you'd connect to MongoDB Atlas here")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def step_2_load_data():
    """Step 2: Load sample data"""
    print("\n" + "=" * 60)
    print("STEP 2: Load Sample Data")
    print("=" * 60)
    
    data_dir = Path(__file__).parent / "data"
    
    # Load vector search data
    with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
        vector_data = json.load(f)
    
    # Load full documents
    with open(data_dir / "mongodb_docs.json", "r") as f:
        full_data = json.load(f)
    
    print(f"✅ Loaded {len(vector_data)} documents with embeddings")
    print(f"✅ Loaded {len(full_data)} full documents")
    
    # Show sample structure
    if vector_data:
        sample_doc = vector_data[0]
        print(f"📊 Sample document fields: {list(sample_doc.keys())}")
        print(f"📊 Embedding dimensions: {len(sample_doc.get('embedding', []))}")
    
    return vector_data, full_data

def step_3_embedding_model():
    """Step 3: Load embedding model"""
    print("\n" + "=" * 60)
    print("STEP 3: Load Embedding Model")
    print("=" * 60)
    
    try:
        from sentence_transformers import SentenceTransformer
        
        print("📥 Loading gte-small embedding model...")
        embedding_model = SentenceTransformer("thenlper/gte-small")
        print("✅ Embedding model loaded successfully")
        
        # Test the model
        test_text = "What are MongoDB best practices?"
        embedding = embedding_model.encode(test_text)
        print(f"✅ Test embedding generated: {len(embedding)} dimensions")
        
        return embedding_model
    except Exception as e:
        print(f"❌ Error loading embedding model: {e}")
        return None

def step_4_create_tools(embedding_model, vector_data, full_data):
    """Step 4: Create agent tools"""
    print("\n" + "=" * 60)
    print("STEP 4: Create Agent Tools")
    print("=" * 60)
    
    def get_embedding(text: str) -> List[float]:
        """Generate embedding for text"""
        embedding = embedding_model.encode(text)
        return embedding.tolist()
    
    def get_information_for_question_answering(user_query: str) -> str:
        """Tool: Retrieve information using vector search"""
        print(f"🔍 Searching for: '{user_query}'")
        
        # Generate query embedding
        query_embedding = get_embedding(user_query)
        
        # Simple similarity search (mock vector search)
        import numpy as np
        similarities = []
        
        for doc in vector_data[:20]:  # Check first 20 docs for demo
            if 'embedding' in doc:
                doc_embedding = doc['embedding']
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                similarities.append((similarity, doc))
        
        # Sort by similarity and get top 3
        similarities.sort(reverse=True, key=lambda x: x[0])
        top_docs = [doc for _, doc in similarities[:3]]
        
        # Format results
        context_parts = []
        for i, doc in enumerate(top_docs):
            title = doc.get('title', 'Unknown')
            body = doc.get('body', '')[:300]  # Truncate
            context_parts.append(f"Document {i+1} - {title}:\n{body}...")
        
        context = "\n\n".join(context_parts)
        print(f"✅ Found {len(top_docs)} relevant documents")
        return context
    
    def get_page_content_for_summarization(page_title: str) -> str:
        """Tool: Get page content by title"""
        print(f"📄 Looking for page: '{page_title}'")
        
        for doc in full_data:
            if doc.get('title', '').lower() == page_title.lower():
                print("✅ Page found")
                return doc.get('body', 'No content found')
        
        print("❌ Page not found")
        return "Document not found"
    
    print("✅ Agent tools created:")
    print("  1. get_information_for_question_answering")
    print("  2. get_page_content_for_summarization")
    
    return get_information_for_question_answering, get_page_content_for_summarization

def step_5_test_tools(qa_tool, summarize_tool):
    """Step 5: Test the tools"""
    print("\n" + "=" * 60)
    print("STEP 5: Test Agent Tools")
    print("=" * 60)
    
    # Test Q&A tool
    print("🧪 Testing Q&A tool...")
    qa_result = qa_tool("What are some best practices for data backups in MongoDB?")
    print(f"📝 Q&A Result (first 200 chars): {qa_result[:200]}...")
    
    print("\n🧪 Testing summarization tool...")
    summary_result = summarize_tool("Create a MongoDB Deployment")
    print(f"📝 Summary Result (first 200 chars): {summary_result[:200]}...")
    
    return True

def step_6_simple_agent():
    """Step 6: Create a simple agent"""
    print("\n" + "=" * 60)
    print("STEP 6: Simple Agent Logic")
    print("=" * 60)
    
    def simple_agent(user_input: str, qa_tool, summarize_tool) -> str:
        """Simple agent that routes queries to appropriate tools"""
        print(f"🤖 Processing: '{user_input}'")
        
        # Simple routing logic
        if any(word in user_input.lower() for word in ['summary', 'summarize']):
            # Extract title (simplified)
            if 'page titled' in user_input.lower():
                title_start = user_input.lower().find('page titled') + len('page titled')
                title = user_input[title_start:].strip().strip('"').strip("'")
                return summarize_tool(title)
            else:
                return "Please specify which page you'd like me to summarize."
        else:
            # Use Q&A tool
            context = qa_tool(user_input)
            return f"Based on MongoDB documentation:\n\n{context}"
    
    print("✅ Simple agent created")
    print("📝 Agent can route queries to appropriate tools")
    
    return simple_agent

def main():
    """Run the complete step-by-step demo"""
    print("🚀 MongoDB AI Agents Lab - Step by Step Demo")
    
    # Step 1: Setup
    if not step_1_setup():
        return
    
    # Step 2: Load data
    vector_data, full_data = step_2_load_data()
    
    # Step 3: Load embedding model
    embedding_model = step_3_embedding_model()
    if not embedding_model:
        return
    
    # Step 4: Create tools
    qa_tool, summarize_tool = step_4_create_tools(embedding_model, vector_data, full_data)
    
    # Step 5: Test tools
    step_5_test_tools(qa_tool, summarize_tool)
    
    # Step 6: Create simple agent
    simple_agent = step_6_simple_agent()
    
    # Demo the agent
    print("\n" + "=" * 60)
    print("FINAL DEMO: Agent in Action")
    print("=" * 60)
    
    test_queries = [
        "What are MongoDB best practices?",
        "Give me a summary of the page titled Create a MongoDB Deployment"
    ]
    
    for query in test_queries:
        print(f"\n🎯 Query: {query}")
        response = simple_agent(query, qa_tool, summarize_tool)
        print(f"🤖 Response: {response[:300]}...")
        print("-" * 40)
    
    print("\n✅ Step-by-step demo completed!")
    print("🎓 You now understand how MongoDB AI agents work!")

if __name__ == "__main__":
    main()