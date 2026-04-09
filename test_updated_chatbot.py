#!/usr/bin/env python3
"""
Test the updated college chatbot
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

def test_college_chatbot():
    """Test the college chatbot with updated training data"""
    print("🧪 Testing Updated College Chatbot")
    print("=" * 50)
    
    try:
        # Load the embedding model
        print("📥 Loading embedding model...")
        embedding_model = SentenceTransformer("thenlper/gte-small")
        print("✅ Embedding model loaded")
        
        # Load college data
        data_dir = Path(__file__).parent / "data"
        with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
            college_data = json.load(f)
        
        print(f"📚 Loaded {len(college_data)} college rules")
        
        # Test search function
        def search_rules(query: str, top_k: int = 3) -> List[Dict]:
            """Search for relevant college rules"""
            query_embedding = embedding_model.encode(query).tolist()
            
            similarities = []
            for rule in college_data:
                if 'embedding' in rule:
                    rule_embedding = rule['embedding']
                    similarity = np.dot(query_embedding, rule_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(rule_embedding)
                    )
                    similarities.append((similarity, rule))
            
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [rule for _, rule in similarities[:top_k]]
        
        # Test queries
        test_queries = [
            "What is the minimum attendance required?",
            "Can I use my phone during class?",
            "What happens if I don't wear a helmet?",
            "Are assignments important?",
            "What are the consequences of cheating?",
            "What happens if I miss both mid-term exams?",
            "Is ragging allowed in college?"
        ]
        
        print("\n🎯 Testing Search Results:")
        print("-" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            results = search_rules(query, top_k=1)
            
            if results:
                best_match = results[0]
                print(f"   ✅ Best Match: {best_match['question']}")
                print(f"   📝 Answer: {best_match['answer'][:100]}...")
                print(f"   🏷️ Category: {best_match.get('category', 'general')}")
            else:
                print("   ❌ No matches found")
        
        print("\n✅ All tests completed successfully!")
        print("🎓 Your chatbot is now ready to help students with college rules!")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_college_chatbot()
    if success:
        print("\n🎉 Training data update successful!")
        print("💡 You can now run any of these:")
        print("   - python api_server.py (for API)")
        print("   - python interactive_agent.py (for chat)")
        print("   - python enhanced_api_server.py (for enhanced API)")
    else:
        print("\n❌ Tests failed. Please check the setup.")
        sys.exit(1)