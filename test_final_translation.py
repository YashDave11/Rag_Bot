#!/usr/bin/env python3
"""
Test script to specifically verify final translation from English to source language
"""

from deep_translator import GoogleTranslator

def test_translation_directly():
    """Test the translation functionality directly"""
    
    print("🧪 Testing Direct Translation Functionality")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "input": "कॉलेज के नियम क्या हैं?",
            "expected_lang": "hi",
            "description": "Hindi query about college rules"
        },
        {
            "input": "কলেজের নিয়ম কী?",
            "expected_lang": "bn",
            "description": "Bengali query about college rules"
        },
        {
            "input": "கல்லூரி விதிகள் என்ன?",
            "expected_lang": "ta",
            "description": "Tamil query about college rules"
        }
    ]
    
    # Sample English response (like what Gemini would generate)
    english_response = """Based on the college code of conduct, here are the key rules:

## Attendance Requirements
- Students must maintain at least 75% attendance
- Regular attendance is mandatory for all classes

## Academic Conduct
- Plagiarism is strictly prohibited
- All assignments must be original work
- Cheating in exams will result in disciplinary action

## Campus Behavior
- Respectful behavior towards faculty and peers is expected
- Mobile phones should be on silent during classes
- Smoking and alcohol are prohibited on campus

For more specific information, please refer to the student handbook or contact the administration office."""
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"Input: {test_case['input']}")
        
        try:
            # Step 1: Detect language and translate to English
            print(f"📝 Step 1: Language Detection & Translation to English")
            translator_to_en = GoogleTranslator(source='auto', target='en')
            english_query = translator_to_en.translate(test_case['input'])
            detected_lang = translator_to_en.source
            
            print(f"   🌍 Detected language: {detected_lang}")
            print(f"   🔄 English query: {english_query}")
            
            # Step 2: Translate response back to source language
            print(f"📝 Step 2: Translating Response Back to {detected_lang}")
            
            if detected_lang != 'en':
                translator_back = GoogleTranslator(source='en', target=detected_lang)
                translated_response = translator_back.translate(english_response)
                
                print(f"   ✅ Translation successful!")
                print(f"   📝 Translated response preview:")
                print(f"   {translated_response[:200]}...")
                
                # Verify it's actually translated (not same as English)
                if translated_response != english_response:
                    print(f"   ✅ Response successfully translated to {detected_lang}")
                else:
                    print(f"   ⚠️  Response appears to be same as English")
            else:
                print(f"   ✅ Language is English, no translation needed")
                
        except Exception as e:
            print(f"   ❌ Translation failed: {e}")
        
        print("-" * 50)

def test_api_translation():
    """Test the API translation"""
    import requests
    
    print(f"\n🌐 Testing API Translation")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test with Hindi query
    test_query = "कॉलेज के नियम क्या हैं?"
    
    try:
        print(f"🔍 Testing with Hindi query: {test_query}")
        
        response = requests.post(
            f"{base_url}/chat",
            json={"message": test_query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ API Response received")
            print(f"🌍 Detected language: {data.get('detected_language')}")
            print(f"🎯 Response language: {data.get('response_language')}")
            print(f"📝 Response preview: {data.get('response', '')[:200]}...")
            
            # Check if response is in Hindi (contains Devanagari script)
            response_text = data.get('response', '')
            has_hindi_chars = any('\u0900' <= char <= '\u097F' for char in response_text)
            
            if has_hindi_chars:
                print(f"✅ Response contains Hindi characters - Translation working!")
            else:
                print(f"⚠️  Response doesn't contain Hindi characters - May not be translated")
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Make sure server is running: python multilingual_api_server.py")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print(f"   Make sure server is running: python multilingual_api_server.py")

if __name__ == "__main__":
    # Test direct translation first
    test_translation_directly()
    
    # Then test API
    test_api_translation()
    
    print(f"\n🎯 Translation Test Complete!")
    print(f"💡 If API test fails, make sure to run: python multilingual_api_server.py")