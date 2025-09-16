import React from "react";
import ReactDOM from "react-dom/client";
import ChatWidget from "./ChatWidget";

// Widget initialization function
window.MongoDBChatWidget = {
  init: function (config = {}) {
    const {
      containerId = "mongodb-chat-widget",
      apiUrl = "http://localhost:8000",
      position = "bottom-right",
      primaryColor = "#007bff",
      title = "MongoDB Assistant",
      welcomeMessage = "Hello! I'm your MongoDB assistant. Ask me anything about MongoDB!",
    } = config;

    // Create container if it doesn't exist
    let container = document.getElementById(containerId);
    if (!container) {
      container = document.createElement("div");
      container.id = containerId;
      document.body.appendChild(container);
    }

    // Render the widget
    const root = ReactDOM.createRoot(container);
    root.render(
      <ChatWidget
        apiUrl={apiUrl}
        position={position}
        primaryColor={primaryColor}
        title={title}
        welcomeMessage={welcomeMessage}
      />
    );

    return {
      destroy: () => {
        root.unmount();
        if (container.parentNode) {
          container.parentNode.removeChild(container);
        }
      },
    };
  },
};

// Auto-initialize if script has data attributes
document.addEventListener("DOMContentLoaded", function () {
  const scripts = document.querySelectorAll(
    'script[src*="mongodb-chat-widget"]'
  );

  scripts.forEach((script) => {
    const config = {
      apiUrl: script.getAttribute("data-api-url") || "http://localhost:8000",
      position: script.getAttribute("data-position") || "bottom-right",
      primaryColor: script.getAttribute("data-primary-color") || "#007bff",
      title: script.getAttribute("data-title") || "MongoDB Assistant",
      welcomeMessage:
        script.getAttribute("data-welcome-message") ||
        "Hello! I'm your MongoDB assistant. Ask me anything about MongoDB!",
    };

    window.MongoDBChatWidget.init(config);
  });
});
