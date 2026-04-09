#!/usr/bin/env python3
"""
Test script to check available Gemini models
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return
    
    genai.configure(api_key=api_key)
    
    # List available models
    print("🔍 Available models:")
    try:
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  ✅ {model.name}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
    
    # Test specific model names
    test_model_names = [
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest', 
        'gemini-1.5-pro',
        'gemini-1.5-pro-latest',
        'gemini-pro'
    ]
    
    print("\n🧪 Testing model names:")
    for model_name in test_model_names:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"  ✅ {model_name} - Working!")
        except Exception as e:
            print(f"  ❌ {model_name} - Error: {e}")

if __name__ == "__main__":
    test_models()