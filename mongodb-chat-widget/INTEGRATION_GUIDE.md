# 🚀 MongoDB Chat Widget - Integration Guide

## 🎯 Quick Integration

### Method 1: Simple Script Tag (Easiest)

Add this to your website's HTML:

```html
<!-- Add before closing </body> tag -->
<script
  src="http://localhost:3000/static/js/mongodb-chat-widget.js"
  data-mongodb-chat
  data-api-url="http://localhost:8000"
  data-theme="default"
  data-position="bottom-right"
></script>
```

### Method 2: JavaScript Initialization

```html
<script src="http://localhost:3000/static/js/mongodb-chat-widget.js"></script>
<script>
  const widget = new MongoDBChatWidget({
    apiUrl: "http://localhost:8000",
    theme: "default",
    position: "bottom-right",
  });
  widget.init();
</script>
```

### Method 3: React Component (For React Apps)

```jsx
import ChatBubble from "./components/ChatBubble";

function App() {
  return (
    <div>
      {/* Your app content */}
      <ChatBubble apiUrl="http://localhost:8000" />
    </div>
  );
}
```

## ⚙️ Configuration Options

| Option        | Type   | Default                 | Description          |
| ------------- | ------ | ----------------------- | -------------------- |
| `apiUrl`      | string | `http://localhost:8000` | Backend API URL      |
| `theme`       | string | `default`               | Widget theme         |
| `position`    | string | `bottom-right`          | Widget position      |
| `containerId` | string | `mongodb-chat-widget`   | Container element ID |

## 🎨 Customization

### Themes

- `default` - MongoDB green theme
- `blue` - Blue corporate theme
- `dark` - Dark mode theme
- `minimal` - Minimal design

### Positions

- `bottom-right` (default)
- `bottom-left`
- `top-right`
- `top-left`

## 📱 Features

✅ **Responsive Design** - Works on desktop and mobile
✅ **Session Management** - Maintains conversation history
✅ **Typing Indicators** - Shows when AI is thinking
✅ **Error Handling** - Graceful fallbacks
✅ **Accessibility** - Keyboard navigation support
✅ **Customizable** - Easy theming and positioning

## 🔧 Development Setup

1. **Start Backend API:**

   ```bash
   python start_server.py
   ```

2. **Start React Development Server:**

   ```bash
   cd mongodb-chat-widget
   npm start
   ```

3. **Build for Production:**
   ```bash
   npm run build
   ```

## 🌐 Production Deployment

1. **Build the widget:**

   ```bash
   npm run build
   ```

2. **Host the built files** on your CDN/server

3. **Update script src** to your hosted URL:
   ```html
   <script src="https://your-domain.com/mongodb-chat-widget.js"></script>
   ```

## 📋 Example Integration

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Website</title>
  </head>
  <body>
    <h1>Welcome to My Website</h1>
    <p>This website has a MongoDB chat assistant!</p>

    <!-- MongoDB Chat Widget -->
    <script
      src="http://localhost:3000/static/js/mongodb-chat-widget.js"
      data-mongodb-chat
      data-api-url="http://localhost:8000"
    ></script>
  </body>
</html>
```

## 🚀 Next Steps

The widget is now ready for:

- ✅ Website integration
- ✅ Customization
- ✅ Production deployment
- ✅ Multiple site usage

Happy chatting! 🎉
