# 🚀 MongoDB Chat Widget - Complete Embedding Guide

## ✨ **One-Line Integration**

Add our MongoDB chat widget to ANY website with just one script tag:

```html
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-api-url="http://localhost:8000"
></script>
```

That's it! The chat bubble will appear on your website instantly! 🎉

## 🎛️ **Customization Options**

### Basic Configuration

```html
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-api-url="http://localhost:8000"
  data-title="MongoDB Assistant"
  data-subtitle="Ask me anything about MongoDB"
  data-primary-color="#00A86B"
  data-position="bottom-right"
></script>
```

### Available Options

| Attribute            | Default                         | Description          |
| -------------------- | ------------------------------- | -------------------- |
| `data-api-url`       | `http://localhost:8000`         | Your backend API URL |
| `data-title`         | `MongoDB Assistant`             | Chat header title    |
| `data-subtitle`      | `Ask me anything about MongoDB` | Chat header subtitle |
| `data-primary-color` | `#00A86B`                       | Primary theme color  |
| `data-position`      | `bottom-right`                  | Widget position      |

### Position Options

- `bottom-right` (default)
- `bottom-left`
- `top-right`
- `top-left`

## 🌈 **Theme Examples**

### Corporate Blue Theme

```html
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-primary-color="#007bff"
  data-title="Database Assistant"
></script>
```

### Dark Theme

```html
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-primary-color="#343a40"
  data-title="MongoDB Expert"
></script>
```

### Custom Branding

```html
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-primary-color="#ff6b35"
  data-title="YourCompany DB Help"
  data-subtitle="MongoDB support for your team"
></script>
```

## 📋 **Complete Integration Examples**

### 1. Simple Blog Integration

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Tech Blog</title>
  </head>
  <body>
    <h1>Welcome to My Blog</h1>
    <p>Content about MongoDB and databases...</p>

    <!-- MongoDB Chat Widget -->
    <script src="http://localhost:3000/embed.js" data-mongodb-chat></script>
  </body>
</html>
```

### 2. E-commerce Site

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Database Solutions Store</title>
  </head>
  <body>
    <header>
      <h1>Database Solutions</h1>
    </header>

    <main>
      <h2>MongoDB Hosting Services</h2>
      <p>Need help choosing the right MongoDB solution?</p>
    </main>

    <!-- MongoDB Expert Chat -->
    <script
      src="http://localhost:3000/embed.js"
      data-mongodb-chat
      data-title="MongoDB Expert"
      data-subtitle="Get help choosing the right solution"
      data-primary-color="#28a745"
    ></script>
  </body>
</html>
```

### 3. Documentation Site

```html
<!DOCTYPE html>
<html>
  <head>
    <title>MongoDB Documentation</title>
  </head>
  <body>
    <nav>Documentation Menu</nav>

    <main>
      <h1>MongoDB Guide</h1>
      <p>Comprehensive MongoDB documentation...</p>
    </main>

    <!-- Interactive Help -->
    <script
      src="http://localhost:3000/embed.js"
      data-mongodb-chat
      data-title="Interactive Help"
      data-subtitle="Ask questions about this documentation"
      data-position="bottom-left"
    ></script>
  </body>
</html>
```

## 🔧 **Advanced Integration**

### Multiple Widgets (Different Configurations)

```html
<!-- Support Chat -->
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-title="Technical Support"
  data-position="bottom-right"
></script>

<!-- Sales Chat -->
<script
  src="http://localhost:3000/embed.js"
  data-mongodb-chat
  data-title="Sales Assistant"
  data-primary-color="#007bff"
  data-position="bottom-left"
></script>
```

### Conditional Loading

```html
<script>
  // Only load chat widget on certain pages
  if (window.location.pathname.includes("/mongodb")) {
    const script = document.createElement("script");
    script.src = "http://localhost:3000/embed.js";
    script.setAttribute("data-mongodb-chat", "");
    document.body.appendChild(script);
  }
</script>
```

## 🚀 **Production Setup**

### 1. Host the Embed Script

Build and host the embed.js file on your CDN:

```bash
# Build the React app
cd mongodb-chat-widget
npm run build

# Host the embed.js file
# Update script src to your hosted URL
```

### 2. Update API URL

```html
<script
  src="https://your-cdn.com/embed.js"
  data-mongodb-chat
  data-api-url="https://your-api.com"
></script>
```

### 3. HTTPS Configuration

Ensure both your embed script and API use HTTPS in production.

## 📱 **Mobile Optimization**

The widget automatically adapts to mobile devices:

- Responsive design
- Touch-friendly interface
- Proper viewport handling
- Keyboard support

## 🎯 **Testing Your Integration**

### 1. Test the Example

Open `example-website.html` in your browser to see the widget in action.

### 2. Verify Integration

- ✅ Chat bubble appears in correct position
- ✅ Clicking opens/closes chat window
- ✅ Messages send and receive properly
- ✅ Styling matches your site

### 3. Test on Different Devices

- Desktop browsers
- Mobile devices
- Tablets
- Different screen sizes

## 🔍 **Troubleshooting**

### Widget Not Appearing

1. Check if embed.js is loading (Network tab in DevTools)
2. Verify API URL is correct and accessible
3. Check browser console for errors

### API Connection Issues

1. Ensure backend server is running
2. Check CORS configuration
3. Verify API URL in script attributes

### Styling Conflicts

The widget uses high z-index (999999) and isolated styles to avoid conflicts.

## 🎉 **You're Ready!**

Your MongoDB chat widget is now ready for:

- ✅ **Any Website** - Works with any HTML page
- ✅ **Easy Customization** - Simple data attributes
- ✅ **Production Use** - Scalable and reliable
- ✅ **Mobile Ready** - Responsive design
- ✅ **Zero Dependencies** - Pure JavaScript

Just add one script tag and you're done! 🚀
