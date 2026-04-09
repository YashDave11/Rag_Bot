#!/usr/bin/env python3
"""
Test script for multilingual translation functionality
"""

from deep_translator import GoogleTranslator

def translate_to_english(text: str) -> str:
    """Translate text to English"""
    try:
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(text)
        return translated
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")

def detect_language_and_translate(text: str):
    """Detect language and translate to English"""
    try:
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(text)
        detected_lang = translator.source
        return translated, detected_lang
    except Exception as e:
        print(f"Translation error: {e}")
        return text, 'unknown'

def translate_from_english(text: str, target_lang: str) -> str:
    """Translate from English to target language"""
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

if __name__ == "__main__":
    print("🧪 Testing Multilingual Translation")
    print("=" * 50)
    
    # Test examples from your reference
    examples = [
        "I am Vishesh Jain",
        "मुझे चाय पीना बहुत पसंद है।",
        "আজ আকাশটা খুব সুন্দর লাগছে।", 
        "நான் புத்தகம் படிக்க விரும்புகிறேன்",
        "నేడు వాతావరణం చల్లగా ఉంది",
        "मला माझ्या मित्रांसोबत खेळायला आवडते"
    ]
    
    for ex in examples:
        print(f"\nOriginal: {ex}")
        
        # Test basic translation
        try:
            translated = translate_to_english(ex)
            print(f"Translated: {translated}")
        except Exception as e:
            print(f"Translation failed: {e}")
        
        # Test language detection
        translated, lang = detect_language_and_translate(ex)
        print(f"Detected language: {lang}")
        print(f"English version: {translated}")
        
        # Test translating back
        if lang != 'en' and lang != 'unknown':
            back_translated = translate_from_english("Hi!! How can I help you today?", lang)
            print(f"MongoDB greeting in {lang}: {back_translated}")
        
        print("-" * 50)
    
    print("\n🎯 Testing MongoDB-related queries:")
    mongodb_queries = [
        "What is MongoDB?",
        "MongoDB क्या है?",
        "MongoDB কি?",
        "MongoDB என்றால் என்ன?",
        "MongoDB అంటే ఏమిటి?"
    ]
    
    for query in mongodb_queries:
        translated, lang = detect_language_and_translate(query)
        print(f"\nQuery: {query}")
        print(f"Language: {lang}")
        print(f"English: {translated}")
        
        # Simulate response translation
        english_response = "MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents."
        if lang != 'en':
            translated_response = translate_from_english(english_response, lang)
            print(f"Response in {lang}: {translated_response}")