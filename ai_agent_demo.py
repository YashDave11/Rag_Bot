#!/usr/bin/env python3
"""
AI Agent Demo - Working example without external dependencies
Shows how the MongoDB AI agent would work with mock data
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

class MockMongoCollection:
    """Mock MongoDB collection for demo purposes"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def aggregate(self, pipeline: List[Dict]) -> List[Dict]:
        """Mock aggregation pipeline for vector search"""
        # For demo, just return top 3 most relevant documents
        # In real implementation, this would use MongoDB's $vectorSearch
        return self.data[:3]
    
    def find_one(self, query: Dict, projection: Dict = None) -> Dict:
        """Mock find_one for document retrieval"""
        # Find document by title
        title = query.get("title")
        for doc in self.data:
            if doc.get("title") == title:
                if projection:
                    # Return only requested fields
                    result = {}
                    for field, include in projection.items():
                        if include and field in doc:
                            result[field] = doc[field]
                    return result
                return doc
        return None

class AIAgent:
    """MongoDB AI Agent implementation"""
    
    def __init__(self):
        print("🤖 Initializing AI Agent...")
        
        # Load data
        data_dir = Path(__file__).parent / "data"
        with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
            self.vector_data = json.load(f)
        
        with open(data_dir / "mongodb_docs.json", "r") as f:
            self.full_data = json.load(f)
        
        # Initialize mock collections
        self.vs_collection = MockMongoCollection(self.vector_data)
        self.full_collection = MockMongoCollection(self.full_data)
        
        # Load embedding model
        print("📥 Loading embedding model...")
        self.embedding_model = SentenceTransformer("thenlper/gte-small")
        
        print("✅ AI Agent initialized successfully!")
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def get_information_for_question_answering(self, user_query: str) -> str:
        """
        Tool: Retrieve information using vector search to answer a user query.
        """
        print(f"🔍 Searching for: '{user_query}'")
        
        # Generate embedding for query
        query_embedding = self.get_embedding(user_query)
        
        # Mock vector search pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 150,
                    "limit": 5
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "body": 1,
                    "title": 1,
                    "vectorSearchScore": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        # Execute search (mocked)
        results = self.vs_collection.aggregate(pipeline)
        
        # Format results
        context_parts = []
        for i, doc in enumerate(results[:3]):  # Top 3 results
            title = doc.get("title", "Unknown")
            body = doc.get("body", "")[:500]  # Truncate for demo
            context_parts.append(f"Document {i+1} - {title}:\n{body}...")
        
        context = "\n\n".join(context_parts)
        print(f"✅ Found {len(results)} relevant documents")
        return context
    
    def get_page_content_for_summarization(self, page_title: str) -> str:
        """
        Tool: Retrieve page content based on provided title.
        """
        print(f"📄 Retrieving page: '{page_title}'")
        
        # Query for document
        query = {"title": page_title}
        projection = {"body": 1, "_id": 0}
        
        document = self.full_collection.find_one(query, projection)
        
        if document:
            print("✅ Page content retrieved")
            return document["body"]
        else:
            print("❌ Document not found")
            return "Document not found"
    
    def process_query(self, user_input: str) -> str:
        """
        Main agent logic - decides which tool to use based on user input
        """
        print(f"\n🎯 Processing query: '{user_input}'")
        
        # Simple logic to determine intent
        if any(word in user_input.lower() for word in ["summary", "summarize", "page titled"]):
            # Extract page title (simplified)
            if "page titled" in user_input.lower():
                title_start = user_input.lower().find("page titled") + len("page titled")
                title = user_input[title_start:].strip().strip('"').strip("'")
                content = self.get_page_content_for_summarization(title)
                return f"Here's the content for '{title}':\n\n{content[:1000]}..."
            else:
                return "Please specify the page title you'd like me to summarize."
        
        else:
            # Use vector search for Q&A
            context = self.get_information_for_question_answering(user_input)
            
            # Mock LLM response (in real implementation, this would call an LLM)
            response = f"""Based on the MongoDB documentation, here's what I found:

{context}

This information should help answer your question about: {user_input}

Note: In a full implementation, this would be processed by an LLM to generate a more natural response."""
            
            return response

def main():
    """Main demo function"""
    print("🚀 MongoDB AI Agent Demo")
    print("=" * 60)
    
    try:
        # Initialize agent
        agent = AIAgent()
        
        # Demo queries
        demo_queries = [
            "What are some best practices for data backups in MongoDB?",
            "How do I optimize MongoDB performance?",
            "Give me a summary of the page titled Create a MongoDB Deployment"
        ]
        
        print("\n" + "=" * 60)
        print("🎮 Running Demo Queries")
        print("=" * 60)
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n--- Demo Query {i} ---")
            response = agent.process_query(query)
            print(f"\n🤖 Agent Response:\n{response}")
            print("\n" + "-" * 40)
        
        print("\n✅ Demo completed successfully!")
        print("\nThis demonstrates how the AI agent would:")
        print("1. 🔍 Use vector search to find relevant documents")
        print("2. 📄 Retrieve specific page content for summarization")
        print("3. 🤖 Process user queries intelligently")
        print("4. 🔄 Maintain conversation context (in full implementation)")
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()