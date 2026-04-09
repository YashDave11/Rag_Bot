#!/usr/bin/env python3
"""
Startup script for ChatMongo SaaS Platform - Phase 1
User Registration & Authentication
"""

import uvicorn
import os
from pathlib import Path

def main():
    print("🚀 Starting ChatMongo SaaS Platform - Phase 1")
    print("=" * 50)
    print("📋 Phase 1 Features:")
    print("   • User registration with email")
    print("   • Session-based authentication")
    print("   • Dashboard with user info")
    print("   • Secure API key management")
    print("   • Original MongoDB chat (backward compatibility)")
    print()
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("   Please create .env file with your API keys")
        print("   Example:")
        print("   GEMINI_API_KEY=your_api_key_here")
        print("   ALLOWED_ORIGINS=http://localhost:3000")
        print()
    
    print("🌐 Server will be available at:")
    print("   • API: http://localhost:8000")
    print("   • Docs: http://localhost:8000/docs")
    print("   • Health: http://localhost:8000/health")
    print()
    print("📱 Frontend:")
    print("   • Main page: saas-website/index.html")
    print("   • Dashboard: saas-website/dashboard.html")
    print()
    print("🔧 To test:")
    print("   1. Open saas-website/index.html in browser")
    print("   2. Click 'Start Free Trial'")
    print("   3. Enter your email")
    print("   4. Get redirected to dashboard")
    print()
    
    # Start the server
    uvicorn.run(
        "enhanced_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()