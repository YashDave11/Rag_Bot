#!/usr/bin/env python3
"""
Test script for the enhanced Gemini-powered agent
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_agent():
    """Test the enhanced agent"""
    print("🧪 Testing Enhanced MongoDB AI Agent")
    print("=" * 50)
    
    try:
        from interactive_agent import InteractiveAgent
        
        # Initialize agent
        agent = InteractiveAgent()
        
        # Test a simple question
        test_question = "What are MongoDB best practices?"
        print(f"\n🔍 Testing question: {test_question}")
        
        response = agent.answer_question(test_question)
        print(f"\n🤖 Response:\n{response}")
        
        print("\n✅ Agent test completed!")
        
        if agent.use_gemini:
            print("🚀 Gemini API is working - you'll get enhanced responses!")
        else:
            print("⚠️  Gemini API not configured - using basic responses")
            print("   To enable Gemini:")
            print("   1. Get API key from: https://makersuite.google.com/app/apikey")
            print("   2. Set environment variable: set GEMINI_API_KEY=your_key_here")
            print("   3. Run the agent again")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()