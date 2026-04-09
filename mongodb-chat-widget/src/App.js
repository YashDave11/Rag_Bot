import React from "react";
import ChatBubble from "./components/ChatBubble";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🍃 MongoDB RAG Chat Widget Demo</h1>
        <p>This is a demo page showing the MongoDB chat widget in action.</p>
        <div className="demo-content">
          <h2>About This Widget</h2>
          <ul>
            <li>🤖 AI-powered Qunix Smart Support assistant</li>
            <li>💬 Real-time chat interface</li>
            <li>📱 Responsive design</li>
            <li>🔌 Easy website integration</li>
            <li>🎨 Customizable appearance</li>
          </ul>

          <h2>Try It Out!</h2>
          <p>
            Click the chat bubble in the bottom-right corner to start chatting
            with Qunix Smart Support.
          </p>

          <div className="example-questions">
            <h3>Example Questions:</h3>
            <ul>
              <li>"What are MongoDB best practices?"</li>
              <li>"How do I create an index?"</li>
              <li>"What is aggregation in MongoDB?"</li>
              <li>"How do I optimize MongoDB performance?"</li>
            </ul>
          </div>
        </div>
      </header>

      {/* The Chat Bubble Widget */}
      <ChatBubble apiUrl="http://localhost:8000" />
    </div>
  );
}

export default App;
