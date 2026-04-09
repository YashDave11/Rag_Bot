#!/usr/bin/env python3
"""
Multilingual Interactive AI Agent - Chat with the MongoDB AI assistant in multiple languages
"""

import json
import sys
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import google.generativeai as genai
from deep_translator import GoogleTranslator

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

class MultilingualAgent:
    """Multilingual MongoDB AI Agent with Gemini API integration"""
    
    def __init__(self):
        print("🤖 Starting Qunix Smart Support AI Assistant...")
        
        # Initialize Gemini API
        self._setup_gemini()
        
        # Load data
        data_dir = Path(__file__).parent / "data"
        
        print("📚 Loading knowledge base documentation...")
        with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
            self.vector_data = json.load(f)
        
        with open(data_dir / "mongodb_docs_embeddings.json", "r") as f:
            self.full_data = json.load(f)
        
        print("🧠 Loading AI model...")
        self.embedding_model = SentenceTransformer("thenlper/gte-small")
        
        print("✅ Qunix Smart Support AI Assistant ready!")
        print(f"📊 Loaded {len(self.vector_data)} documents for search")
        print("🌍 Supports multiple languages with auto-detection!")
    
    def _setup_gemini(self):
        """Setup Gemini API"""
        api_key = "AIzaSyCl5ubFeNTdeqmWPu4iYOc97dec6fuCHcc"
        
        try:
            genai.configure(api_key=api_key)
            # Try different model names
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                print("🚀 Gemini API configured successfully with gemini-1.5-pro!")
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
    
    def detect_and_translate_to_english(self, text: str) -> Tuple[str, str]:
        """
        Detect language and translate to English if needed
        Returns: (translated_text, detected_language)
        """
        try:
            # First, try to detect the language
            translator = GoogleTranslator(source='auto', target='en')
            translated = translator.translate(text)
            
            # Get the detected source language
            detected_lang = translator.source
            
            # If already in English, return original text
            if detected_lang == 'en' or translated == text:
                return text, 'en'
            
            print(f"🌍 Detected language: {detected_lang}")
            print(f"🔄 Translating to English for processing...")
            
            return translated, detected_lang
            
        except Exception as e:
            print(f"⚠️  Translation failed: {e}")
            print("   Proceeding with original text...")
            return text, 'en'  # Assume English if translation fails
    
    def translate_to_language(self, text: str, target_language: str) -> str:
        """
        Translate text to target language
        """
        if target_language == 'en':
            return text
        
        try:
            translator = GoogleTranslator(source='en', target=target_language)
            translated = translator.translate(text)
            print(f"🔄 Translating response back to {target_language}...")
            return translated
        except Exception as e:
            print(f"⚠️  Translation to {target_language} failed: {e}")
            print("   Returning English response...")
            return text
    
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
        """Answer a question using the knowledge base and Gemini API with multilingual support"""
        # Step 1: Detect language and translate to English for processing
        english_question, source_language = self.detect_and_translate_to_english(question)
        
        print(f"🔍 Searching for information about: {english_question}")
        
        # Step 2: Search using English query
        relevant_docs = self.search_documents(english_question)
        
        # Prepare context from relevant documents
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
        
        # Step 3: Generate response in English
        if self.use_gemini:
            english_response = self._generate_gemini_response(english_question, context)
        else:
            english_response = self._generate_basic_response(english_question, relevant_docs)
        
        # Step 4: Translate response back to source language
        final_response = self.translate_to_language(english_response, source_language)
        
        return final_response
    
    def _generate_gemini_response(self, question: str, context: str) -> str:
        """Generate response using Gemini API with enhanced prompting"""
        try:
            prompt = f"""You are a helpful College Code of Conduct Assistant. Your role is to provide accurate and concise answers about college rules and regulations. Your responses must be based **solely** on the provided context, which is retrieved from the college's official policies.

USER QUESTION: {question}

COLLEGE CODE OF CONDUCT CONTEXT:
{context}

INSTRUCTIONS:
1. **Relevance Check**: First, determine if the user's question is related to the college's code of conduct, rules, or student policies.

2. **If Related**:
   - Provide a direct and well-structured answer using only the provided context.
   - Use clear headings (##) and bullet points to organize the information.
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

            print("🧠 Generating enhanced AI response...")
            response = self.gemini_model.generate_content(prompt)
            # Clean up markdown formatting from the response
            cleaned_response = self.clean_markdown_formatting(response.text)
            return cleaned_response
            
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            print("   Falling back to basic response...")
            return self._generate_basic_response(question, self.search_documents(question))
    
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
    
    def _generate_basic_response(self, question: str, relevant_docs: List[Dict]) -> str:
        """Generate basic response without Gemini"""
        # Check if question seems MongoDB-related
        mongodb_keywords = ['mongo', 'database', 'collection', 'document', 'query', 'index', 'atlas', 'aggregation']
        is_mongodb_related = any(keyword in question.lower() for keyword in mongodb_keywords)
        
        if not relevant_docs:
            if is_mongodb_related:
                return """I couldn't find specific information about that in the MongoDB documentation. 

Try asking about:
• General information and support
• How to get help with specific topics
• Best practices and guidelines
• Policies and procedures
• Frequently asked questions"""
            else:
                return """Hi!! How can I help you today?

I can assist you with:
• General information and support
• Best practices and guidelines
• Policies and procedures
• Frequently asked questions
• Any topic you need help with

What would you like to know?"""
        
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
        """Summarize a specific page using Gemini API with multilingual support"""
        # Detect language and translate title to English for search
        english_title, source_language = self.detect_and_translate_to_english(title)
        
        print(f"📄 Looking for page: {english_title}")
        
        page = self.find_page_by_title(english_title)
        if not page:
            # Try partial matching
            matches = []
            for doc in self.full_data:
                if english_title.lower() in doc.get('title', '').lower():
                    matches.append(doc)
            
            if matches:
                page = matches[0]
                print(f"✅ Found similar page: {page['title']}")
            else:
                error_msg = f"I couldn't find a page titled '{title}'. Try a different title or ask a general question."
                return self.translate_to_language(error_msg, source_language)
        
        content = page.get('body', '')
        page_title = page.get('title', 'Unknown')
        
        if self.use_gemini:
            english_summary = self._generate_gemini_summary(page_title, content)
        else:
            # Return first part of the content
            if len(content) > 1000:
                content = content[:1000] + "..."
            english_summary = f"**{page_title}**\n\n{content}"
        
        # Translate summary back to source language
        return self.translate_to_language(english_summary, source_language)
    
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

4. **Make it practical**: Focus on information developers can actually use
5. **Keep it comprehensive but readable**: Don't skip important details, but organize them well

6. **End with**: Practical next steps or related topics to explore

SUMMARY:"""

            print("🧠 Generating enhanced AI summary...")
            response = self.gemini_model.generate_content(prompt)
            return f"## Summary: {title}\n\n{response.text}"
            
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            print("   Falling back to basic summary...")
            if len(content) > 1000:
                content = content[:1000] + "..."
            return f"**{title}**\n\n{content}"
    
    def chat(self):
        """Main chat loop with multilingual support"""
        print("\n" + "="*60)
        print("💬 Qunix Smart Support AI Assistant - Interactive Mode")
        print("="*60)
        print("🌍 Ask me anything in any language!")
        print("Examples:")
        print("  • What are the best practices?")
        print("  • सबसे अच्छी प्रथाएं क्या हैं?")
        print("  • সেরা অনুশীলন কী?")
        print("  • சிறந்த நடைமுறைகள் என்ன?")
        print("  • Type 'quit' to exit")
        print("-"*60)
        
        while True:
            try:
                user_input = input("\n🤔 Your question: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using Multilingual MongoDB AI Assistant!")
                    break
                
                # Determine if it's a summarization request
                # Check in multiple languages
                summarize_keywords = ['summarize', 'summary', 'सारांश', 'সারসংক্ষেপ', 'சுருக்கம்']
                is_summarize = any(word in user_input.lower() for word in summarize_keywords)
                
                if is_summarize:
                    # Extract title (this is basic - could be improved)
                    for keyword in summarize_keywords:
                        if keyword in user_input.lower():
                            title_start = user_input.lower().find(keyword) + len(keyword)
                            title = user_input[title_start:].strip().strip('"').strip("'")
                            break
                    
                    if title:
                        response = self.summarize_page(title)
                    else:
                        # Translate error message to user's language
                        english_error = "Please specify which page you'd like me to summarize."
                        _, source_lang = self.detect_and_translate_to_english(user_input)
                        response = self.translate_to_language(english_error, source_lang)
                else:
                    # Regular Q&A
                    response = self.answer_question(user_input)
                
                print(f"\n🤖 **Qunix Smart Support Assistant:**")
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using Qunix Smart Support AI Assistant!")
                break
            except Exception as e:
                print(f"\n❌ Sorry, I encountered an error: {e}")

def test_translation():
    """Test the translation functionality"""
    print("🧪 Testing translation functionality...")
    
    examples = [
        "I am Vishesh Jain",
        "मुझे चाय पीना बहुत पसंद है।",
        "আজ আকাশটা খুব সুন্দর লাগছে।",
        "நான் புத்தகம் படிக்க விரும்புகிறேன்",
        "నేడు వాతావరణం చల్లగా ఉంది",
        "मला माझ्या मित्रांसोबत खेळायला आवडते"
    ]
    
    agent = MultilingualAgent()
    
    for example in examples:
        print(f"\nOriginal: {example}")
        translated, lang = agent.detect_and_translate_to_english(example)
        print(f"Translated to English: {translated}")
        print(f"Detected language: {lang}")
        
        # Test translating back
        back_translated = agent.translate_to_language("Hello, how are you?", lang)
        print(f"'Hello, how are you?' in {lang}: {back_translated}")
        print("-" * 50)

def main():
    """Main function"""
    try:
        # Uncomment the line below to test translation first
        # test_translation()
        
        agent = MultilingualAgent()
        agent.chat()
    except Exception as e:
        print(f"❌ Error starting the assistant: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()