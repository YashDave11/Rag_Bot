# How to Run the Project

This guide will help you set up and run the MongoDB GenAI ChatMongo SaaS application.

## Project Location

This project is located at: `C:\Users\yashd\Music\Rag_Chatbot\rag-chatbot`

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB instance)
- Google Gemini API key
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

If you haven't already, navigate to the project directory:

```bash
cd C:\Users\yashd\Music\Rag_Chatbot\rag-chatbot
```

Or clone from repository:

```bash
git clone <repository-url>
cd rag-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create or update the `.env` file in the project root with the following variables:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# API Server Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000
API_HOST=0.0.0.0
API_PORT=8000
```

To get a Gemini API key:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

### 4. Set Up MongoDB

Make sure you have MongoDB running either:

- **MongoDB Atlas**: Create a free cluster at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- **Local MongoDB**: Install and run MongoDB locally

## Running the Application

### Option 1: Run the Main API Server

```bash
python phase3a_api_server.py
```

This will start the FastAPI server on `http://localhost:8000`

### Option 2: Run Enhanced API Server

```bash
python enhanced_api_server.py
```

### Option 3: Run Multilingual API Server

```bash
python multilingual_api_server.py
```

### Option 4: Run Interactive Agent

```bash
python interactive_agent.py
```

## Testing the Application

### Test the API

```bash
python test_phase3a.py
```

### Test with Web Interface

1. Start the API server (see above)
2. Open `saas-website/index.html` in your browser
3. Or open `saas-website/dashboard.html` for the dashboard view

### Test Chat Widget

Navigate to the chat widget directories:

- `chat-widget/` - Basic chat widget
- `mongodb-chat-widget/` - MongoDB-themed chat widget

## Project Structure

```
.
├── saas-website/          # Main SaaS website files
│   ├── index.html         # Landing page
│   └── dashboard.html     # Dashboard interface
├── chat-widget/           # Basic chat widget
├── mongodb-chat-widget/   # MongoDB-themed chat widget
├── data/                  # Data files and embeddings
├── notebooks/             # Jupyter notebooks
├── phase3a_api_server.py  # Main API server
├── all_data.py            # Data management module
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Available API Endpoints

Once the server is running, visit:

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- Chat Endpoint: `http://localhost:8000/chat`

## Troubleshooting

### Gemini API Errors

If you see errors like "404 models/gemini-x.x-xxx is not found":

- Make sure you're using Gemini 2.0 models (already configured in the latest version)
- Update the SDK: `pip install --upgrade google-generativeai`
- Check your API key is valid

### MongoDB Connection Issues

- Verify your MongoDB connection string
- Check network connectivity
- Ensure your IP is whitelisted in MongoDB Atlas

### Port Already in Use

If port 8000 is already in use:

- Change the `API_PORT` in `.env` file
- Or stop the process using port 8000

## Additional Resources

- [Vector Search Lab](https://mongodb-developer.github.io/vector-search-lab/)
- [Building RAG Applications](https://mongodb-developer.github.io/ai-rag-lab/)
- [Building AI Agents](https://mongodb-developer.github.io/ai-agents-lab/)

## Support

For issues or questions, please refer to the MongoDB Developer documentation or create an issue in the repository.
