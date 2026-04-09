#!/usr/bin/env python3
"""
Multilingual FastAPI server for College Webpage Chatbot
Uses embeddings from webpage chunks to answer questions.
"""

import os
import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Tuple

from fastapi import FastAPI, HTTPException, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np
from deep_translator import GoogleTranslator

# ================== CONFIG ==================
EMBEDDINGS_FILE = "webpages_embeddings.json"   # from Python 01
MODEL_NAME = "thenlper/gte-small"

# Load environment variables
load_dotenv()

# ================== Pydantic Models ==================
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
    preferred_language: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    detected_language: str
    response_language: str
    status: str = "success"

# ================== Chat Engine ==================
class MultilingualChatEngine:
    def __init__(self):
        self.setup_gemini()
        self.embedding_model = SentenceTransformer(MODEL_NAME)
        self.load_data()
        print("🌍 Multilingual Chat Engine initialized with webpage embeddings!")

    def setup_gemini(self):
        """Setup Gemini API with working models"""
        api_key = os.getenv("GEMINI_API_KEY")
        try:
            genai.configure(api_key=api_key)
            # Use Gemini 2.5 Flash which is confirmed working
            try:
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                # Test the model
                test_response = self.gemini_model.generate_content("Hello")
                print("Gemini API configured successfully with gemini-2.5-flash!")
            except Exception as e:
                print(f"Failed gemini-2.5-flash: {str(e)[:80]}")
                try:
                    self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                    test_response = self.gemini_model.generate_content("Hello")
                    print("Gemini API configured successfully with gemini-2.0-flash!")
                except Exception as e2:
                    print(f"Failed gemini-2.0-flash: {str(e2)[:80]}")
                    self.gemini_model = genai.GenerativeModel('gemini-flash-latest')
                    print("Gemini API configured successfully with gemini-flash-latest!")
            self.use_gemini = True
        except Exception as e:
            print(f"Gemini API setup failed: {e}")
            self.use_gemini = False

    def load_data(self):
        """Load webpage embeddings"""
        try:
            with open(Path(__file__).parent / EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            # Flatten chunks
            self.vector_data = []
            for page in raw_data:
                for chunk in page.get("chunks", []):
                    self.vector_data.append({
                        "url": page["url"],
                        "text": chunk["text"],
                        "embedding": chunk["embedding"]
                    })

            print(f"📚 Loaded {len(self.vector_data)} chunks from {EMBEDDINGS_FILE}")
        except Exception as e:
            print(f"❌ Error loading embeddings: {e}")
            self.vector_data = []

    def search_documents(self, query: str, top_k: int = 5, similarity_threshold: float = 0.3) -> List[Dict]:
        """Search for relevant chunks using semantic similarity with quality filtering"""
        if not self.vector_data:
            return []

        query_embedding = self.embedding_model.encode(query)
        similarities = []
        
        for i, doc in enumerate(self.vector_data):
            doc_embedding = doc["embedding"]
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            
            # Only include documents above similarity threshold
            if similarity >= similarity_threshold:
                similarities.append((similarity, doc))

        # Sort by similarity score
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Log search results for debugging
        print(f"🔍 Search results for query: '{query}'")
        for i, (score, doc) in enumerate(similarities[:top_k]):
            print(f"  {i+1}. Score: {score:.3f} - Text: {doc['text'][:100]}...")
        
        if not similarities:
            print(f"⚠️ No documents found above similarity threshold {similarity_threshold}")
            return []
            
        return [doc for _, doc in similarities[:top_k]]

    def _cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _is_response_relevant(self, question: str, response: str) -> bool:
        """Check if the generated response is actually relevant to the question"""
        # Simple relevance check - look for key indicators
        irrelevant_phrases = [
            "I don't have this information",
            "I don't have enough information", 
            "I couldn't find",
            "not available in the provided documents",
            "I apologize, but I don't have"
        ]
        
        response_lower = response.lower()
        return not any(phrase in response_lower for phrase in irrelevant_phrases)

    def generate_response(self, question: str, context: str, has_relevant_context: bool = True) -> str:
        """Generate response using Gemini API with strict hallucination prevention"""
        if not self.use_gemini:
            return "The AI service is unavailable right now."

        try:
            if not has_relevant_context:
                return f"""I apologize, but I couldn't find relevant information in the college documents to answer your question: "{question}"

This might be because:
- The information isn't available in the current documents
- The question might need to be more specific
- The topic might not be covered in the college materials

To get better help, you could try asking about:
- College admission requirements and procedures
- Academic programs and course details
- Campus facilities and services
- Student policies and code of conduct
- Fee structure and scholarship information
- Faculty and department information

Please try rephrasing your question with more specific terms or ask about the topics listed above."""
            prompt = f"""You are an expert College Information Assistant. Your sole function is to answer user questions with concise, accurate information found ONLY in the provided `CONTEXT`.

Core Directives:
1.  Synthesize and Summarize: Do not copy-paste long passages. Read the `CONTEXT` and synthesize the key information into a brief, direct answer.
2.  Be Decisive: Answer the question directly. Omit filler phrases and unnecessary background information.
3.  Strict Sourcing: Base every part of your answer on the provided `CONTEXT`. Do not infer, assume, or use any outside knowledge.

Handling Missing Information:
- If the `CONTEXT` does not contain the information needed to answer the `QUESTION`, you MUST respond with the exact phrase: "I don't have this information in the provided documents."

Formatting:
- Use plain text only.
- Do not use markdown (like #, *, or lists).
- Use simple line breaks for readability.

---
USER QUESTION:
`{question}`

CONTEXT:
`{context}`

ANSWER:"""
            response = self.gemini_model.generate_content(prompt)
            # Clean up markdown formatting from the response
            cleaned_response = self.clean_markdown_formatting(response.text)
            return cleaned_response
        except Exception as e:
            print(f"⚠ Gemini API error: {e}")
            return "I’m having trouble generating an answer right now."

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
            
            # Validate translation quality
            if not self._validate_translation_quality(text, translated, detected_lang):
                print(f"⚠️ Translation quality check failed, using original text")
                return text, 'en'  # Treat as English if translation fails
            
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

    def _validate_translation_quality(self, original: str, translated: str, detected_lang: str) -> bool:
        """Validate if translation seems reasonable"""
        if not translated or translated.strip() == "":
            return False
        
        # If languages are the same, translation should be identical
        if detected_lang == 'en' and original != translated:
            return False
            
        # Check if translation is suspiciously short compared to original
        if len(translated) < len(original) * 0.3:
            return False
            
        return True

    def _keyword_search_fallback(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fallback keyword-based search when semantic search fails"""
        if not self.vector_data:
            return []
            
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.vector_data:
            text = doc["text"].lower()
            # Count keyword matches
            matches = sum(1 for word in query_words if word in text)
            if matches > 0:
                score = matches / len(query_words)  # Percentage of query words found
                scored_docs.append((score, doc))
        
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        print(f"🔍 Keyword fallback found {len(scored_docs)} documents")
        
        return [doc for _, doc in scored_docs[:top_k]]

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

    def process_multilingual_query(self, message: str, session_id: str = None, conversation_history: List[Dict] = None, preferred_language: Optional[str] = None) -> Tuple[str, str, str]:
        """
        Process a multilingual query with conversation context
        Returns: (response, detected_language, response_language)
        """
        print(f"\n🔍 Processing query: {message}")
        print(f"📝 Session ID: {session_id}")
        print(f"💬 Conversation history length: {len(conversation_history) if conversation_history else 0}")
        
        # Step 1: Detect language and translate to English
        english_query, detected_lang = self.detect_and_translate_to_english(message)
        print(f"🌍 Detected language: {detected_lang}")
        print(f"🔄 English query: {english_query}")

        # Step 2: Search for relevant documents with quality filtering
        relevant_docs = self.search_documents(english_query, top_k=5, similarity_threshold=0.3)
        print(f"📚 Found {len(relevant_docs)} relevant documents")
        
        # Step 2b: If semantic search fails, try keyword-based fallback
        if len(relevant_docs) == 0:
            print(f"🔄 Trying keyword-based fallback search...")
            relevant_docs = self._keyword_search_fallback(english_query, top_k=3)
            print(f"📚 Fallback search found {len(relevant_docs)} documents")
        
        # Step 3: Validate context quality and prepare context
        has_relevant_context = len(relevant_docs) > 0
        
        if has_relevant_context:
            # Filter and prepare high-quality context
            context_parts = []
            for doc in relevant_docs:
                text = doc["text"].strip()
                if len(text) > 20:  # Filter out very short chunks
                    context_parts.append(f"Source: {doc.get('url', 'Unknown')}\nContent: {text}")
            
            context = "\n\n---\n\n".join(context_parts) if context_parts else "No relevant documents found."
            print(f"📝 Context prepared with {len(context_parts)} quality chunks")
        else:
            context = "No relevant documents found."
            print(f"⚠️ No relevant context found for query")

        # Step 4: Generate English response with context validation and conversation history
        print(f"🤖 Generating AI response with conversation context...")
        english_response = self.generate_response_with_context(english_query, context, conversation_history, has_relevant_context)
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

    def generate_response_with_context(self, question: str, context: str, conversation_history: List[Dict] = None, has_relevant_context: bool = True) -> str:
        """Generate response using Gemini API with conversation context and strict hallucination prevention"""
        if not self.use_gemini:
            return "The AI service is unavailable right now."

        try:
            if not has_relevant_context:
                return f"""I apologize, but I couldn't find relevant information in the college documents to answer your question: "{question}"

This might be because:
- The information isn't available in the current documents
- The question might need to be more specific
- The topic might not be covered in the college materials

To get better help, you could try asking about:
- College admission requirements and procedures
- Academic programs and course details
- Campus facilities and services
- Student policies and code of conduct
- Fee structure and scholarship information
- Faculty and department information

Please try rephrasing your question with more specific terms or ask about the topics listed above."""

            # Prepare conversation history for context
            conversation_context = ""
            if conversation_history and len(conversation_history) > 0:
                print(f"📚 Including {len(conversation_history)} previous messages for context")
                recent_messages = conversation_history[-3:]  # Last 3 exchanges for context
                conversation_parts = []
                for msg in recent_messages:
                    conversation_parts.append(f"User: {msg.get('user_message', '')}")
                    conversation_parts.append(f"Assistant: {msg.get('bot_response', '')}")
                conversation_context = "\n".join(conversation_parts)
            
            prompt = f"""You are an expert College Information Assistant. Your sole function is to answer user questions with concise, accurate information found ONLY in the provided `CONTEXT`.

Core Directives:
1.  Synthesize and Summarize: Do not copy-paste long passages. Read the `CONTEXT` and synthesize the key information into a brief, direct answer.
2.  Be Decisive: Answer the question directly. Omit filler phrases and unnecessary background information.
3.  Strict Sourcing: Base every part of your answer on the provided `CONTEXT`. Do not infer, assume, or use any outside knowledge.
4.  Conversation Awareness: Use the conversation history to understand context and avoid repeating information, but still base your answer on the provided CONTEXT.

Handling Missing Information:
- If the `CONTEXT` does not contain the information needed to answer the `QUESTION`, you MUST respond with the exact phrase: "I don't have this information in the provided documents."

Formatting:
- Use plain text only.
- Do not use markdown (like #, *, or lists).
- Use simple line breaks for readability.

---
CONVERSATION HISTORY:
{conversation_context}

CURRENT USER QUESTION:
`{question}`

CONTEXT:
`{context}`

ANSWER:"""
            response = self.gemini_model.generate_content(prompt)
            # Clean up markdown formatting from the response
            cleaned_response = self.clean_markdown_formatting(response.text)
            return cleaned_response
        except Exception as e:
            print(f"⚠ Gemini API error: {e}")
            return "I'm having trouble generating an answer right now."

# ================== FastAPI Setup ==================
chat_engine = MultilingualChatEngine()
app = FastAPI(title="College Webpage Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    print("🚀 College Webpage Chatbot API starting up...")
    print(f"📚 Loaded {len(chat_engine.vector_data)} document chunks")
    print(f"🤖 Gemini AI: {'Available' if chat_engine.use_gemini else 'Unavailable'}")
    print("💬 Context maintenance: Enabled")
    print("🌍 Multilingual support: Enabled")
    
    # Clean up any existing sessions on startup
    cleanup_old_sessions()
    print("✅ Startup complete!")

users_db = {}
sessions_db = {}

def generate_api_key(email: str) -> str:
    timestamp = str(datetime.now().timestamp())
    raw_key = f"{email}:{timestamp}:{uuid.uuid4()}"
    return hashlib.sha256(raw_key.encode()).hexdigest()[:32]

def cleanup_old_sessions():
    """Clean up sessions older than 24 hours"""
    current_time = datetime.now()
    sessions_to_remove = []
    
    for session_id, session_data in sessions_db.items():
        try:
            last_activity = datetime.fromisoformat(session_data["last_activity"])
            if (current_time - last_activity).total_seconds() > 24 * 3600:  # 24 hours
                sessions_to_remove.append(session_id)
        except:
            # If there's an issue with the timestamp, remove the session
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        del sessions_db[session_id]
    
    if sessions_to_remove:
        print(f"🧹 Cleaned up {len(sessions_to_remove)} old sessions")
    
    return len(sessions_to_remove)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_data: ChatMessage, api_key: str = Cookie(None)):
    session_id = chat_data.session_id or str(uuid.uuid4())
    
    # Get or create session history
    if session_id not in sessions_db:
        sessions_db[session_id] = {
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
    
    # Get conversation history for context
    conversation_history = sessions_db[session_id]["messages"]
    
    # Process the query with conversation context
    response, detected_lang, response_lang = chat_engine.process_multilingual_query(
        chat_data.message, 
        session_id=session_id,
        conversation_history=conversation_history,
        preferred_language=chat_data.preferred_language
    )
    
    # Store the conversation in session history
    message_entry = {
        "user_message": chat_data.message,
        "bot_response": response,
        "timestamp": datetime.now().isoformat(),
        "detected_language": detected_lang,
        "response_language": response_lang
    }
    
    sessions_db[session_id]["messages"].append(message_entry)
    sessions_db[session_id]["last_activity"] = datetime.now().isoformat()
    
    # Keep only last 10 exchanges to prevent memory issues
    if len(sessions_db[session_id]["messages"]) > 10:
        sessions_db[session_id]["messages"] = sessions_db[session_id]["messages"][-10:]
    
    print(f"💾 Session {session_id} now has {len(sessions_db[session_id]['messages'])} messages")

    return ChatResponse(
        response=response,
        session_id=session_id,
        timestamp=datetime.now().isoformat(),
        detected_language=detected_lang,
        response_language=response_lang
    )

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get conversation history for a session"""
    if session_id in sessions_db:
        return {
            "session_id": session_id,
            "messages": sessions_db[session_id]["messages"],
            "created_at": sessions_db[session_id]["created_at"],
            "last_activity": sessions_db[session_id]["last_activity"],
            "message_count": len(sessions_db[session_id]["messages"])
        }
    else:
        return {
            "session_id": session_id,
            "messages": [],
            "message_count": 0,
            "error": "Session not found"
        }

@app.delete("/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear conversation history for a session"""
    if session_id in sessions_db:
        del sessions_db[session_id]
        return {"message": f"Session {session_id} cleared successfully"}
    else:
        return {"message": f"Session {session_id} not found"}

@app.post("/admin/cleanup-sessions")
async def manual_cleanup_sessions():
    """Manually trigger session cleanup"""
    cleaned_count = cleanup_old_sessions()
    return {
        "message": "Session cleanup completed",
        "sessions_cleaned": cleaned_count,
        "active_sessions": len(sessions_db),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    # Auto cleanup on health check (lightweight maintenance)
    cleanup_old_sessions()
    
    return {
        "status": "healthy",
        "documents_loaded": len(chat_engine.vector_data),
        "gemini_available": chat_engine.use_gemini,
        "multilingual_support": True,
        "context_maintenance": True,
        "active_sessions": len(sessions_db),
        "total_messages": sum(len(session["messages"]) for session in sessions_db.values()),
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

@app.get("/embed.js")
async def get_embed_script():
    """Serve the embed script with updated red styling"""
    embed_script = '''/**
 * Quinx Chat Widget - Embeddable Script with Red Styling
 * Add this script to any website to embed the chat widget
 */

(function () {
  "use strict";

  // Configuration
  const WIDGET_CONFIG = {
    apiUrl: "http://localhost:8000",
    version: "2.0.0",
  };

  // Get script tag attributes for configuration
  function getScriptConfig() {
    const scripts = document.querySelectorAll(
      'script[src*="embed.js"], script[data-quinx-chat-id]'
    );
    const script = scripts[scripts.length - 1]; // Get the current script

    return {
      apiUrl: script.getAttribute("data-api-url") || WIDGET_CONFIG.apiUrl,
      chatId: script.getAttribute("data-quinx-chat-id") || "default",
      user: script.getAttribute("data-user") || "",
      bubbleColor: script.getAttribute("data-bubble-color") || "#dc3545", // Red color
      bubbleIcon: decodeURIComponent(script.getAttribute("data-bubble-icon") || "💬"),
      position: script.getAttribute("data-bubble-position") || "bottom-right",
      title: script.getAttribute("data-title") || "Quinx Smart Support",
      subtitle: script.getAttribute("data-subtitle") || "Hi!! How can I help you today?",
    };
  }

  // Create widget container
  function createWidgetContainer(config) {
    const container = document.createElement("div");
    container.id = "quinx-chat-widget-" + Date.now();
    container.style.cssText = `
      position: fixed;
      z-index: 999999;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
      ${getPositionStyles(config.position)}
    `;

    document.body.appendChild(container);
    return container;
  }

  // Get position styles based on configuration
  function getPositionStyles(position) {
    const positions = {
      "bottom-right": "bottom: 20px; right: 20px;",
      "bottom-left": "bottom: 20px; left: 20px;",
      "top-right": "top: 20px; right: 20px;",
      "top-left": "top: 20px; left: 20px;",
    };
    return positions[position] || positions["bottom-right"];
  }

  // Create the chat widget HTML with red styling
  function createChatWidget(config) {
    return `
      <div id="chat-widget" style="position: relative;">
        <!-- Chat Toggle Button with Red Styling -->
        <button id="chat-toggle" style="
          width: 64px;
          height: 64px;
          border-radius: 50%;
          background: linear-gradient(135deg, ${config.bubbleColor}, #b02a37);
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          overflow: hidden;
        ">
          ${config.bubbleIcon}
        </button>

        <!-- Chat Window with Red Theme -->
        <div id="chat-window" style="
          position: absolute;
          bottom: 80px;
          right: 0;
          width: 380px;
          height: 600px;
          background: white;
          border-radius: 16px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
          display: none;
          flex-direction: column;
          overflow: hidden;
          border: 1px solid rgba(0, 0, 0, 0.05);
          transform: translateY(20px) scale(0.95);
          opacity: 0;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        ">
          <!-- Header with Red Gradient -->
          <div style="
            background: linear-gradient(135deg, ${config.bubbleColor}, #b02a37);
            color: white;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
          ">
            <div style="display: flex; align-items: center; gap: 12px;">
              <div style="
                width: 40px;
                height: 40px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
              ">${config.bubbleIcon}</div>
              <div>
                <div style="font-weight: 600; font-size: 18px; margin-bottom: 2px;">${config.title}</div>
                <div style="font-size: 13px; opacity: 0.9;">${config.subtitle}</div>
              </div>
            </div>
            <button id="chat-close" style="
              background: rgba(255, 255, 255, 0.2);
              border: none;
              color: white;
              width: 32px;
              height: 32px;
              border-radius: 50%;
              cursor: pointer;
              display: flex;
              align-items: center;
              justify-content: center;
              transition: all 0.2s;
            ">✕</button>
          </div>

          <!-- Messages -->
          <div id="chat-messages" style="
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: linear-gradient(to bottom, #f8f9fa, #ffffff);
          ">
            <div class="message bot-message" style="
              margin-bottom: 20px;
              display: flex;
              flex-direction: column;
              align-items: flex-start;
              animation: fadeIn 0.3s ease-out;
            ">
              <div style="
                max-width: 85%;
                padding: 14px 18px;
                border-radius: 20px 20px 20px 4px;
                background: white;
                color: #333;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(0, 0, 0, 0.05);
                font-size: 14px;
                line-height: 1.5;
              ">
                ${config.subtitle}
              </div>
              <div style="font-size: 11px; color: #999; margin-top: 4px;">
                ${new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </div>
            </div>
          </div>

          <!-- Input with Red Send Button -->
          <div style="
            padding: 20px;
            background: white;
            border-top: 1px solid rgba(0, 0, 0, 0.05);
            display: flex;
            gap: 12px;
            align-items: flex-end;
          ">
            <textarea id="chat-input" placeholder="Ask me about TechnoNJR..." style="
              flex: 1;
              border: 2px solid #e9ecef;
              border-radius: 24px;
              padding: 12px 18px;
              font-size: 14px;
              resize: none;
              max-height: 120px;
              min-height: 48px;
              font-family: inherit;
              outline: none;
              transition: all 0.2s;
              background: #f8f9fa;
            "></textarea>
            <button id="chat-send" style="
              width: 48px;
              height: 48px;
              border-radius: 50%;
              background: linear-gradient(135deg, ${config.bubbleColor}, #b02a37);
              border: none;
              color: white;
              cursor: pointer;
              display: flex;
              align-items: center;
              justify-content: center;
              transition: all 0.2s;
              font-size: 16px;
              flex-shrink: 0;
            ">➤</button>
          </div>
        </div>
      </div>
    `;
  }

  // Chat functionality
  function initializeChatFunctionality(container, config) {
    const toggle = container.querySelector("#chat-toggle");
    const window = container.querySelector("#chat-window");
    const close = container.querySelector("#chat-close");
    const input = container.querySelector("#chat-input");
    const send = container.querySelector("#chat-send");
    const messages = container.querySelector("#chat-messages");

    let isOpen = false;
    let sessionId = null;

    // Add hover effects
    toggle.addEventListener("mouseenter", () => {
      toggle.style.transform = "scale(1.1)";
      toggle.style.boxShadow = "0 12px 35px rgba(220, 53, 69, 0.5)";
    });

    toggle.addEventListener("mouseleave", () => {
      toggle.style.transform = "scale(1)";
      toggle.style.boxShadow = "0 8px 25px rgba(220, 53, 69, 0.4)";
    });

    // Input focus effects
    input.addEventListener("focus", () => {
      input.style.borderColor = config.bubbleColor;
      input.style.background = "white";
      input.style.boxShadow = `0 0 0 3px ${config.bubbleColor}20`;
    });

    input.addEventListener("blur", () => {
      input.style.borderColor = "#e9ecef";
      input.style.background = "#f8f9fa";
      input.style.boxShadow = "none";
    });

    // Toggle chat window
    function toggleChat() {
      isOpen = !isOpen;
      if (isOpen) {
        window.style.display = "flex";
        setTimeout(() => {
          window.style.transform = "translateY(0) scale(1)";
          window.style.opacity = "1";
        }, 10);
        toggle.innerHTML = "✕";
      } else {
        window.style.transform = "translateY(20px) scale(0.95)";
        window.style.opacity = "0";
        setTimeout(() => {
          window.style.display = "none";
        }, 400);
        toggle.innerHTML = config.bubbleIcon;
      }
    }

    // Add message to chat
    function addMessage(text, isUser = false) {
      const messageDiv = document.createElement("div");
      messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;
      messageDiv.style.cssText = `
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: ${isUser ? "flex-end" : "flex-start"};
        animation: fadeIn 0.3s ease-out;
      `;

      const bubble = document.createElement("div");
      bubble.style.cssText = `
        max-width: 85%;
        padding: 14px 18px;
        border-radius: ${isUser ? "20px 20px 4px 20px" : "20px 20px 20px 4px"};
        background: ${isUser ? `linear-gradient(135deg, ${config.bubbleColor}, #b02a37)` : "white"};
        color: ${isUser ? "white" : "#333"};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ${!isUser ? "border: 1px solid rgba(0, 0, 0, 0.05);" : ""}
        font-size: 14px;
        line-height: 1.5;
        white-space: pre-wrap;
        word-wrap: break-word;
      `;
      bubble.textContent = text;

      const time = document.createElement("div");
      time.style.cssText = `
        font-size: 11px;
        color: #999;
        margin-top: 4px;
      `;
      time.textContent = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      messageDiv.appendChild(bubble);
      messageDiv.appendChild(time);
      messages.appendChild(messageDiv);
      messages.scrollTop = messages.scrollHeight;
    }

    // Send message to API
    async function sendMessage() {
      const message = input.value.trim();
      if (!message) return;

      addMessage(message, true);
      input.value = "";

      // Add typing indicator with red theme
      const typingDiv = document.createElement("div");
      typingDiv.id = "typing-indicator";
      typingDiv.style.cssText = `
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
      `;
      
      const typingBubble = document.createElement("div");
      typingBubble.style.cssText = `
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 14px 18px;
        background: white;
        border-radius: 20px 20px 20px 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
        max-width: 85%;
      `;
      
      typingBubble.innerHTML = `
        <span style="color: #666; font-size: 14px;">Thinking</span>
        <div style="display: flex; gap: 4px;">
          <span style="width: 8px; height: 8px; background: ${config.bubbleColor}; border-radius: 50%; animation: typing 1.4s infinite ease-in-out;"></span>
          <span style="width: 8px; height: 8px; background: ${config.bubbleColor}; border-radius: 50%; animation: typing 1.4s infinite ease-in-out; animation-delay: -0.16s;"></span>
          <span style="width: 8px; height: 8px; background: ${config.bubbleColor}; border-radius: 50%; animation: typing 1.4s infinite ease-in-out; animation-delay: -0.32s;"></span>
        </div>
      `;
      
      typingDiv.appendChild(typingBubble);
      messages.appendChild(typingDiv);
      messages.scrollTop = messages.scrollHeight;

      try {
        const response = await fetch(`${config.apiUrl}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: message,
            session_id: sessionId,
          }),
        });

        const data = await response.json();
        sessionId = data.session_id;

        // Remove typing indicator
        typingDiv.remove();

        // Add bot response
        addMessage(data.response);
      } catch (error) {
        console.error("Chat error:", error);
        typingDiv.remove();
        addMessage(
          "Sorry, I'm having trouble connecting. Please try again later."
        );
      }
    }

    // Event listeners
    toggle.addEventListener("click", toggleChat);
    close.addEventListener("click", toggleChat);
    send.addEventListener("click", sendMessage);

    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // Add CSS animations
    const style = document.createElement("style");
    style.textContent = `
      @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
      }
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
    `;
    document.head.appendChild(style);
  }

  // Initialize the widget
  function initWidget() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initWidget);
      return;
    }

    const config = getScriptConfig();
    const container = createWidgetContainer(config);
    container.innerHTML = createChatWidget(config);
    initializeChatFunctionality(container, config);

    console.log("Quinx Chat Widget initialized successfully with red styling!");
  }

  // Auto-initialize
  initWidget();
})();'''
    
    return Response(content=embed_script, media_type="application/javascript")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)