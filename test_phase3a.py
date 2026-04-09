#!/usr/bin/env python3
"""
Quick test for Phase 3A API
"""

import requests
import json

def test_api():
    print("🧪 Testing Phase 3A API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Basic health check
        print("\n1. Testing API health...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ API is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ API error: {response.status_code}")
            return
        
        # Test 2: Health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
        
        print("\n✅ API server is working correctly!")
        print("Now try uploading a PDF through the dashboard.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server!")
        print("Make sure to run: python phase3a_api_server.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_api()