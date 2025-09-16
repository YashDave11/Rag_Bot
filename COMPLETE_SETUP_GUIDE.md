# 🚀 Complete MongoDB Chat Widget Setup Guide

## 🎯 **What We've Built**

A complete chat widget system with:

- ✅ **FastAPI Backend** - MongoDB RAG-powered API
- ✅ **React Chat Widget** - Beautiful, responsive interface
- ✅ **Embedding System** - One-line integration for any website
- ✅ **Customization Options** - Themes, colors, positioning

## 📁 **Project Structure**

```
rag-chatbot/
├── 📄 api_server.py              # FastAPI backend
├── 📄 start_server.py            # Backend startup script
├── 📄 clean_interactive_agent.py # Standalone chat agent
├── 📁 data/                      # MongoDB documentation
├── 📁 mongodb-chat-widget/       # React widget
│   ├── 📁 src/components/        # React components
│   ├── 📁 public/
│   │   └── 📄 embed.js          # Embedding script
│   └── 📄 package.json
├── 📄 example-website.html       # Integration example
├── 📄 test-embedding.html        # Embedding test page
└── 📄 EMBEDDING_GUIDE.md         # Integration docs
```

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Start the Backend API**

```bash
# In the main project directory
python start_server.py
```

✅ API runs on `http://localhost:8000`

### **Step 2: Start the React Development Server**

```bash
# Navigate to React project
cd mongodb-chat-widget

# Start development server
npm start
```

✅ React app runs on `http://localhost:3000`

### **Step 3: Test the Embedding**

Open `test-embedding.html` in your browser to see the widget in action!

## 🌐 **Integration Examples**

### **Simplest Integration (1 line)**

```html
<script src="http://localhost:3000/embed.js" data-mongodb-chat></script>
```

### **Custom Configuration**

```html
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-api-url="http://localhost:8000"
  data-title="MongoDB Expert"
  data-subtitle="Ask me anything about MongoDB"
  data-primary-color="#00A86B"
  data-position="bottom-right"
></script>
```

### **Multiple Positions**

```html
<!-- Support chat (bottom-right) -->
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-title="Technical Support"
  data-position="bottom-right"
></script>

<!-- Sales chat (bottom-left) -->
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-title="Sales Assistant"
  data-primary-color="#007bff"
  data-position="bottom-left"
></script>
```

## 🎨 **Customization Options**

| Option               | Default                         | Description       |
| -------------------- | ------------------------------- | ----------------- |
| `data-api-url`       | `http://localhost:8000`         | Backend API URL   |
| `data-title`         | `MongoDB Assistant`             | Chat header title |
| `data-subtitle`      | `Ask me anything about MongoDB` | Header subtitle   |
| `data-primary-color` | `#00A86B`                       | Theme color       |
| `data-position`      | `bottom-right`                  | Widget position   |

## 🧪 **Testing Your Setup**

### **1. Backend Test**

```bash
# Test API directly
python test_api.py

# Or visit in browser
http://localhost:8000/health
```

### **2. React Widget Test**

```bash
# Start React dev server
cd mongodb-chat-widget
npm start

# Visit: http://localhost:3000
```

### **3. Embedding Test**

Open these files in your browser:

- `test-embedding.html` - Basic embedding test
- `example-website.html` - Full website example

## 🔧 **Development Workflow**

### **Making Changes to the Chat Widget**

1. Edit files in `mongodb-chat-widget/src/`
2. Changes auto-reload in development
3. Test in browser at `http://localhost:3000`

### **Making Changes to the Backend**

1. Edit `api_server.py` or related files
2. Restart with `python start_server.py`
3. Test API endpoints

### **Making Changes to Embedding**

1. Edit `mongodb-chat-widget/public/embed.js`
2. Test with `test-embedding.html`
3. No restart needed (static file)

## 🚀 **Production Deployment**

### **1. Build the React App**

```bash
cd mongodb-chat-widget
npm run build
```

### **2. Host the Files**

- Host `build/` folder contents on your CDN
- Update embed.js URL in integration code
- Deploy FastAPI backend to your server

### **3. Update URLs**

```html
<script
  src="https://your-cdn.com/embed.js"
  data-mongodb-chat
  data-api-url="https://your-api.com"
></script>
```

## 📋 **Troubleshooting**

### **Widget Not Appearing**

- ✅ Check if both servers are running
- ✅ Verify embed.js URL is accessible
- ✅ Check browser console for errors

### **API Connection Issues**

- ✅ Ensure backend is running on correct port
- ✅ Check CORS configuration
- ✅ Verify API URL in embed script

### **Chat Not Responding**

- ✅ Test API directly: `http://localhost:8000/health`
- ✅ Check network tab for failed requests
- ✅ Verify Gemini API key is working

## 🎯 **What You Can Do Now**

✅ **Embed on Any Website** - Just add one script tag
✅ **Customize Appearance** - Colors, titles, positions
✅ **Handle MongoDB Questions** - AI-powered responses
✅ **Scale to Production** - Ready for real deployment
✅ **Mobile Responsive** - Works on all devices

## 🎉 **Success!**

You now have a complete, production-ready MongoDB chat widget system that can be embedded on any website with a single line of code!

### **Next Steps:**

1. 🌐 Deploy to production servers
2. 🎨 Add more customization options
3. 📊 Add analytics and monitoring
4. 🔧 Add admin dashboard
5. 🚀 Scale to handle more traffic

**Happy chatting!** 🤖💬
