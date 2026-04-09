#!/usr/bin/env python3
"""
Test script to verify context maintenance in the chatbot
"""

import requests
import json
import time

def test_context_maintenance():
    """Test that the chatbot maintains conversation context"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Context Maintenance in Chatbot")
    print("=" * 50)
    
    # Test 1: Start a new conversation
    print("\n1. Starting new conversation...")
    
    conversation_tests = [
        {
            "message": "What is the college name?",
            "expected_context": "Should provide college information"
        },
        {
            "message": "What are the admission requirements?", 
            "expected_context": "Should provide admission info"
        },
        {
            "message": "Can you tell me more about the fees mentioned earlier?",
            "expected_context": "Should reference previous conversation about fees/admission"
        },
        {
            "message": "What about the courses you mentioned?",
            "expected_context": "Should reference previous conversation about courses"
        }
    ]
    
    session_id = None
    
    for i, test in enumerate(conversation_tests, 1):
        print(f"\n{i}. Testing: {test['message']}")
        
        payload = {
            "message": test["message"],
            "session_id": session_id
        }
        
        try:
            response = requests.post(f"{base_url}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                session_id = data["session_id"]  # Keep the same session
                
                print(f"   ✅ Response: {data['response'][:100]}...")
                print(f"   📝 Session ID: {session_id}")
                print(f"   🌍 Language: {data['detected_language']} -> {data['response_language']}")
                
                # Check conversation history
                history_response = requests.get(f"{base_url}/chat/history/{session_id}")
                if history_response.status_code == 200:
                    history = history_response.json()
                    print(f"   💬 Conversation length: {history['message_count']} messages")
                else:
                    print(f"   ⚠️ Could not fetch history: {history_response.status_code}")
                
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    # Test 2: Verify conversation history
    print(f"\n📚 Final Conversation History Check")
    print("-" * 30)
    
    if session_id:
        try:
            history_response = requests.get(f"{base_url}/chat/history/{session_id}")
            if history_response.status_code == 200:
                history = history_response.json()
                print(f"Session ID: {history['session_id']}")
                print(f"Total Messages: {history['message_count']}")
                print(f"Created: {history['created_at']}")
                print(f"Last Activity: {history['last_activity']}")
                
                print("\nConversation Flow:")
                for i, msg in enumerate(history['messages'], 1):
                    print(f"  {i}. User: {msg['user_message'][:50]}...")
                    print(f"     Bot: {msg['bot_response'][:50]}...")
                    print()
            else:
                print(f"❌ Could not fetch final history: {history_response.status_code}")
        except Exception as e:
            print(f"❌ Exception fetching history: {e}")
    
    # Test 3: Health check
    print("\n🏥 Health Check")
    print("-" * 15)
    
    try:
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code == 200:
            health = health_response.json()
            print(f"Status: {health['status']}")
            print(f"Active Sessions: {health['active_sessions']}")
            print(f"Total Messages: {health['total_messages']}")
            print(f"Context Maintenance: {health['context_maintenance']}")
            print(f"Multilingual Support: {health['multilingual_support']}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Health check exception: {e}")
    
    print("\n✅ Context maintenance test completed!")
    print("\nTo test manually:")
    print("1. Start the server: python all_data.py")
    print("2. Open your chat widget")
    print("3. Ask follow-up questions that reference previous messages")
    print("4. The bot should maintain context across the conversation")

if __name__ == "__main__":
    test_context_maintenance()