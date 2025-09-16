#!/usr/bin/env python3
"""
Clean Interactive MongoDB AI Agent with Gemini integration
"""

import json
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import google.generativeai as genai
import numpy as np

class CleanInteractiveAgent:
    """Clean MongoDB AI Agent with Gemini integration"""
    
    def __init__(self):
        print("🤖 Starting MongoDB AI Assistant...")
        
        try:
            # Setup Gemini
            self._setup_gemini()
            
            # Load data
            self._load_data()
            
            # Load embedding model
            print("🧠 Loading embedding model...")
            self.embedding_model = SentenceTransformer("thenlper/gte-small")
            
            print("✅ AI Assistant ready!")
            print(f"📊 Loaded {len(self.vector_data)} documents for search")
            
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            raise
    
    def _setup_gemini(self):
        """Setup Gemini API"""
        try:
            api_key = "AIzaSyCl5ubFeNTdeqmWPu4iYOc97dec6fuCHcc"
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            self.use_gemini = True
            print("🚀 Gemini API configured successfully!")
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            self.use_gemini = False
    
    def _load_data(self):
        """Load MongoDB documentation data"""
        try:
            data_dir = Path(__file__).parent / "data"
            
            print("📚 Loading MongoDB documentation...")
            with open(data_dir / "mongodb_docs_embeddings.json", "r", encoding='utf-8') as f:
                self.vector_data = json.load(f)
            
            with open(data_dir / "mongodb_docs.json", "r", encoding='utf-8') as f:
                self.full_data = json.load(f)
                
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
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
            return self.vector_data[:top_k]  # Fallback to first few docs
    
    def answer_question(self, question: str) -> str:
        """Answer a question using Gemini API"""
        try:
            print(f"🔍 Searching for: {question}")
            
            # Search for relevant documents
            relevant_docs = self.search_documents(question)
            
            # Prepare context
            context_parts = []
            for doc in relevant_docs:
                title = doc.get('title', 'Unknown')
                body = doc.get('body', '')
                
                # Limit content length
                if len(body) > 1000:
                    body = body[:1000] + "..."
                
                context_parts.append(f"Document: {title}\nContent: {body}")
            
            context = "\n\n".join(context_parts)
            
            if self.use_gemini:
                return self._generate_gemini_response(question, context)
            else:
                return self._generate_basic_response(question, relevant_docs)
                
        except Exception as e:
            print(f"❌ Error answering question: {e}")
            return "Sorry, I encountered an error processing your question."
    
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
- End with 2-3 relevant follow-up questions

RESPONSE FORMAT EXAMPLE:
Main Topic

Key Points:
- Point one with clear explanation
- Point two with practical details
- Point three with examples

Important Details:
- Specific information here
- Code examples in plain text
- Best practices and recommendations

Questions you might ask next:
- Related question 1?
- Related question 2?
- Related question 3?

Answer:"""

            print("🧠 Generating AI response...")
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
            return self._generate_basic_response(question, self.search_documents(question))
    
    def _generate_basic_response(self, question: str, docs: List[Dict]) -> str:
        """Generate basic response without Gemini"""
        if not docs:
            return """I couldn't find relevant information in the MongoDB documentation.

Try asking about:
- MongoDB operations and queries
- Database best practices
- Indexing strategies
- Performance optimization
- Atlas cloud features"""
        
        response = "Based on MongoDB documentation:\n\n"
        for i, doc in enumerate(docs, 1):
            title = doc.get('title', 'Unknown')
            body = doc.get('body', '')[:300] + "..."
            response += f"{i}. {title}\n   {body}\n\n"
        
        return response
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "="*60)
        print("💬 MongoDB AI Assistant - Interactive Mode")
        print("="*60)
        print("Ask me anything about MongoDB!")
        print("Examples:")
        print("  • What are MongoDB best practices?")
        print("  • How do I create an index?")
        print("  • What is aggregation in MongoDB?")
        print("  • Type 'quit' to exit")
        print("-"*60)
        
        while True:
            try:
                user_input = input("\n🤔 Your question: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Thanks for using MongoDB AI Assistant!")
                    break
                
                response = self.answer_question(user_input)
                print(f"\n🤖 **MongoDB AI Assistant:**")
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using MongoDB AI Assistant!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    try:
        agent = CleanInteractiveAgent()
        agent.chat()
    except Exception as e:
        print(f"❌ Failed to start assistant: {e}")

if __name__ == "__main__":
    main()