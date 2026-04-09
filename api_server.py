#!/usr/bin/env python3
"""
FastAPI server for MongoDB RAG Chat Bot
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid
from datetime import datetime
import asyncio
from pathlib import Path
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np

# Pydantic models for request/response
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    status: str = "success"

class ChatHistory(BaseModel):
    session_id: str
    messages: List[dict]

# MongoDB RAG Agent (adapted from our clean agent)
class MongoDBRAGAgent:
    """MongoDB RAG Agent for API usage"""
    
    def __init__(self):
        self.sessions = {}  # In-memory session storage
        self._setup_gemini()
        self._load_data()
        self._load_embedding_model()
    
    def _setup_gemini(self):
        """Setup Gemini API"""
        try:
            api_key = "AIzaSyCl5ubFeNTdeqmWPu4iYOc97dec6fuCHcc"
            genai.configure(api_key=api_key)
            # Try different model names
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                print("✅ Gemini API configured with gemini-1.5-pro")
            except:
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                print("✅ Gemini API configured with gemini-pro")
            self.use_gemini = True
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            self.use_gemini = False
    
    def _load_data(self):
        """Load college rules and conduct data"""
        try:
            data_dir = Path(__file__).parent / "data"
            
            with open(data_dir / "mongodb_docs_embeddings.json", "r", encoding='utf-8') as f:
                self.vector_data = json.load(f)
            
            with open(data_dir / "mongodb_docs.json", "r", encoding='utf-8') as f:
                self.full_data = json.load(f)
            
            print(f"✅ Loaded {len(self.vector_data)} college rules")
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
                    
                    # Calculate cosine similarity
                    similarity = np.dot(query_array, doc_embedding) / (
                        np.linalg.norm(query_array) * np.linalg.norm(doc_embedding)
                    )
                    similarities.append((similarity, doc))
            
            # Sort by similarity and return top results
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [doc for _, doc in similarities[:top_k]]
            
        except Exception as e:
            print(f"⚠️  Search error: {e}")
            return self.vector_data[:top_k]  # Fallback
    
    def generate_response(self, question: str, session_id: str = None) -> dict:
        """Generate response for a question"""
        try:
            # Create session if not exists
            if not session_id:
                session_id = str(uuid.uuid4())
            
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'messages': [],
                    'created_at': datetime.now().isoformat()
                }
            
            # Search for relevant documents
            relevant_docs = self.search_documents(question)
            
            # Prepare context
            context_parts = []
            for doc in relevant_docs:
                title = doc.get('title', 'Unknown')
                body = doc.get('body', '')
                
                if len(body) > 1000:
                    body = body[:1000] + "..."
                
                context_parts.append(f"Document: {title}\nContent: {body}")
            
            context = "\n\n".join(context_parts)
            
            # Generate response
            if self.use_gemini:
                response_text = self._generate_gemini_response(question, context)
            else:
                response_text = self._generate_basic_response(question, relevant_docs)
            
            # Store in session
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
    
    def _generate_gemini_response(self, question: str, context: str) -> str:
        """Generate response using Gemini"""
        try:
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
- End with a brief suggestion for follow-up

Answer:"""

            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
            return self._generate_basic_response(question, self.search_documents(question))
    
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
        for i, doc in enumerate(docs[:2], 1):  # Limit to 2 docs for API
            title = doc.get('title', 'Unknown')
            body = doc.get('body', '')[:200] + "..."
            response += f"{i}. {title}\n   {body}\n\n"
        
        return response
    
    def get_session_history(self, session_id: str) -> dict:
        """Get chat history for a session"""
        if session_id in self.sessions:
            return self.sessions[session_id]
        return {'messages': [], 'created_at': datetime.now().isoformat()}

# Initialize the agent
print("🤖 Initializing MongoDB RAG Agent...")
agent = MongoDBRAGAgent()
print("✅ Agent ready!")

# FastAPI app
app = FastAPI(
    title="MongoDB RAG Chat API",
    description="REST API for MongoDB RAG-powered chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "MongoDB RAG Chat API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Send a message and get a response"""
    try:
        result = agent.generate_response(message.message, message.session_id)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    try:
        history = agent.get_session_history(session_id)
        return ChatHistory(session_id=session_id, messages=history['messages'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "gemini_available": agent.use_gemini,
        "documents_loaded": len(agent.vector_data),
        "active_sessions": len(agent.sessions)
    }

# Use start_server.py to run the server