/**
 * MongoDB Chat Widget - Embeddable Script
 * Add this script to any website to embed the MongoDB chat widget
 */

(function () {
  "use strict";

  // Configuration
  const WIDGET_CONFIG = {
    apiUrl: "http://localhost:8000",
    widgetUrl: "http://localhost:3000",
    version: "1.0.0",
  };

  // Get script tag attributes for configuration
  function getScriptConfig() {
    const scripts = document.querySelectorAll(
      'script[src*="embed.js"], script[data-mongodb-chat]'
    );
    const script = scripts[scripts.length - 1]; // Get the current script

    return {
      apiUrl: script.getAttribute("data-api-url") || WIDGET_CONFIG.apiUrl,
      theme: script.getAttribute("data-theme") || "default",
      position: script.getAttribute("data-position") || "bottom-right",
      primaryColor: script.getAttribute("data-primary-color") || "#00A86B",
      title: script.getAttribute("data-title") || "MongoDB Assistant",
      subtitle:
        script.getAttribute("data-subtitle") || "Ask me anything about MongoDB",
    };
  }

  // Create widget container
  function createWidgetContainer(config) {
    const container = document.createElement("div");
    container.id = "mongodb-chat-widget-" + Date.now();
    container.style.cssText = `
      position: fixed;
      z-index: 999999;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
      ${getPositionStyles(config.position)}
    `;

    document.body.appendChild(container);
    return container;
  }

  // Get position styles based on configuration
  function getPositionStyles(position) {
    const positions = {
      "bottom-right": "bottom: 20px; right: 20px;",
      "bottom-left": "bottom: 20px; left: 20px;",
      "top-right": "top: 20px; right: 20px;",
      "top-left": "top: 20px; left: 20px;",
    };
    return positions[position] || positions["bottom-right"];
  }

  // Create the chat widget HTML
  function createChatWidget(config) {
    return `
      <div id="chat-widget" style="position: relative;">
        <!-- Chat Toggle Button -->
        <button id="chat-toggle" style="
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background: linear-gradient(135deg, #00684A, ${config.primaryColor});
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          box-shadow: 0 4px 20px rgba(0, 104, 74, 0.3);
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          💬
        </button>

        <!-- Chat Window -->
        <div id="chat-window" style="
          position: absolute;
          bottom: 80px;
          right: 0;
          width: 350px;
          height: 500px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
          display: none;
          flex-direction: column;
          overflow: hidden;
          transform: translateY(20px) scale(0.95);
          opacity: 0;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        ">
          <!-- Header -->
          <div style="
            background: linear-gradient(135deg, #00684A, ${
              config.primaryColor
            });
            color: white;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
          ">
            <div style="display: flex; align-items: center; gap: 12px;">
              <div style="font-size: 24px;">🍃</div>
              <div>
                <div style="font-weight: 600; font-size: 16px;">${
                  config.title
                }</div>
                <div style="font-size: 12px; opacity: 0.9;">${
                  config.subtitle
                }</div>
              </div>
            </div>
            <button id="chat-close" style="
              background: none;
              border: none;
              color: white;
              font-size: 18px;
              cursor: pointer;
              padding: 4px;
              border-radius: 4px;
            ">✕</button>
          </div>

          <!-- Messages -->
          <div id="chat-messages" style="
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: #f8f9fa;
          ">
            <div class="message bot-message" style="
              margin-bottom: 16px;
              display: flex;
              flex-direction: column;
              align-items: flex-start;
            ">
              <div style="
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 18px;
                background: white;
                color: #333;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                font-size: 14px;
                line-height: 1.4;
              ">
                Hello! I'm your MongoDB assistant. I can help you with MongoDB best practices, queries, indexing, performance optimization, and more. What would you like to know?
              </div>
              <div style="font-size: 11px; color: #666; margin-top: 4px; opacity: 0.7;">
                ${new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </div>
            </div>
          </div>

          <!-- Input -->
          <div style="
            padding: 16px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 12px;
            align-items: flex-end;
          ">
            <textarea id="chat-input" placeholder="Ask me about MongoDB..." style="
              flex: 1;
              border: 1px solid #ddd;
              border-radius: 20px;
              padding: 12px 16px;
              font-size: 14px;
              resize: none;
              max-height: 100px;
              min-height: 40px;
              font-family: inherit;
              outline: none;
            "></textarea>
            <button id="chat-send" style="
              width: 40px;
              height: 40px;
              border-radius: 50%;
              background: linear-gradient(135deg, #00684A, ${
                config.primaryColor
              });
              border: none;
              color: white;
              cursor: pointer;
              display: flex;
              align-items: center;
              justify-content: center;
              flex-shrink: 0;
            ">➤</button>
          </div>
        </div>
      </div>
    `;
  }

  // Chat functionality
  function initializeChatFunctionality(container, config) {
    const toggle = container.querySelector("#chat-toggle");
    const window = container.querySelector("#chat-window");
    const close = container.querySelector("#chat-close");
    const input = container.querySelector("#chat-input");
    const send = container.querySelector("#chat-send");
    const messages = container.querySelector("#chat-messages");

    let isOpen = false;
    let sessionId = null;

    // Toggle chat window
    function toggleChat() {
      isOpen = !isOpen;
      if (isOpen) {
        window.style.display = "flex";
        setTimeout(() => {
          window.style.transform = "translateY(0) scale(1)";
          window.style.opacity = "1";
        }, 10);
        toggle.innerHTML = "✕";
      } else {
        window.style.transform = "translateY(20px) scale(0.95)";
        window.style.opacity = "0";
        setTimeout(() => {
          window.style.display = "none";
        }, 300);
        toggle.innerHTML = "💬";
      }
    }

    // Add message to chat
    function addMessage(text, isUser = false) {
      const messageDiv = document.createElement("div");
      messageDiv.className = `message ${
        isUser ? "user-message" : "bot-message"
      }`;
      messageDiv.style.cssText = `
        margin-bottom: 16px;
        display: flex;
        flex-direction: column;
        align-items: ${isUser ? "flex-end" : "flex-start"};
      `;

      const bubble = document.createElement("div");
      bubble.style.cssText = `
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 18px;
        background: ${
          isUser ? `linear-gradient(135deg, #007bff, #0056b3)` : "white"
        };
        color: ${isUser ? "white" : "#333"};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        font-size: 14px;
        line-height: 1.4;
        white-space: pre-wrap;
        word-wrap: break-word;
      `;
      bubble.textContent = text;

      const time = document.createElement("div");
      time.style.cssText = `
        font-size: 11px;
        color: #666;
        margin-top: 4px;
        opacity: 0.7;
      `;
      time.textContent = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      messageDiv.appendChild(bubble);
      messageDiv.appendChild(time);
      messages.appendChild(messageDiv);
      messages.scrollTop = messages.scrollHeight;
    }

    // Send message to API
    async function sendMessage() {
      const message = input.value.trim();
      if (!message) return;

      addMessage(message, true);
      input.value = "";

      // Add typing indicator
      const typingDiv = document.createElement("div");
      typingDiv.id = "typing-indicator";
      typingDiv.style.cssText = `
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        color: #666;
        font-size: 14px;
        font-style: italic;
      `;
      typingDiv.innerHTML =
        'Thinking<span style="animation: blink 1s infinite;">...</span>';
      messages.appendChild(typingDiv);
      messages.scrollTop = messages.scrollHeight;

      try {
        const response = await fetch(`${config.apiUrl}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: message,
            session_id: sessionId,
          }),
        });

        const data = await response.json();
        sessionId = data.session_id;

        // Remove typing indicator
        typingDiv.remove();

        // Add bot response
        addMessage(data.response);
      } catch (error) {
        console.error("Chat error:", error);
        typingDiv.remove();
        addMessage(
          "Sorry, I'm having trouble connecting. Please try again later."
        );
      }
    }

    // Event listeners
    toggle.addEventListener("click", toggleChat);
    close.addEventListener("click", toggleChat);
    send.addEventListener("click", sendMessage);

    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // Hover effects
    toggle.addEventListener("mouseenter", () => {
      toggle.style.transform = "scale(1.1)";
    });

    toggle.addEventListener("mouseleave", () => {
      toggle.style.transform = "scale(1)";
    });
  }

  // Initialize the widget
  function initWidget() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initWidget);
      return;
    }

    const config = getScriptConfig();
    const container = createWidgetContainer(config);
    container.innerHTML = createChatWidget(config);
    initializeChatFunctionality(container, config);

    console.log("MongoDB Chat Widget initialized successfully!");
  }

  // Auto-initialize
  initWidget();
})();
