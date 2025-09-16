/**
 * MongoDB RAG Chat Widget - Professional Embed Script
 * Version: 2.0.0
 *
 * Easy integration for any website:
 * <script src="https://your-domain.com/chat-widget.js" data-widget-key="your-api-key"></script>
 */

(function () {
  "use strict";

  // Configuration
  const WIDGET_CONFIG = {
    version: "2.0.0",
    apiUrl: "http://localhost:8000", // Your API endpoint
    widgetUrl: "http://localhost:3000", // Your widget hosting URL
    defaultTheme: {
      primaryColor: "#00A86B",
      title: "MongoDB Assistant",
      subtitle: "Ask me anything about MongoDB",
      position: "bottom-right",
    },
  };

  // Utility functions
  const utils = {
    // Get script configuration from data attributes
    getConfig() {
      const script = document.querySelector(
        'script[data-widget-key], script[src*="chat-widget.js"]'
      );
      if (!script) return WIDGET_CONFIG.defaultTheme;

      return {
        widgetKey: script.getAttribute("data-widget-key"),
        apiUrl: script.getAttribute("data-api-url") || WIDGET_CONFIG.apiUrl,
        primaryColor:
          script.getAttribute("data-primary-color") ||
          WIDGET_CONFIG.defaultTheme.primaryColor,
        title:
          script.getAttribute("data-title") || WIDGET_CONFIG.defaultTheme.title,
        subtitle:
          script.getAttribute("data-subtitle") ||
          WIDGET_CONFIG.defaultTheme.subtitle,
        position:
          script.getAttribute("data-position") ||
          WIDGET_CONFIG.defaultTheme.position,
        welcomeMessage: script.getAttribute("data-welcome-message"),
        showPoweredBy: script.getAttribute("data-show-powered-by") !== "false",
        autoOpen: script.getAttribute("data-auto-open") === "true",
        theme: script.getAttribute("data-theme") || "default",
      };
    },

    // Create unique container ID
    generateId() {
      return "mongodb-chat-widget-" + Math.random().toString(36).substr(2, 9);
    },

    // Get position styles
    getPositionStyles(position) {
      const positions = {
        "bottom-right": { bottom: "20px", right: "20px" },
        "bottom-left": { bottom: "20px", left: "20px" },
        "top-right": { top: "20px", right: "20px" },
        "top-left": { top: "20px", left: "20px" },
      };
      return positions[position] || positions["bottom-right"];
    },

    // Inject CSS styles
    injectStyles(config) {
      if (document.getElementById("mongodb-chat-widget-styles")) return;

      const styles = `
        .mongodb-chat-widget-container {
          position: fixed;
          z-index: 999999;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
          ${Object.entries(this.getPositionStyles(config.position))
            .map(([key, value]) => `${key}: ${value}`)
            .join("; ")};
        }

        .mongodb-chat-toggle {
          width: 64px;
          height: 64px;
          border-radius: 50%;
          background: linear-gradient(135deg, ${config.primaryColor}dd, ${
        config.primaryColor
      });
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          overflow: hidden;
        }

        .mongodb-chat-toggle:hover {
          transform: scale(1.1);
          box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
        }

        .mongodb-chat-toggle.has-notification::after {
          content: '';
          position: absolute;
          top: -2px;
          right: -2px;
          width: 12px;
          height: 12px;
          background: #ff4757;
          border-radius: 50%;
          border: 2px solid white;
          animation: pulse 2s infinite;
        }

        .mongodb-chat-window {
          position: absolute;
          ${config.position.includes("top") ? "top: 80px;" : "bottom: 80px;"}
          ${config.position.includes("left") ? "left: 0;" : "right: 0;"}
          width: 380px;
          height: 600px;
          background: white;
          border-radius: 16px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
          display: none;
          flex-direction: column;
          overflow: hidden;
          border: 1px solid rgba(0, 0, 0, 0.05);
          transform: translateY(20px) scale(0.95);
          opacity: 0;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .mongodb-chat-window.open {
          display: flex;
          transform: translateY(0) scale(1);
          opacity: 1;
        }

        .mongodb-chat-header {
          background: linear-gradient(135deg, ${config.primaryColor}, ${
        config.primaryColor
      }dd);
          color: white;
          padding: 20px;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .mongodb-chat-header-info {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .mongodb-chat-header-icon {
          width: 40px;
          height: 40px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
        }

        .mongodb-chat-header-title {
          font-weight: 600;
          font-size: 18px;
          margin-bottom: 2px;
        }

        .mongodb-chat-header-subtitle {
          font-size: 13px;
          opacity: 0.9;
        }

        .mongodb-chat-close {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          color: white;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s;
        }

        .mongodb-chat-close:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .mongodb-chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          background: linear-gradient(to bottom, #f8f9fa, #ffffff);
        }

        .mongodb-chat-message {
          margin-bottom: 20px;
          display: flex;
          flex-direction: column;
          animation: fadeIn 0.3s ease-out;
        }

        .mongodb-chat-message.user {
          align-items: flex-end;
        }

        .mongodb-chat-message.bot {
          align-items: flex-start;
        }

        .mongodb-chat-bubble {
          max-width: 85%;
          padding: 14px 18px;
          border-radius: 20px;
          font-size: 14px;
          line-height: 1.5;
          white-space: pre-wrap;
          word-wrap: break-word;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .mongodb-chat-bubble.user {
          background: linear-gradient(135deg, #007bff, #0056b3);
          color: white;
          border-radius: 20px 20px 4px 20px;
        }

        .mongodb-chat-bubble.bot {
          background: white;
          color: #333;
          border: 1px solid rgba(0, 0, 0, 0.05);
          border-radius: 20px 20px 20px 4px;
        }

        .mongodb-chat-time {
          font-size: 11px;
          color: #999;
          margin-top: 4px;
        }

        .mongodb-chat-input-container {
          padding: 20px;
          background: white;
          border-top: 1px solid rgba(0, 0, 0, 0.05);
          display: flex;
          gap: 12px;
          align-items: flex-end;
        }

        .mongodb-chat-input {
          flex: 1;
          border: 2px solid #e9ecef;
          border-radius: 24px;
          padding: 12px 18px;
          font-size: 14px;
          resize: none;
          max-height: 120px;
          min-height: 48px;
          font-family: inherit;
          outline: none;
          transition: all 0.2s;
          background: #f8f9fa;
        }

        .mongodb-chat-input:focus {
          border-color: ${config.primaryColor};
          background: white;
          box-shadow: 0 0 0 3px ${config.primaryColor}20;
        }

        .mongodb-chat-send {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          background: linear-gradient(135deg, ${config.primaryColor}, ${
        config.primaryColor
      }dd);
          border: none;
          color: white;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s;
          font-size: 16px;
        }

        .mongodb-chat-send:hover:not(:disabled) {
          transform: scale(1.05);
        }

        .mongodb-chat-send:disabled {
          background: #e9ecef;
          cursor: not-allowed;
        }

        .mongodb-chat-typing {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 14px 18px;
          background: white;
          border-radius: 20px 20px 20px 4px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          border: 1px solid rgba(0, 0, 0, 0.05);
          max-width: 85%;
        }

        .mongodb-chat-typing-dots {
          display: flex;
          gap: 4px;
        }

        .mongodb-chat-typing-dots span {
          width: 8px;
          height: 8px;
          background: ${config.primaryColor};
          border-radius: 50%;
          animation: typing 1.4s infinite ease-in-out;
        }

        .mongodb-chat-typing-dots span:nth-child(1) { animation-delay: -0.32s; }
        .mongodb-chat-typing-dots span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); }
        }

        @keyframes typing {
          0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
          40% { transform: scale(1); opacity: 1; }
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
          .mongodb-chat-window {
            width: calc(100vw - 20px);
            height: calc(100vh - 120px);
            left: 0 !important;
            right: 0 !important;
            margin: 0 auto;
          }
        }
      `;

      const styleSheet = document.createElement("style");
      styleSheet.id = "mongodb-chat-widget-styles";
      styleSheet.textContent = styles;
      document.head.appendChild(styleSheet);
    },
  };

  // Widget class
  class MongoDBChatWidget {
    constructor(config) {
      this.config = config;
      this.container = null;
      this.isOpen = false;
      this.sessionId = null;
      this.messages = [];
      this.isLoading = false;
    }

    init() {
      this.createContainer();
      this.createWidget();
      this.bindEvents();

      if (this.config.autoOpen) {
        setTimeout(() => this.openChat(), 1000);
      }

      console.log("MongoDB Chat Widget initialized successfully!");
    }

    createContainer() {
      this.container = document.createElement("div");
      this.container.id = utils.generateId();
      this.container.className = "mongodb-chat-widget-container";
      document.body.appendChild(this.container);
    }

    createWidget() {
      this.container.innerHTML = `
        <div class="mongodb-chat-window" id="chat-window">
          <div class="mongodb-chat-header">
            <div class="mongodb-chat-header-info">
              <div class="mongodb-chat-header-icon">🍃</div>
              <div>
                <div class="mongodb-chat-header-title">${this.config.title}</div>
                <div class="mongodb-chat-header-subtitle">${this.config.subtitle}</div>
              </div>
            </div>
            <button class="mongodb-chat-close" id="chat-close">✕</button>
          </div>
          <div class="mongodb-chat-messages" id="chat-messages"></div>
          <div class="mongodb-chat-input-container">
            <textarea class="mongodb-chat-input" id="chat-input" placeholder="Ask me about MongoDB..." rows="1"></textarea>
            <button class="mongodb-chat-send" id="chat-send">➤</button>
          </div>
        </div>
        <button class="mongodb-chat-toggle" id="chat-toggle">💬</button>
      `;

      // Add welcome message
      this.addMessage(
        this.config.welcomeMessage ||
          "Hello! I'm your MongoDB assistant. I can help you with MongoDB best practices, queries, indexing, performance optimization, and more. What would you like to know?",
        false
      );
    }

    bindEvents() {
      const toggle = this.container.querySelector("#chat-toggle");
      const close = this.container.querySelector("#chat-close");
      const input = this.container.querySelector("#chat-input");
      const send = this.container.querySelector("#chat-send");

      toggle.addEventListener("click", () => this.toggleChat());
      close.addEventListener("click", () => this.closeChat());
      send.addEventListener("click", () => this.sendMessage());

      input.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    toggleChat() {
      if (this.isOpen) {
        this.closeChat();
      } else {
        this.openChat();
      }
    }

    openChat() {
      const window = this.container.querySelector("#chat-window");
      const toggle = this.container.querySelector("#chat-toggle");

      window.classList.add("open");
      toggle.innerHTML = "✕";
      toggle.classList.remove("has-notification");
      this.isOpen = true;
    }

    closeChat() {
      const window = this.container.querySelector("#chat-window");
      const toggle = this.container.querySelector("#chat-toggle");

      window.classList.remove("open");
      toggle.innerHTML = "💬";
      this.isOpen = false;
    }

    addMessage(text, isUser = false) {
      const messagesContainer = this.container.querySelector("#chat-messages");
      const messageDiv = document.createElement("div");
      messageDiv.className = `mongodb-chat-message ${isUser ? "user" : "bot"}`;

      const time = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      messageDiv.innerHTML = `
        <div class="mongodb-chat-bubble ${
          isUser ? "user" : "bot"
        }">${text}</div>
        <div class="mongodb-chat-time">${time}</div>
      `;

      messagesContainer.appendChild(messageDiv);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTyping() {
      const messagesContainer = this.container.querySelector("#chat-messages");
      const typingDiv = document.createElement("div");
      typingDiv.id = "typing-indicator";
      typingDiv.className = "mongodb-chat-message bot";
      typingDiv.innerHTML = `
        <div class="mongodb-chat-typing">
          <span>Thinking</span>
          <div class="mongodb-chat-typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      `;
      messagesContainer.appendChild(typingDiv);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTyping() {
      const typing = this.container.querySelector("#typing-indicator");
      if (typing) typing.remove();
    }

    async sendMessage() {
      const input = this.container.querySelector("#chat-input");
      const message = input.value.trim();

      if (!message || this.isLoading) return;

      this.addMessage(message, true);
      input.value = "";
      this.isLoading = true;
      this.showTyping();

      try {
        const response = await fetch(`${this.config.apiUrl}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: message,
            session_id: this.sessionId,
          }),
        });

        const data = await response.json();
        this.sessionId = data.session_id;

        this.hideTyping();
        this.addMessage(data.response);

        // Show notification if chat is closed
        if (!this.isOpen) {
          const toggle = this.container.querySelector("#chat-toggle");
          toggle.classList.add("has-notification");
        }
      } catch (error) {
        console.error("Chat error:", error);
        this.hideTyping();
        this.addMessage(
          "Sorry, I'm having trouble connecting. Please try again later."
        );
      }

      this.isLoading = false;
    }
  }

  // Initialize widget
  function initWidget() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initWidget);
      return;
    }

    const config = utils.getConfig();
    utils.injectStyles(config);

    const widget = new MongoDBChatWidget(config);
    widget.init();

    // Make widget globally accessible
    window.MongoDBChatWidget = widget;
  }

  // Auto-initialize
  initWidget();
})();
