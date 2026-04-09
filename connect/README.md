# MongoDB Chat Assistant - Local Integration

This folder contains a basic website integration of the MongoDB Chat Assistant widget.

## Quick Start

1. **Start the API Server**

   ```bash
   python start_server.py
   ```

   This will start the FastAPI server on `http://localhost:8000`

2. **Start the React Chat Widget Server**

   ```bash
   cd chat-widget
   npm start
   ```

   This will start the React development server on `http://localhost:3000`

3. **Open the Website**

   - Open `connect/index.html` in your web browser
   - Or serve it locally: `python -m http.server 8080` and visit `http://localhost:8080/connect/`

4. **Use the Chat Assistant**
   - Look for the chat bubble in the bottom-right corner
   - Click it to open the chat window
   - Ask MongoDB questions and get instant AI-powered answers!

## Features

- ✅ **Live Chat Widget** - Interactive chat bubble with MongoDB AI assistant
- ✅ **Server Status Indicator** - Shows if the API server is running
- ✅ **Responsive Design** - Works on desktop and mobile devices
- ✅ **Sample Questions** - Click on suggested questions to try them out
- ✅ **Real-time Health Check** - Automatically checks server connectivity

## Configuration

The chat widget is configured with:

- **API URL**: `http://localhost:8000` (your local server)
- **Position**: Bottom-right corner
- **Primary Color**: Green (#00a86b)
- **Welcome Message**: Custom MongoDB assistant greeting

## Troubleshooting

### Chat Widget Not Appearing

1. Make sure `start_server.py` is running (API server on port 8000)
2. Make sure the React dev server is running on port 3000 (`cd chat-widget && npm start`)
3. Check that both servers are accessible
4. Refresh the page
5. Check browser console for any errors

### Server Status Shows Offline

1. Run `python start_server.py` in your terminal (API server)
2. Run `cd chat-widget && npm start` in another terminal (React server)
3. Wait for both servers to fully start
4. Refresh the page

### CORS Issues

If you see CORS errors, make sure you're either:

- Opening the HTML file directly in browser, OR
- Serving it from a local server (recommended)

## Sample Questions to Try

- "How do I create an index in MongoDB?"
- "What are MongoDB aggregation pipelines?"
- "How to optimize MongoDB queries?"
- "MongoDB vs SQL differences"
- "How to connect to MongoDB from Python?"
- "What is sharding in MongoDB?"

## Integration Notes

This example shows how to integrate the MongoDB chat widget into any website with just a few lines of code:

```html
<script
  src="../chat-widget/dist/mongodb-chat-widget.umd.js"
  data-api-url="http://localhost:8000"
  data-position="bottom-right"
  data-primary-color="#00a86b"
  data-title="MongoDB Assistant"
  data-welcome-message="Hi! I'm your MongoDB assistant..."
></script>
```

You can customize the widget by modifying the `data-*` attributes.
