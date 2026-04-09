#!/usr/bin/env python3
"""
Test script to verify the improved language detection and translation
"""

def detect_language_by_script(text: str) -> str:
    """Detect language based on character script ranges"""
    print(f"🔍 Analyzing script for: {text}")
    
    # Check for common Indian language scripts
    for char in text:
        # Hindi (Devanagari)
        if '\u0900' <= char <= '\u097F':
            print(f"   Found Devanagari character: {char}")
            return 'hi'
        # Bengali
        elif '\u0980' <= char <= '\u09FF':
            print(f"   Found Bengali character: {char}")
            return 'bn'
        # Tamil
        elif '\u0B80' <= char <= '\u0BFF':
            print(f"   Found Tamil character: {char}")
            return 'ta'
        # Telugu
        elif '\u0C00' <= char <= '\u0C7F':
            print(f"   Found Telugu character: {char}")
            return 'te'
        # Gujarati
        elif '\u0A80' <= char <= '\u0AFF':
            print(f"   Found Gujarati character: {char}")
            return 'gu'
        # Kannada
        elif '\u0C80' <= char <= '\u0CFF':
            print(f"   Found Kannada character: {char}")
            return 'kn'
        # Malayalam
        elif '\u0D00' <= char <= '\u0D7F':
            print(f"   Found Malayalam character: {char}")
            return 'ml'
        # Punjabi (Gurmukhi)
        elif '\u0A00' <= char <= '\u0A7F':
            print(f"   Found Punjabi character: {char}")
            return 'pa'
    
    print(f"   No Indian script characters found, assuming English")
    return 'en'

def test_script_detection():
    """Test the script-based language detection"""
    
    print("🧪 Testing Script-Based Language Detection")
    print("=" * 60)
    
    test_cases = [
        {
            "text": "कॉलेज के नियम क्या हैं?",
            "expected": "hi",
            "description": "Hindi (Devanagari)"
        },
        {
            "text": "কলেজের নিয়ম কী?",
            "expected": "bn",
            "description": "Bengali"
        },
        {
            "text": "கல்லூரி விதிகள் என்ன?",
            "expected": "ta",
            "description": "Tamil"
        },
        {
            "text": "కాలేజీ నియమాలు ఏమిటి?",
            "expected": "te",
            "description": "Telugu"
        },
        {
            "text": "What are the college rules?",
            "expected": "en",
            "description": "English"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"Text: {test_case['text']}")
        
        detected = detect_language_by_script(test_case['text'])
        expected = test_case['expected']
        
        if detected == expected:
            print(f"✅ PASS: Detected '{detected}' (expected '{expected}')")
        else:
            print(f"❌ FAIL: Detected '{detected}' (expected '{expected}')")
        
        print("-" * 40)

def test_translation_with_proper_detection():
    """Test translation using proper language detection"""
    
    print(f"\n🌐 Testing Translation with Proper Detection")
    print("=" * 60)
    
    from deep_translator import GoogleTranslator
    
    # Sample English response
    english_response = """Based on the college code of conduct, here are the key rules:

## Attendance Requirements
- Students must maintain at least 75% attendance
- Regular attendance is mandatory for all classes

## Academic Conduct  
- Plagiarism is strictly prohibited
- All assignments must be original work

## Campus Behavior
- Respectful behavior is expected
- Mobile phones should be on silent during classes

For more information, contact the administration office."""
    
    test_cases = [
        {
            "query": "कॉलेज के नियम क्या हैं?",
            "lang_code": "hi",
            "description": "Hindi"
        },
        {
            "query": "কলেজের নিয়ম কী?",
            "lang_code": "bn", 
            "description": "Bengali"
        },
        {
            "query": "கல்லூரி விதிகள் என்ன?",
            "lang_code": "ta",
            "description": "Tamil"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        
        # Detect language using script analysis
        detected_lang = detect_language_by_script(test_case['query'])
        print(f"🌍 Script-detected language: {detected_lang}")
        
        if detected_lang != 'en' and detected_lang == test_case['lang_code']:
            try:
                # Translate response to detected language
                print(f"🔄 Translating response to {detected_lang}...")
                translator = GoogleTranslator(source='en', target=detected_lang)
                translated_response = translator.translate(english_response)
                
                print(f"✅ Translation successful!")
                print(f"📝 Translated response preview:")
                print(f"   {translated_response[:200]}...")
                
                # Check if actually translated (different from English)
                if translated_response != english_response:
                    print(f"✅ Response successfully translated to {detected_lang}")
                else:
                    print(f"⚠️  Response appears same as English")
                    
            except Exception as e:
                print(f"❌ Translation failed: {e}")
        else:
            print(f"⚠️  Language detection mismatch or English detected")
        
        print("-" * 50)

def test_api_with_fix():
    """Test the API with the language detection fix"""
    
    print(f"\n🌐 Testing API with Language Detection Fix")
    print("=" * 60)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    # Test with Tamil query (which was failing before)
    test_query = "கல்லூரி விதிகள் என்ன?"
    
    try:
        print(f"🔍 Testing with Tamil query: {test_query}")
        
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
            
            # Check if response contains Tamil characters
            response_text = data.get('response', '')
            has_tamil_chars = any('\u0B80' <= char <= '\u0BFF' for char in response_text)
            
            if has_tamil_chars:
                print(f"✅ Response contains Tamil characters - Translation working!")
            else:
                print(f"⚠️  Response doesn't contain Tamil characters")
                print(f"   Detected language was: {data.get('detected_language')}")
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print(f"   Make sure server is running: python multilingual_api_server.py")

if __name__ == "__main__":
    # Test script-based detection
    test_script_detection()
    
    # Test translation with proper detection
    test_translation_with_proper_detection()
    
    # Test API
    test_api_with_fix()
    
    print(f"\n🎯 Language Detection Fix Test Complete!")
    print(f"💡 The script-based detection should now properly identify Tamil as 'ta' instead of 'auto'")