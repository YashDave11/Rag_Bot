#!/usr/bin/env python3
"""
Test script to verify that the formatting fix is working
"""

import requests
import json

def test_formatting_fix():
    """Test the formatting fix for markdown removal"""
    print("🧪 Testing Formatting Fix")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test query
    test_query = "what is inspire100"
    
    try:
        # Test health endpoint first
        print("1. Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ Server is healthy")
            print(f"   📚 Documents loaded: {health_data.get('documents_loaded', 0)}")
            print(f"   🤖 Gemini available: {health_data.get('gemini_available', False)}")
        else:
            print(f"   ❌ Health check failed: {health_response.status_code}")
            return
        
        print("\n2. Testing chat endpoint...")
        chat_payload = {
            "message": test_query,
            "session_id": "test_session_123"
        }
        
        print(f"   📝 Sending query: '{test_query}'")
        chat_response = requests.post(
            f"{base_url}/chat",
            json=chat_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if chat_response.status_code == 200:
            data = chat_response.json()
            
            print(f"   ✅ Chat response received")
            print(f"   🌍 Detected language: {data.get('detected_language')}")
            print(f"   🎯 Response language: {data.get('response_language')}")
            
            response_text = data.get('response', '')
            print(f"\n3. Analyzing response formatting...")
            print(f"   📝 Response length: {len(response_text)} characters")
            
            # Check for markdown formatting
            has_asterisks = '*' in response_text
            has_hashes = '#' in response_text
            has_underscores = '_' in response_text and response_text.count('_') > 2
            
            print(f"   🔍 Markdown check:")
            print(f"      - Contains asterisks (*): {'❌ YES' if has_asterisks else '✅ NO'}")
            print(f"      - Contains hashes (#): {'❌ YES' if has_hashes else '✅ NO'}")
            print(f"      - Contains underscores (_): {'❌ YES' if has_underscores else '✅ NO'}")
            
            if not has_asterisks and not has_hashes and not has_underscores:
                print(f"   🎉 FORMATTING FIX SUCCESSFUL - No markdown found!")
            else:
                print(f"   ⚠️  FORMATTING ISSUE - Markdown still present")
            
            print(f"\n4. Response preview:")
            print(f"   " + "─" * 60)
            preview = response_text[:300] + "..." if len(response_text) > 300 else response_text
            for line in preview.split('\n'):
                print(f"   {line}")
            print(f"   " + "─" * 60)
            
            # Check if response is meaningful (not just error message)
            is_meaningful = len(response_text) > 50 and "trouble" not in response_text.lower()
            print(f"\n5. Response quality:")
            print(f"   📊 Meaningful response: {'✅ YES' if is_meaningful else '❌ NO'}")
            
            if is_meaningful:
                print(f"   🎉 SUCCESS - Server is working correctly!")
            else:
                print(f"   ⚠️  Issue - Response seems to be an error message")
                
        else:
            print(f"   ❌ Chat request failed: {chat_response.status_code}")
            print(f"   📄 Response: {chat_response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to server at {base_url}")
        print(f"   Make sure the server is running with: python all_data.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_formatting_fix()