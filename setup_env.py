#!/usr/bin/env python3
"""
Setup environment variables for the AI Agents Lab
"""

import os

def setup_environment():
    """Set up required environment variables"""
    
    print("🔧 Setting up environment for AI Agents Lab...")
    
    # For demo purposes, we'll use mock values
    # In a real workshop, you'd get these from MongoDB Atlas and your LLM provider
    
    # Mock MongoDB URI (you'd replace this with your actual Atlas connection string)
    mock_mongodb_uri = "mongodb+srv://username:password@cluster.mongodb.net/database"
    
    # Mock serverless URL (this is from the workshop infrastructure)
    mock_serverless_url = "https://vtqjvgchmwcjwsrela2oyhlegu0hwqnw.lambda-url.us-west-2.on.aws/"
    
    # Set environment variables
    os.environ["MONGODB_URI"] = mock_mongodb_uri
    os.environ["SERVERLESS_URL"] = mock_serverless_url
    
    print("✅ Environment variables set:")
    print(f"   MONGODB_URI: {mock_mongodb_uri[:50]}...")
    print(f"   SERVERLESS_URL: {mock_serverless_url[:50]}...")
    
    print("\n⚠️  NOTE: These are mock values for demo purposes.")
    print("   For a real implementation, you would need:")
    print("   1. A real MongoDB Atlas connection string")
    print("   2. API keys for your chosen LLM provider")
    print("   3. The actual workshop serverless endpoint")
    
    return True

if __name__ == "__main__":
    setup_environment()