import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Test the newer models that should work
test_models = [
    'gemini-2.5-flash',
    'gemini-2.0-flash',
    'gemini-flash-latest',
    'gemini-pro-latest'
]

print("Testing newer model availability:")
for model_name in test_models:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, test message")
        print(f"✅ {model_name} - Works! Response: {response.text[:50]}...")
    except Exception as e:
        print(f"❌ {model_name} - Error: {str(e)[:100]}...")