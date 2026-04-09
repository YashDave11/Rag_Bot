#!/usr/bin/env python3
"""
Simple test to verify server setup
"""

import requests
import json

def test_server():
    print("🧪 Testing ChatMongo SaaS API Server...")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Server is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Server error: {response.status_code}")
            return
        
        # Test 2: Health check detailed
        print("\n2. Testing detailed health...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
        
        # Test 3: Registration
        print("\n3. Testing user registration...")
        test_email = "test@example.com"
        response = requests.post(
            f"{base_url}/auth/register",
            json={"email": test_email},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("   ✅ Registration successful")
            user_data = response.json()
            print(f"   User ID: {user_data['user_id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   API Key: {user_data['api_key']}")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
        
        print("\n🎉 Server test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server!")
        print("   Make sure the server is running:")
        print("   python start_phase1_server.py")
        print("   or")
        print("   python enhanced_api_server.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_server()