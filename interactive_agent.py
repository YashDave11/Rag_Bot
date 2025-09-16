#!/usr/bin/env python3
"""
Interactive AI Agent - Chat with the MongoDB AI assistant with Gemini API integration
"""

import json
import sys
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import google.generativeai as genai

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

class InteractiveAgent:
    """Interactive MongoDB AI Agent with Gemini API integration"""
    
    def __init__(self):
        print("🤖 Starting MongoDB AI Assistant...")
        
        # Initialize Gemini API
        self._setup_gemini()
        
        # Load data
        data_dir = Path(__file__).parent / "data"
        
        print("📚 Loading MongoDB documentation...")
        with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
            self.vector_data = json.load(f)
        
        with open(data_dir / "mongodb_docs.json", "r") as f:
            self.full_data = json.load(f)
        
        print("🧠 Loading AI model...")
        self.embedding_model = SentenceTransformer("thenlper/gte-small")
        
        print("✅ AI Assistant ready!")
        print(f"📊 Loaded {len(self.vector_data)} documents for search")
    
    def _setup_gemini(self):
        """Setup Gemini API"""
        api_key = "AIzaSyCl5ubFeNTdeqmWPu4iYOc97dec6fuCHcc"
        
        try:
            genai.configure(api_key=api_key)
            # Try different model names
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                print("🚀 Gemini API configured successfully with gemini-1.5-flash!")
            except:
                try:
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                    print("🚀 Gemini API configured successfully with gemini-1.5-pro!")
                except:
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                    print("🚀 Gemini API configured successfully with gemini-pro!")
            self.use_gemini = True
        except Exception as e:
            print(f"⚠️  Failed to configure Gemini API: {e}")
            print("   Falling back to basic responses...")
            self.use_gemini = False
        
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant documents using semantic similarity"""
        query_embedding = self.embedding_model.encode(query)
        
        # Calculate similarity with all documents
        similarities = []
        for i, doc in enumerate(self.vector_data):
            if 'embedding' in doc:
                doc_embedding = doc['embedding']
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append((similarity, i, doc))
        
        # Sort by similarity and return top results
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, _, doc in similarities[:top_k]]
    
    def _cosine_similarity(self, a, b):
        """Calculate cosine similarity between two vectors"""
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def find_page_by_title(self, title: str) -> Dict:
        """Find a specific page by title"""
        for doc in self.full_data:
            if doc.get('title', '').lower() == title.lower():
                return doc
        return None
    
    def answer_question(self, question: str) -> str:
        """Answer a question using the knowledge base and Gemini API"""
        print(f"🔍 Searching for information about: {question}")
        
        # Always search for relevant documents, even for non-MongoDB questions
        relevant_docs = self.search_documents(question)
        
        # Prepare context from relevant documents (more comprehensive)
        context_parts = []
        for doc in relevant_docs:
            title = doc.get('title', 'Unknown Document')
            body = doc.get('body', '')
            # Use more content for better Gemini processing
            if len(body) > 1500:
                body = body[:1500] + "..."
            context_parts.append(f"Document Title: {title}\nContent: {body}")
        
        # If no relevant docs found, still use Gemini with empty context
        if not context_parts:
            context = "No specific MongoDB documentation found for this query."
        else:
            context = "\n\n".join(context_parts)
        
        if self.use_gemini:
            return self._generate_gemini_response(question, context)
        else:
            return self._generate_basic_response(question, relevant_docs)
    
    def _generate_gemini_response(self, question: str, context: str) -> str:
        """Generate response using Gemini API with enhanced prompting"""
        try:
            prompt = f"""You are a MongoDB Expert Assistant. Your role is to provide helpful, accurate, and well-structured responses about MongoDB.

USER QUESTION: {question}

MONGODB DOCUMENTATION CONTEXT:
{context}

INSTRUCTIONS:
1. **Relevance Check**: First determine if the user's question is related to MongoDB, databases, or development.

2. **If MongoDB-related**: 
   - Provide a comprehensive, well-structured answer using the context
   - Use clear headings, bullet points, and code examples when appropriate
   - Include practical tips and best practices
   - If context is insufficient, acknowledge limitations and suggest what to ask instead

3. **If NOT MongoDB-related** (general greetings, unrelated topics):
   - Politely acknowledge the question
   - Redirect to MongoDB topics in a friendly way
   - Suggest relevant MongoDB questions they could ask
   - Keep it brief but helpful

4. **Response Format**:
   - Use clear structure with headings (##) when needed
   - Include bullet points for lists
   - Add code blocks for MongoDB commands/syntax
   - Use emojis sparingly for visual appeal
   - Keep tone professional but friendly

5. **Always end with**: A brief suggestion for follow-up questions or related topics they might find useful.

RESPONSE:"""

            print("🧠 Generating enhanced AI response...")
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            print("   Falling back to basic response...")
            return self._generate_basic_response(question, self.search_documents(question))
    
    def _generate_basic_response(self, question: str, relevant_docs: List[Dict]) -> str:
        """Generate basic response without Gemini"""
        # Check if question seems MongoDB-related
        mongodb_keywords = ['mongo', 'database', 'collection', 'document', 'query', 'index', 'atlas', 'aggregation']
        is_mongodb_related = any(keyword in question.lower() for keyword in mongodb_keywords)
        
        if not relevant_docs:
            if is_mongodb_related:
                return """I couldn't find specific information about that in the MongoDB documentation. 

Try asking about:
• MongoDB best practices
• How to create indexes
• Database performance optimization
• Collection operations
• Aggregation pipelines"""
            else:
                return """👋 Hello! I'm a MongoDB expert assistant. 

I can help you with:
• MongoDB database operations
• Performance optimization
• Best practices and configurations
• Atlas cloud services
• Aggregation and queries

What would you like to know about MongoDB?"""
        
        response_parts = [
            f"Based on the MongoDB documentation, here's what I found:\n"
        ]
        
        for i, doc in enumerate(relevant_docs, 1):
            title = doc.get('title', 'Unknown Document')
            body = doc.get('body', '')
            
            # Truncate long content
            if len(body) > 300:
                body = body[:300] + "..."
            
            response_parts.append(f"{i}. **{title}**")
            response_parts.append(f"   {body}\n")
        
        return "\n".join(response_parts)
    
    def summarize_page(self, title: str) -> str:
        """Summarize a specific page using Gemini API"""
        print(f"📄 Looking for page: {title}")
        
        page = self.find_page_by_title(title)
        if not page:
            # Try partial matching
            matches = []
            for doc in self.full_data:
                if title.lower() in doc.get('title', '').lower():
                    matches.append(doc)
            
            if matches:
                page = matches[0]
                print(f"✅ Found similar page: {page['title']}")
            else:
                return f"I couldn't find a page titled '{title}'. Try a different title or ask a general question."
        
        content = page.get('body', '')
        page_title = page.get('title', 'Unknown')
        
        if self.use_gemini:
            return self._generate_gemini_summary(page_title, content)
        else:
            # Return first part of the content
            if len(content) > 1000:
                content = content[:1000] + "..."
            return f"**{page_title}**\n\n{content}"
    
    def _generate_gemini_summary(self, title: str, content: str) -> str:
        """Generate summary using Gemini API with enhanced prompting"""
        try:
            prompt = f"""You are a MongoDB Expert Assistant. Create a comprehensive, well-structured summary of this MongoDB documentation page.

PAGE TITLE: {title}

FULL CONTENT:
{content}

INSTRUCTIONS:
1. **Create a clear, comprehensive summary** that captures all key information
2. **Structure the response** with:
   - Brief overview/introduction
   - Key concepts and features
   - Important commands or syntax (in code blocks)
   - Best practices and recommendations
   - Common use cases or examples

3. **Format Guidelines**:
   - Use clear headings (##) for main sections
   - Use bullet points for lists and key points
   - Include code blocks for MongoDB commands/syntax
   - Use **bold** for important terms
   - Add emojis sparingly for visual appeal

4. **Make it practical**: Focus on information developers can actually use
5. **Keep it comprehensive but readable**: Don't skip important details, but organize them well

6. **End with**: Practical next steps or related topics to explore

SUMMARY:"""

            print("🧠 Generating enhanced AI summary...")
            response = self.gemini_model.generate_content(prompt)
            return f"## 📋 Summary: {title}\n\n{response.text}"
            
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            print("   Falling back to basic summary...")
            if len(content) > 1000:
                content = content[:1000] + "..."
            return f"**{title}**\n\n{content}"
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "="*60)
        print("💬 MongoDB AI Assistant - Interactive Mode")
        print("="*60)
        print("Ask me anything about MongoDB!")
        print("Examples:")
        print("  • What are MongoDB best practices?")
        print("  • How do I create an index?")
        print("  • Summarize 'Create a MongoDB Deployment'")
        print("  • Type 'quit' to exit")
        print("-"*60)
        
        while True:
            try:
                user_input = input("\n🤔 Your question: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using MongoDB AI Assistant!")
                    break
                
                # Determine if it's a summarization request
                if any(word in user_input.lower() for word in ['summarize', 'summary']):
                    # Extract title
                    if 'summarize' in user_input.lower():
                        title_start = user_input.lower().find('summarize') + len('summarize')
                        title = user_input[title_start:].strip().strip('"').strip("'")
                    else:
                        title_start = user_input.lower().find('summary') + len('summary')
                        title = user_input[title_start:].strip().strip('"').strip("'")
                    
                    if title:
                        response = self.summarize_page(title)
                    else:
                        response = "Please specify which page you'd like me to summarize."
                else:
                    # Regular Q&A
                    response = self.answer_question(user_input)
                
                print(f"\n🤖 **MongoDB AI Assistant:**")
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using MongoDB AI Assistant!")
                break
            except Exception as e:
                print(f"\n❌ Sorry, I encountered an error: {e}")

def main():
    """Main function"""
    try:
        agent = InteractiveAgent()
        agent.chat()
    except Exception as e:
        print(f"❌ Error starting the assistant: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()