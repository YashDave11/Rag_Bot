#!/usr/bin/env python3
"""
Simple test server without external dependencies
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test server is running!", "status": "ok"}

@app.post("/auth/register")
async def register(data: dict):
    return {
        "user_id": "test123",
        "email": data.get("email", "test@example.com"),
        "api_key": "test_key",
        "created_at": "2024-01-01",
        "widget_status": "none",
        "message_count": 0,
        "message_limit": 300
    }

@app.get("/auth/me")
async def get_me():
    return {
        "user_id": "test123",
        "email": "test@example.com",
        "api_key": "test_key",
        "created_at": "2024-01-01",
        "widget_status": "none",
        "message_count": 0,
        "message_limit": 300
    }

if __name__ == "__main__":
    print("🧪 Starting simple test server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)