#!/usr/bin/env python3
"""
Start the FastAPI server
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting MongoDB RAG Chat API Server...")
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )