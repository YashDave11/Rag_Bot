#!/usr/bin/env python3
"""
Multilingual FastAPI server for Qunix Smart Support Platform
Supports multiple languages with auto-detection and translation
"""

import os
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from fastapi import FastAPI, HTTPException, Depends, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

# Import original MongoDB RAG functionality
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np

# Import translation functionality
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Pydantic models
class UserRegistration(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    user_id: str
    email: str
    api_key: str
    created_at: str
    widget_status: str
    message_count: int
    message_limit: int

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    preferred_language: Optional[str] = None  # Optional language preference

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    detected_language: str
    response_language: str
    status: str = "success"

class MultilingualChatEngine:
    """Enhanced chat engine with multilingual support"""
    
    def __init__(self):
        self.setup_gemini()
        self.load_data()
        self.embedding_model = SentenceTransformer("thenlper/gte-small")
        print("🌍 Multilingual Chat Engine initialized!")
    
    def setup_gemini(self):
        """Setup Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCl5ubFeNTdeqmWPu4iYOc97dec6fuCHcc")
        
        try:
            genai.configure(api_key=api_key)
            # Try different model names
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                print("🚀 Gemini API configured successfully with gemini-1.5-pro!")
            except:
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                print("🚀 Gemini API configured successfully with gemini-pro!")
            self.use_gemini = True
        except Exception as e:
            print(f"⚠️  Failed to configure Gemini API: {e}")
            self.use_gemini = False
    
    def load_data(self):
        """Load knowledge base documentation data"""
        data_dir = Path(__file__).parent / "data"
        
        try:
            with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
                self.vector_data = json.load(f)
            
            with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
                self.full_data = json.load(f)
            
            print(f"📚 Loaded {len(self.vector_data)} documents")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.vector_data = []
            self.full_data = []
    
    def detect_and_translate_to_english(self, text: str) -> Tuple[str, str]:
        """
        Detect language and translate to English if needed
        Returns: (translated_text, detected_language)
        """
        try:
            print(f"🔍 Detecting language for: {text}")
            
            # First, try to detect language using a separate detection call
            from deep_translator import single_detection
            try:
                detected_lang = single_detection(text, api_key=None)
                print(f"🌍 Language detected via detection API: {detected_lang}")
            except:
                # Fallback: Use manual detection based on character ranges
                detected_lang = self._detect_language_by_script(text)
                print(f"🌍 Language detected via script analysis: {detected_lang}")
            
            # If already English, return as is
            if detected_lang == 'en':
                print(f"✅ Text is already in English")
                return text, 'en'
            
            # Translate to English
            translator = GoogleTranslator(source=detected_lang, target='en')
            translated = translator.translate(text)
            
            print(f"🔄 Translated to English: {translated}")
            return translated, detected_lang
            
        except Exception as e:
            print(f"❌ Language detection/translation failed: {e}")
            print(f"   Trying fallback method...")
            
            # Fallback: Use auto detection but with better handling
            try:
                translator = GoogleTranslator(source='auto', target='en')
                translated = translator.translate(text)
                
                # Manual detection based on script
                detected_lang = self._detect_language_by_script(text)
                if detected_lang == 'unknown':
                    detected_lang = 'en'  # Default to English
                
                print(f"🔄 Fallback translation successful, detected: {detected_lang}")
                return translated, detected_lang
                
            except Exception as e2:
                print(f"❌ Fallback also failed: {e2}")
                return text, 'en'
    
    def _detect_language_by_script(self, text: str) -> str:
        """Detect language based on character script ranges"""
        # Check for common Indian language scripts
        for char in text:
            # Hindi (Devanagari)
            if '\u0900' <= char <= '\u097F':
                return 'hi'
            # Bengali
            elif '\u0980' <= char <= '\u09FF':
                return 'bn'
            # Tamil
            elif '\u0B80' <= char <= '\u0BFF':
                return 'ta'
            # Telugu
            elif '\u0C00' <= char <= '\u0C7F':
                return 'te'
            # Gujarati
            elif '\u0A80' <= char <= '\u0AFF':
                return 'gu'
            # Kannada
            elif '\u0C80' <= char <= '\u0CFF':
                return 'kn'
            # Malayalam
            elif '\u0D00' <= char <= '\u0D7F':
                return 'ml'
            # Marathi (also uses Devanagari, so same as Hindi)
            # Punjabi (Gurmukhi)
            elif '\u0A00' <= char <= '\u0A7F':
                return 'pa'
        
        # If no Indian scripts found, assume English
        return 'en'
    
    def translate_to_language(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        print(f"🔄 translate_to_language called with target: {target_language}")
        
        # Handle invalid language codes
        if target_language in ['en', 'auto', 'unknown']:
            print(f"✅ Target is English or invalid ({target_language}), returning original text")
            return text
        
        try:
            print(f"🌍 Translating from English to {target_language}...")
            print(f"📝 Original text: {text[:100]}...")
            
            translator = GoogleTranslator(source='en', target=target_language)
            translated = translator.translate(text)
            
            # Verify translation actually happened (not same as original)
            if translated != text:
                print(f"✅ Translation successful!")
                print(f"📝 Translated text: {translated[:100]}...")
                return translated
            else:
                print(f"⚠️  Translation returned same text, may not have worked")
                return text
                
        except Exception as e:
            print(f"❌ Translation to {target_language} failed: {e}")
            print(f"   Returning original English text as fallback")
            return text
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant documents using semantic similarity"""
        if not self.vector_data:
            return []
        
        query_embedding = self.embedding_model.encode(query)
        
        similarities = []
        for i, doc in enumerate(self.vector_data):
            if 'embedding' in doc:
                doc_embedding = doc['embedding']
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append((similarity, i, doc))
        
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, _, doc in similarities[:top_k]]
    
    def _cosine_similarity(self, a, b):
        """Calculate cosine similarity between two vectors"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def generate_response(self, question: str, context: str) -> str:
        """Generate response using Gemini API"""
        if not self.use_gemini:
            return "I'm sorry, the AI service is currently unavailable. Please try again later."
        
        try:
            prompt = f"""You are a helpful College Code of Conduct Assistant. Your role is to provide accurate and concise answers about college rules and regulations. Your responses must be based **solely** on the provided context, which is retrieved from the college's official policies.

USER QUESTION: {question}

COLLEGE CODE OF CONDUCT CONTEXT:
{context}

INSTRUCTIONS:
1. **Relevance Check**: First, determine if the user's question is related to the college's code of conduct, rules, or student policies.

2. **If Related**:
   - Provide a direct and well-structured answer using only the provided context.
   - Use clear headings and bullet points to organize the information.
   - Highlight key rules, specific requirements (like attendance percentages), and the consequences for non-compliance.
   - If the context is insufficient to answer the question, state that the information is not available in the provided document and suggest alternative questions they could ask.

3. **If NOT Related**:
   - Politely acknowledge the question.
   - Gently redirect the user to topics about the college's rules and regulations.
   - Suggest relevant example questions they could ask about the code of conduct.
   - Keep the response brief and friendly.

4. **Response Format**:
   - Use a professional yet friendly tone.
   - Ensure the answer is easy to read and understand.
   - DO NOT use markdown formatting like * or # symbols.
   - Use plain text with line breaks for structure.

5. **Always end with**: A brief suggestion for follow-up questions or related topics they might find useful.


RESPONSE:"""

            response = self.gemini_model.generate_content(prompt)
            # Clean up markdown formatting from the response
            cleaned_response = self.clean_markdown_formatting(response.text)
            return cleaned_response
            
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again in a moment."
    
    def clean_markdown_formatting(self, text: str) -> str:
        """Remove markdown formatting characters from text"""
        import re
        
        # Remove markdown headers (# ## ###)
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
        
        # Remove bold/italic markers (* ** _)
        text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
        text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
        
        # Remove bullet point markers (- * +)
        text = re.sub(r'^[\s]*[-*+]\s*', '• ', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace and normalize line breaks
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Remove excessive line breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Normalize spaces
        text = text.strip()
        
        return text
    
    def process_multilingual_query(self, message: str, preferred_language: Optional[str] = None) -> Tuple[str, str, str]:
        """
        Process a multilingual query and return response
        Returns: (response, detected_language, response_language)
        """
        print(f"\n🔍 Processing query: {message}")
        
        # Step 1: Detect language and translate to English
        english_query, detected_lang = self.detect_and_translate_to_english(message)
        print(f"🌍 Detected language: {detected_lang}")
        print(f"🔄 English query: {english_query}")
        
        # Step 2: Search for relevant documents
        relevant_docs = self.search_documents(english_query)
        print(f"📚 Found {len(relevant_docs)} relevant documents")
        
        # Step 3: Prepare context
        context_parts = []
        for doc in relevant_docs:
            title = doc.get('title', 'Unknown Document')
            body = doc.get('body', '')
            if len(body) > 1000:
                body = body[:1000] + "..."
            context_parts.append(f"Title: {title}\nContent: {body}")
        
        context = "\n\n".join(context_parts) if context_parts else "No specific documentation found."
        
        # Step 4: Generate English response
        print(f"🤖 Generating AI response...")
        english_response = self.generate_response(english_query, context)
        print(f"✅ English response generated: {english_response[:100]}...")
        
        # Step 5: Determine response language (CRITICAL: Use detected language)
        response_language = preferred_language or detected_lang
        print(f"🎯 Target response language: {response_language}")
        
        # Step 6: CRITICAL - Always translate if not English
        if response_language != 'en':
            print(f"🔄 TRANSLATING response to {response_language}...")
            final_response = self.translate_to_language(english_response, response_language)
        else:
            print(f"✅ Response language is English, no translation needed")
            final_response = english_response
        
        print(f"🎉 Final response ready in {response_language}")
        return final_response, detected_lang, response_language

# Initialize the multilingual chat engine
chat_engine = MultilingualChatEngine()

# FastAPI app
app = FastAPI(
    title="Qunix Smart Support API",
    description="Multilingual AI Assistant with smart support capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple user storage (in production, use a proper database)
users_db = {}
sessions_db = {}

def generate_api_key(email: str) -> str:
    """Generate a unique API key for user"""
    timestamp = str(datetime.now().timestamp())
    raw_key = f"{email}:{timestamp}:{uuid.uuid4()}"
    return hashlib.sha256(raw_key.encode()).hexdigest()[:32]

def get_user_by_api_key(api_key: str) -> Optional[Dict]:
    """Get user by API key"""
    for user_id, user_data in users_db.items():
        if user_data.get("api_key") == api_key:
            return user_data
    return None

@app.post("/register", response_model=UserResponse)
async def register_user(user_data: UserRegistration):
    """Register a new user"""
    email = user_data.email
    
    # Check if user already exists
    for user_id, existing_user in users_db.items():
        if existing_user["email"] == email:
            return UserResponse(**existing_user)
    
    # Create new user
    user_id = str(uuid.uuid4())
    api_key = generate_api_key(email)
    
    new_user = {
        "user_id": user_id,
        "email": email,
        "api_key": api_key,
        "created_at": datetime.now().isoformat(),
        "widget_status": "active",
        "message_count": 0,
        "message_limit": 100  # Free tier limit
    }
    
    users_db[user_id] = new_user
    
    return UserResponse(**new_user)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_data: ChatMessage,
    api_key: str = Cookie(None)
):
    """Process multilingual chat message"""
    
    # For demo purposes, allow requests without API key
    if api_key:
        user = get_user_by_api_key(api_key)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # Check message limit
        if user["message_count"] >= user["message_limit"]:
            raise HTTPException(status_code=429, detail="Message limit exceeded")
        
        # Increment message count
        user["message_count"] += 1
    
    # Generate session ID if not provided
    session_id = chat_data.session_id or str(uuid.uuid4())
    
    try:
        # Process the multilingual query
        response, detected_lang, response_lang = chat_engine.process_multilingual_query(
            chat_data.message, 
            chat_data.preferred_language
        )
        
        # Store session data
        sessions_db[session_id] = {
            "messages": sessions_db.get(session_id, {}).get("messages", []) + [
                {"user": chat_data.message, "assistant": response, "timestamp": datetime.now().isoformat()}
            ]
        }
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            detected_language=detected_lang,
            response_language=response_lang
        )
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "multilingual_support": True,
        "gemini_available": chat_engine.use_gemini,
        "documents_loaded": len(chat_engine.vector_data),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages"""
    # Common languages supported by Google Translate
    supported_languages = {
        "en": "English",
        "hi": "Hindi",
        "bn": "Bengali", 
        "ta": "Tamil",
        "te": "Telugu",
        "mr": "Marathi",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ml": "Malayalam",
        "pa": "Punjabi",
        "or": "Odia",
        "as": "Assamese",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ar": "Arabic"
    }
    
    return {
        "supported_languages": supported_languages,
        "auto_detection": True,
        "note": "The system automatically detects the input language and responds in the same language"
    }

if __name__ == "__main__":
    import uvicorn
    print("🌍 Starting Qunix Smart Support API Server...")
    print("📚 Knowledge base documentation loaded")
    print("🤖 AI assistant ready")
    print("🔗 Server will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)