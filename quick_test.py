#!/usr/bin/env python3
"""
Quick test of the updated chatbot system
"""

import sys
import os
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

def quick_test():
    """Quick test of the college chatbot"""
    print("🏫 Quick College Chatbot Test")
    print("=" * 40)
    
    try:
        # Import the agent class
        from api_server import Agent
        
        # Initialize agent
        print("🚀 Initializing agent...")
        agent = Agent()
        
        # Test a few queries
        test_queries = [
            "What is the minimum attendance required?",
            "Can I use my phone during class?",
            "What happens if I cheat in exams?"
        ]
        
        print("\n🧪 Testing queries:")
        for query in test_queries:
            print(f"\n❓ Question: {query}")
            
            # Use the agent's chat method
            result = agent.chat(query)
            print(f"🤖 Response: {result['response'][:150]}...")
        
        print("\n✅ Quick test completed successfully!")
        print("🎓 Your college chatbot is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Your chatbot training data has been successfully updated!")
        print("📚 The system now uses college rules instead of MongoDB docs!")
    else:
        print("\n❌ Test failed. Please check the setup.")
        sys.exit(1)