#!/usr/bin/env python3
"""
Phase 3A API Server: PDF Upload & Processing
Extends the basic functionality with document processing capabilities
"""

import os
import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import PyPDF2
import io

# Simple document processing without heavy dependencies
class DocumentProcessor:
    """Simple document processor for PDF text extraction and chunking"""
    
    def __init__(self):
        self.users_dir = Path(__file__).parent / "users_data"
        self.users_dir.mkdir(exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text_content = ""
            
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            return text_content.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def create_chunks(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[dict]:
        """Create overlapping text chunks"""
        if not text.strip():
            return []
        
        # Simple sentence-based chunking
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = ""
        chunk_id = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Add sentence to current chunk
            test_chunk = current_chunk + sentence + ". "
            
            if len(test_chunk) <= chunk_size:
                current_chunk = test_chunk
            else:
                # Save current chunk if it has content
                if current_chunk.strip():
                    chunks.append({
                        'chunk_id': chunk_id,
                        'text': current_chunk.strip(),
                        'length': len(current_chunk.strip())
                    })
                    chunk_id += 1
                
                # Start new chunk with overlap
                if overlap > 0 and chunks:
                    # Take last few words for overlap
                    words = current_chunk.split()
                    overlap_words = words[-min(overlap//10, len(words)):]  # Rough overlap
                    current_chunk = " ".join(overlap_words) + " " + sentence + ". "
                else:
                    current_chunk = sentence + ". "
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                'chunk_id': chunk_id,
                'text': current_chunk.strip(),
                'length': len(current_chunk.strip())
            })
        
        return chunks
    
    def process_documents(self, user_email: str, files: List[UploadFile]) -> dict:
        """Process uploaded PDF documents for a user"""
        try:
            # Create user directory
            user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
            user_dir = self.users_dir / user_id
            user_dir.mkdir(exist_ok=True)
            
            processed_docs = []
            total_chunks = 0
            
            for file in files:
                if not file.filename.lower().endswith('.pdf'):
                    continue
                
                # Read file content
                file_content = file.file.read()
                
                # Extract text
                text_content = self.extract_text_from_pdf(file_content)
                
                if not text_content.strip():
                    continue
                
                # Create chunks
                chunks = self.create_chunks(text_content)
                
                # Save document data
                doc_data = {
                    'filename': file.filename,
                    'processed_at': datetime.now().isoformat(),
                    'text_length': len(text_content),
                    'chunks_count': len(chunks),
                    'chunks': chunks
                }
                
                # Save to file
                doc_file = user_dir / f"doc_{len(processed_docs)}.json"
                with open(doc_file, 'w', encoding='utf-8') as f:
                    json.dump(doc_data, f, indent=2, ensure_ascii=False)
                
                processed_docs.append({
                    'filename': file.filename,
                    'chunks_count': len(chunks),
                    'text_length': len(text_content)
                })
                
                total_chunks += len(chunks)
            
            # Save processing summary
            summary = {
                'user_email': user_email,
                'user_id': user_id,
                'processed_at': datetime.now().isoformat(),
                'documents': processed_docs,
                'total_documents': len(processed_docs),
                'total_chunks': total_chunks
            }
            
            summary_file = user_dir / "processing_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            return {
                'success': True,
                'user_id': user_id,
                'documents_processed': len(processed_docs),
                'chunks_count': total_chunks,
                'documents': processed_docs
            }
            
        except Exception as e:
            raise Exception(f"Document processing failed: {str(e)}")

# Initialize processor
processor = DocumentProcessor()

# FastAPI app
app = FastAPI(
    title="ChatMongo Phase 3A API",
    description="PDF Upload & Processing API",
    version="3.0.0"
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
    return {
        "message": "ChatMongo Phase 3A API - PDF Processing",
        "version": "3.0.0",
        "status": "ready"
    }

class ChatRequest(BaseModel):
    message: str
    user_email: Optional[str] = ""
    chat_id: Optional[str] = "default"

@app.post("/chat")
async def chat(request: ChatRequest):
    """Basic chat endpoint for the widget"""
    try:
        # Simple echo response for now
        response_text = f"I received your message: '{request.message}'. The full chat functionality with document search will be implemented soon!"
        
        return {
            "response": response_text,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/process")
async def process_documents(
    userEmail: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Process uploaded PDF documents"""
    try:
        # Validate files
        pdf_files = [f for f in files if f.filename.lower().endswith('.pdf')]
        
        if not pdf_files:
            raise HTTPException(status_code=400, detail="No valid PDF files provided")
        
        if len(pdf_files) > 10:  # Limit to 10 files
            raise HTTPException(status_code=400, detail="Too many files. Maximum 10 PDFs allowed.")
        
        # Check file sizes
        for file in pdf_files:
            file.file.seek(0, 2)  # Seek to end
            size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if size > 10 * 1024 * 1024:  # 10MB limit per file
                raise HTTPException(
                    status_code=400, 
                    detail=f"File {file.filename} is too large. Maximum 10MB per file."
                )
        
        # Process documents
        result = processor.process_documents(userEmail, pdf_files)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/status/{user_email}")
async def get_processing_status(user_email: str):
    """Get processing status for a user"""
    try:
        user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
        user_dir = processor.users_dir / user_id
        summary_file = user_dir / "processing_summary.json"
        
        if not summary_file.exists():
            return {"status": "no_documents", "message": "No documents processed yet"}
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        return {
            "status": "processed",
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "processor": "ready",
        "users_count": len(list(processor.users_dir.glob("*")))
    }

@app.get("/embed.js")
async def get_embed_script():
    """Serve the embeddable chat widget script"""
    embed_js = """
(function() {
    'use strict';
    
    // Get script configuration
    const script = document.currentScript;
    const apiUrl = script.getAttribute('data-api-url') || 'http://localhost:8001';
    const chatId = script.getAttribute('data-quinx-chat-id') || 'default';
    const userEmail = script.getAttribute('data-user') || '';
    const bubbleColor = script.getAttribute('data-bubble-color') || '#00ED64';
    const bubbleIcon = decodeURIComponent(script.getAttribute('data-bubble-icon') || '💬');
    const bubblePosition = script.getAttribute('data-bubble-position') || 'bottom-right';
    const bubbleSize = script.getAttribute('data-bubble-size') || 'medium';
    
    // Position styles
    const positions = {
        'bottom-right': { bottom: '20px', right: '20px' },
        'bottom-left': { bottom: '20px', left: '20px' },
        'top-right': { top: '20px', right: '20px' },
        'top-left': { top: '20px', left: '20px' }
    };
    
    // Size styles
    const sizes = {
        'small': { width: '50px', height: '50px', fontSize: '20px' },
        'medium': { width: '60px', height: '60px', fontSize: '24px' },
        'large': { width: '70px', height: '70px', fontSize: '28px' }
    };
    
    const pos = positions[bubblePosition] || positions['bottom-right'];
    const size = sizes[bubbleSize] || sizes['medium'];
    
    // Create chat widget HTML
    const widgetHTML = `
        <div id="mongodb-chat-widget" style="position: fixed; ${Object.entries(pos).map(([k,v]) => k + ':' + v).join(';')}; z-index: 9999;">
            <div id="chat-bubble" style="width: ${size.width}; height: ${size.height}; border-radius: 50%; background: ${bubbleColor}; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: transform 0.2s; font-size: ${size.fontSize};">
                ${bubbleIcon}
            </div>
            <div id="chat-window" style="display: none; position: absolute; ${bubblePosition.includes('bottom') ? 'bottom: 80px' : 'top: 80px'}; ${bubblePosition.includes('right') ? 'right: 0' : 'left: 0'}; width: 380px; height: 500px; background: white; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); flex-direction: column; overflow: hidden;">
                <div style="background: ${bubbleColor}; color: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; font-size: 18px; font-weight: 600;">ChatMongo</h3>
                        <p style="margin: 4px 0 0 0; font-size: 12px; opacity: 0.9;">AI-Powered Assistant</p>
                    </div>
                    <button id="close-chat" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0; width: 30px; height: 30px;">&times;</button>
                </div>
                <div id="chat-messages" style="flex: 1; overflow-y: auto; padding: 16px; background: #f5f5f5;"></div>
                <div style="padding: 16px; background: white; border-top: 1px solid #e0e0e0;">
                    <div style="display: flex; gap: 8px;">
                        <input id="chat-input" type="text" placeholder="Type your message..." style="flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; outline: none;" />
                        <button id="send-btn" style="background: ${bubbleColor}; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">Send</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }
    
    function initWidget() {
        // Insert widget HTML
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
        
        // Get elements
        const bubble = document.getElementById('chat-bubble');
        const chatWindow = document.getElementById('chat-window');
        const closeBtn = document.getElementById('close-chat');
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const messagesDiv = document.getElementById('chat-messages');
        
        let isOpen = false;
        
        // Hover effect
        bubble.addEventListener('mouseenter', () => {
            bubble.style.transform = 'scale(1.1)';
        });
        bubble.addEventListener('mouseleave', () => {
            bubble.style.transform = 'scale(1)';
        });
        
        // Toggle chat window
        bubble.addEventListener('click', () => {
            isOpen = !isOpen;
            chatWindow.style.display = isOpen ? 'flex' : 'none';
            if (isOpen && messagesDiv.children.length === 0) {
                addMessage('Hello! How can I help you today?', 'bot');
            }
        });
        
        closeBtn.addEventListener('click', () => {
            isOpen = false;
            chatWindow.style.display = 'none';
        });
        
        // Send message
        function sendMessage() {
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            // Show typing indicator
            const typingId = addMessage('Typing...', 'bot');
            
            // Send to API
            fetch(apiUrl + '/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: message,
                    user_email: userEmail,
                    chat_id: chatId
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById(typingId).remove();
                addMessage(data.response || 'Sorry, I could not process that.', 'bot');
            })
            .catch(err => {
                document.getElementById(typingId).remove();
                addMessage('Sorry, there was an error. Please try again.', 'bot');
                console.error('Chat error:', err);
            });
        }
        
        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        function addMessage(text, sender) {
            const msgId = 'msg-' + Date.now();
            const isBot = sender === 'bot';
            const msgHTML = `
                <div id="${msgId}" style="margin-bottom: 12px; display: flex; justify-content: ${isBot ? 'flex-start' : 'flex-end'};">
                    <div style="max-width: 70%; padding: 10px 14px; border-radius: 12px; background: ${isBot ? 'white' : bubbleColor}; color: ${isBot ? '#333' : 'white'}; font-size: 14px; line-height: 1.4; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                        ${text}
                    </div>
                </div>
            `;
            messagesDiv.insertAdjacentHTML('beforeend', msgHTML);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            return msgId;
        }
        
        console.log('✅ MongoDB Chat Widget loaded successfully');
        console.log('Chat ID:', chatId);
        console.log('User:', userEmail);
    }
})();
""".strip()
    
    return Response(content=embed_js, media_type="application/javascript")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Phase 3A API Server...")
    print("📄 PDF Processing Features:")
    print("   • PDF text extraction")
    print("   • Document chunking")
    print("   • Multi-file upload support")
    print("   • User-specific storage")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8001)