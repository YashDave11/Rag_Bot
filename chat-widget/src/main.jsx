import React from "react";
import ReactDOM from "react-dom/client";
import ChatWidget from "./ChatWidget";

// Development mode - render directly
const root = ReactDOM.createRoot(
  document.getElementById("mongodb-chat-widget")
);
root.render(
  <ChatWidget
    apiUrl="http://localhost:8000"
    position="bottom-right"
    primaryColor="#007bff"
    title="Qunix Smart Support"
  />
);
