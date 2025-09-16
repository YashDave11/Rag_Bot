#!/usr/bin/env python3
"""
Test the FastAPI server
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing MongoDB RAG Chat API...")
    
    try:
        # Test health check
        print("\n1. Testing health check...")
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test detailed health
        print("\n2. Testing detailed health...")
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test chat endpoint
        print("\n3. Testing chat endpoint...")
        chat_data = {
            "message": "What are MongoDB best practices?",
            "session_id": None
        }
        
        response = requests.post(
            f"{base_url}/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Session ID: {result['session_id']}")
            print(f"Response: {result['response'][:200]}...")
            
            # Test chat history
            print("\n4. Testing chat history...")
            session_id = result['session_id']
            response = requests.get(f"{base_url}/chat/history/{session_id}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                history = response.json()
                print(f"Messages in history: {len(history['messages'])}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()