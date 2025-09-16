import React from "react";
import ReactDOM from "react-dom/client";
import ChatBubble from "./components/ChatBubble";

// Embeddable Widget Class
class MongoDBChatWidget {
  constructor(options = {}) {
    this.options = {
      apiUrl: options.apiUrl || "http://localhost:8000",
      containerId: options.containerId || "mongodb-chat-widget",
      theme: options.theme || "default",
      position: options.position || "bottom-right",
      ...options,
    };

    this.container = null;
    this.root = null;
  }

  // Initialize the widget
  init() {
    // Create container if it doesn't exist
    this.container = document.getElementById(this.options.containerId);

    if (!this.container) {
      this.container = document.createElement("div");
      this.container.id = this.options.containerId;
      document.body.appendChild(this.container);
    }

    // Create React root and render
    this.root = ReactDOM.createRoot(this.container);
    this.render();
  }

  // Render the widget
  render() {
    if (this.root) {
      this.root.render(
        <ChatBubble
          apiUrl={this.options.apiUrl}
          theme={this.options.theme}
          position={this.options.position}
        />
      );
    }
  }

  // Destroy the widget
  destroy() {
    if (this.root) {
      this.root.unmount();
      this.root = null;
    }

    if (this.container && this.container.parentNode) {
      this.container.parentNode.removeChild(this.container);
      this.container = null;
    }
  }

  // Update widget options
  updateOptions(newOptions) {
    this.options = { ...this.options, ...newOptions };
    this.render();
  }
}

// Global function for easy integration
window.MongoDBChatWidget = MongoDBChatWidget;

// Auto-initialize if script tag has data attributes
document.addEventListener("DOMContentLoaded", () => {
  const scripts = document.querySelectorAll("script[data-mongodb-chat]");

  scripts.forEach((script) => {
    const options = {
      apiUrl: script.getAttribute("data-api-url") || "http://localhost:8000",
      theme: script.getAttribute("data-theme") || "default",
      position: script.getAttribute("data-position") || "bottom-right",
    };

    const widget = new MongoDBChatWidget(options);
    widget.init();
  });
});

export default MongoDBChatWidget;
