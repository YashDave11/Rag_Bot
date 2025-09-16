# 🤖 MongoDB RAG Chat Widget

A beautiful, embeddable React chat widget powered by MongoDB RAG (Retrieval-Augmented Generation) and Gemini AI.

## ✨ Features

- 🎯 **AI-Powered**: Uses Gemini AI for intelligent MongoDB assistance
- 💬 **Beautiful UI**: Modern, responsive chat interface
- 🔧 **Easy Integration**: One-line script tag integration
- 🎨 **Customizable**: Colors, position, and messages
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🔄 **Session Management**: Maintains conversation history
- ⚡ **Real-time**: Instant responses with typing indicators

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd chat-widget
npm install
```

### 2. Development Mode

```bash
npm run dev
```

Visit `http://localhost:3000` to see the widget in action.

### 3. Build for Production

```bash
npm run build-widget
```

This creates `dist/mongodb-chat-widget.umd.js` for embedding.

## 🔧 Integration

### Simple Integration

Add this single line to any website:

```html
<script
  src="mongodb-chat-widget.umd.js"
  data-api-url="http://localhost:8000"
></script>
```

### Advanced Integration

```html
<script
  src="mongodb-chat-widget.umd.js"
  data-api-url="http://localhost:8000"
  data-position="bottom-right"
  data-primary-color="#007bff"
  data-title="MongoDB Assistant"
  data-welcome-message="Hello! How can I help you with MongoDB today?"
></script>
```

### Programmatic Integration

```javascript
const widget = window.MongoDBChatWidget.init({
  apiUrl: "http://localhost:8000",
  position: "bottom-left",
  primaryColor: "#28a745",
  title: "Custom Assistant",
  welcomeMessage: "Welcome! Ask me anything about MongoDB.",
});

// Later, destroy the widget
widget.destroy();
```

## ⚙️ Configuration Options

| Option           | Type   | Default                                | Description                                                              |
| ---------------- | ------ | -------------------------------------- | ------------------------------------------------------------------------ |
| `apiUrl`         | string | `http://localhost:8000`                | Backend API URL                                                          |
| `position`       | string | `bottom-right`                         | Widget position (`bottom-right`, `bottom-left`, `top-right`, `top-left`) |
| `primaryColor`   | string | `#007bff`                              | Primary color for the widget                                             |
| `title`          | string | `MongoDB Assistant`                    | Chat header title                                                        |
| `welcomeMessage` | string | `Hello! I'm your MongoDB assistant...` | Initial bot message                                                      |

## 📱 Mobile Support

The widget automatically adapts to mobile screens:

- Full-screen chat on small devices
- Touch-friendly interface
- Responsive design

## 🎨 Customization

### Colors

```html
<script src="mongodb-chat-widget.umd.js" data-primary-color="#e74c3c"></script>
```

### Position

```html
<script src="mongodb-chat-widget.umd.js" data-position="top-left"></script>
```

### Custom Messages

```html
<script
  src="mongodb-chat-widget.umd.js"
  data-title="My Custom Bot"
  data-welcome-message="Welcome to our MongoDB support!"
></script>
```

## 🔌 API Requirements

The widget requires a running FastAPI backend with these endpoints:

- `POST /chat` - Send messages
- `GET /health` - Health check
- `GET /chat/history/{session_id}` - Chat history

Make sure your API has CORS enabled for web integration.

## 📦 Files Structure

```
chat-widget/
├── src/
│   ├── ChatWidget.jsx      # Main React component
│   ├── ChatWidget.css      # Widget styles
│   ├── main.jsx           # Development entry
│   └── widget.jsx         # Production widget entry
├── dist/                  # Built files
├── package.json
├── vite.config.js
└── README.md
```

## 🛠️ Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run build-widget` - Build embeddable widget
- `npm run preview` - Preview production build

### Testing

1. Start the FastAPI backend: `python start_server.py`
2. Start the widget dev server: `npm run dev`
3. Open `http://localhost:3000`

## 🌐 Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 📄 License

MIT License - feel free to use in your projects!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

Made with ❤️ for the MongoDB community
