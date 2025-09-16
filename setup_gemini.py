#!/usr/bin/env python3
"""
Setup script for Gemini API key
"""

import os

def setup_gemini_api():
    """Setup Gemini API key"""
    print("🔑 Gemini API Key Setup")
    print("=" * 40)
    
    # Check if API key is already set
    current_key = os.getenv('GEMINI_API_KEY')
    if current_key:
        print(f"✅ API key is already set: {current_key[:10]}...")
        choice = input("Do you want to update it? (y/n): ").lower()
        if choice != 'y':
            print("👍 Keeping existing API key")
            return
    
    print("\n📝 To get your Gemini API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated key")
    
    api_key = input("\n🔑 Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    # Set environment variable for current session
    os.environ['GEMINI_API_KEY'] = api_key
    
    # Create a batch file to set it permanently on Windows
    batch_content = f'@echo off\nset GEMINI_API_KEY={api_key}\necho ✅ Gemini API key set for this session\n'
    
    with open('set_gemini_key.bat', 'w') as f:
        f.write(batch_content)
    
    print(f"✅ API key set for current session")
    print(f"📁 Created 'set_gemini_key.bat' for future sessions")
    print(f"💡 Run 'set_gemini_key.bat' before starting the agent in new terminals")
    
    # Test the API key
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello!")
        print(f"🧪 API test successful: {response.text[:50]}...")
    except Exception as e:
        print(f"⚠️  API test failed: {e}")
        print("Please check your API key and try again")

if __name__ == "__main__":
    setup_gemini_api()