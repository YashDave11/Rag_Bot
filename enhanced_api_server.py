#!/usr/bin/env python3
"""
Enhanced FastAPI server for ChatMongo SaaS Platform
Phase 1: User Registration & Authentication
"""

import os
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

# Import original MongoDB RAG functionality
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np

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

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    status: str = "success"

# Enhanced User Management System
class UserManager:
    """Handles user registration, authentication, and data management"""
    
    def __init__(self):
        self.users_dir = Path(__file__).parent / "users_data"
        self.users_dir.mkdir(exist_ok=True)
        self.sessions = {}  # In-memory session storage
        
    def generate_api_key(self, user_id: str) -> str:
        """Generate unique API key for user"""
        timestamp = str(int(datetime.now().timestamp()))
        raw_key = f"{user_id}_{timestamp}"
        return f"cmk_{hashlib.md5(raw_key.encode()).hexdigest()[:16]}"
    
    def create_user(self, email: str) -> dict:
        """Create new user account"""
        # Check if user already exists
        existing_user = self.get_user_by_email(email)
        if existing_user:
            return existing_user
        
        user_id = str(uuid.uuid4())
        api_key = self.generate_api_key(user_id)
        
        user_data = {
            'user_id': user_id,
            'email': email,
            'api_key': api_key,
            'created_at': datetime.now().isoformat(),
            'widget_status': 'none',  # none, active, offline
            'message_count': 0,
            'message_limit': 300,
            'widget_config': None,
            'documents': []
        }
        
        # Save user data
        user_file = self.users_dir / f"{user_id}.json"
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return user_data
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email address"""
        for user_file in self.users_dir.glob("*.json"):
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    if user_data.get('email') == email:
                        return user_data
            except:
                continue
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        user_file = self.users_dir / f"{user_id}.json"
        if user_file.exists():
            try:
                with open(user_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def get_user_by_api_key(self, api_key: str) -> Optional[dict]:
        """Get user by API key"""
        for user_file in self.users_dir.glob("*.json"):
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    if user_data.get('api_key') == api_key:
                        return user_data
            except:
                continue
        return None
    
    def create_session(self, user_id: str) -> str:
        """Create user session"""
        session_token = f"session_{user_id}_{uuid.uuid4().hex[:8]}"
        self.sessions[session_token] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat()
        }
        return session_token
    
    def get_user_from_session(self, session_token: str) -> Optional[dict]:
        """Get user from session token"""
        if not session_token or session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            del self.sessions[session_token]
            return None
        
        return self.get_user_by_id(session['user_id'])

# Original MongoDB RAG Agent (keeping for backward compatibility)
class MongoDBRAGAgent:
    """Original MongoDB RAG Agent"""
    
    def __init__(self):
        self.sessions = {}
        self._setup_gemini()
        self._load_data()
        self._load_embedding_model()
    
    def _setup_gemini(self):
        """Setup Gemini API with environment variable"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=api_key)
            # Try different model names
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                print("✅ Gemini API configured from environment with gemini-1.5-pro")
            except:
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                print("✅ Gemini API configured from environment with gemini-pro")
            self.use_gemini = True
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            self.use_gemini = False
    
    def _load_data(self):
        """Load MongoDB documentation data"""
        try:
            data_dir = Path(__file__).parent / "data"
            
            with open(data_dir / "mongodb_docs_embeddings.json", "r", encoding='utf-8') as f:
                self.vector_data = json.load(f)
            
            with open(data_dir / "mongodb_docs.json", "r", encoding='utf-8') as f:
                self.full_data = json.load(f)
            
            print(f"✅ Loaded {len(self.vector_data)} documents")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def _load_embedding_model(self):
        """Load embedding model"""
        try:
            self.embedding_model = SentenceTransformer("thenlper/gte-small")
            print("✅ Embedding model loaded")
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            raise
    
    def search_documents(self, query: str, top_k: int = 3) -> List[dict]:
        """Search for relevant documents"""
        try:
            query_embedding = self.embedding_model.encode(query)
            
            similarities = []
            for i, doc in enumerate(self.vector_data):
                if 'embedding' in doc and doc['embedding']:
                    doc_embedding = np.array(doc['embedding'])
                    query_array = np.array(query_embedding)
                    
                    similarity = np.dot(query_array, doc_embedding) / (
                        np.linalg.norm(query_array) * np.linalg.norm(doc_embedding)
                    )
                    similarities.append((similarity, doc))
            
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [doc for _, doc in similarities[:top_k]]
            
        except Exception as e:
            print(f"⚠️  Search error: {e}")
            return self.vector_data[:top_k]
    
    def generate_response(self, question: str, session_id: str = None) -> dict:
        """Generate response for a question"""
        try:
            if not session_id:
                session_id = str(uuid.uuid4())
            
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'messages': [],
                    'created_at': datetime.now().isoformat()
                }
            
            relevant_docs = self.search_documents(question)
            
            if self.use_gemini:
                response_text = self._generate_gemini_response(question, relevant_docs)
            else:
                response_text = self._generate_basic_response(question, relevant_docs)
            
            message_data = {
                'user_message': question,
                'bot_response': response_text,
                'timestamp': datetime.now().isoformat()
            }
            self.sessions[session_id]['messages'].append(message_data)
            
            return {
                'response': response_text,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'response': f"Sorry, I encountered an error: {str(e)}",
                'session_id': session_id or str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
    
    def _generate_gemini_response(self, question: str, docs: List[dict]) -> str:
        """Generate response using Gemini"""
        try:
            context_parts = []
            for doc in docs:
                title = doc.get('title', 'Unknown')
                body = doc.get('body', '')
                
                if len(body) > 1000:
                    body = body[:1000] + "..."
                
                context_parts.append(f"Document: {title}\nContent: {body}")
            
            context = "\n\n".join(context_parts)
            
            prompt = f"""You are a MongoDB Expert Assistant. Answer the user's question based on the provided context.

Question: {question}

MongoDB Documentation Context:
{context}

FORMATTING INSTRUCTIONS:
- Use clean, readable text without markdown asterisks or bold formatting
- Structure your response with clear sections using simple headings
- Use simple bullet points with dashes (-)
- No markdown formatting like **bold** or *italic*
- Use plain text with good spacing and organization
- Keep responses conversational but informative
- If the question is not MongoDB-related, politely redirect to MongoDB topics
- Keep responses concise but helpful (max 300 words)

Answer:"""

            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
            return self._generate_basic_response(question, docs)
    
    def _generate_basic_response(self, question: str, docs: List[dict]) -> str:
        """Generate basic response without Gemini"""
        if not docs:
            return """I couldn't find relevant information in the MongoDB documentation.

Try asking about:
- MongoDB operations and queries
- Database best practices
- Indexing strategies
- Performance optimization"""
        
        response = "Based on MongoDB documentation:\n\n"
        for i, doc in enumerate(docs[:2], 1):
            title = doc.get('title', 'Unknown')
            body = doc.get('body', '')[:200] + "..."
            response += f"{i}. {title}\n   {body}\n\n"
        
        return response

# Initialize components
print("🤖 Initializing ChatMongo SaaS Platform...")
user_manager = UserManager()
mongodb_agent = MongoDBRAGAgent()
print("✅ Platform ready!")

# FastAPI app
app = FastAPI(
    title="ChatMongo SaaS API",
    description="SaaS Platform for Custom PDF Chatbots",
    version="1.0.0"
)

# CORS middleware with environment-based origins
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get current user
def get_current_user(session_token: str = Cookie(None)) -> Optional[dict]:
    """Get current user from session"""
    return user_manager.get_user_from_session(session_token)

# API Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "ChatMongo SaaS API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

# Authentication Routes
@app.post("/auth/register")
async def register_user(user_data: UserRegistration, response: Response):
    """Register new user"""
    try:
        user = user_manager.create_user(user_data.email)
        session_token = user_manager.create_session(user['user_id'])
        
        # Set session cookie
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=7*24*60*60,  # 7 days
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        return UserResponse(
            user_id=user['user_id'],
            email=user['email'],
            api_key=user['api_key'],
            created_at=user['created_at'],
            widget_status=user['widget_status'],
            message_count=user['message_count'],
            message_limit=user['message_limit']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return UserResponse(
        user_id=current_user['user_id'],
        email=current_user['email'],
        api_key=current_user['api_key'],
        created_at=current_user['created_at'],
        widget_status=current_user['widget_status'],
        message_count=current_user['message_count'],
        message_limit=current_user['message_limit']
    )

@app.post("/auth/logout")
async def logout(response: Response, session_token: str = Cookie(None)):
    """Logout user"""
    if session_token and session_token in user_manager.sessions:
        del user_manager.sessions[session_token]
    
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

# Original MongoDB Chat (for backward compatibility)
@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Original MongoDB chat endpoint"""
    try:
        result = mongodb_agent.generate_response(message.message, message.session_id)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "gemini_available": mongodb_agent.use_gemini,
        "users_count": len(list(user_manager.users_dir.glob("*.json"))),
        "active_sessions": len(user_manager.sessions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv('API_HOST', '0.0.0.0'), 
        port=int(os.getenv('API_PORT', 8000))
    )