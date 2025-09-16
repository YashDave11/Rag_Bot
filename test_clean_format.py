#!/usr/bin/env python3
"""
Test the clean formatting with a single question
"""

from clean_interactive_agent import CleanInteractiveAgent

def test_clean_format():
    """Test the clean formatting"""
    try:
        print("🧪 Testing Clean Format...")
        agent = CleanInteractiveAgent()
        
        # Test questions
        questions = [
            "hi",
            "What are MongoDB best practices?",
            "How do I create an index in MongoDB?",
            "What is aggregation?"
        ]
        
        for question in questions:
            print(f"\n{'='*60}")
            print(f"Question: {question}")
            print('='*60)
            
            response = agent.answer_question(question)
            print(response)
            print("\n")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_clean_format()