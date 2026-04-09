import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import { FaComments, FaTimes, FaPaperPlane } from "react-icons/fa";
import { FaRobot } from "react-icons/fa";
import axios from "axios";

// Styled Components
const ChatContainer = styled.div`
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
    sans-serif;
`;

const ChatToggle = styled.button`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #cf0404, #a00303);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(207, 4, 4, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 25px rgba(207, 4, 4, 0.4);
  }

  &:active {
    transform: scale(0.95);
  }
`;

const ChatWindow = styled.div`
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: ${(props) =>
    props.isOpen ? "translateY(0) scale(1)" : "translateY(20px) scale(0.95)"};
  opacity: ${(props) => (props.isOpen ? 1 : 0)};
  visibility: ${(props) => (props.isOpen ? "visible" : "hidden")};
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  @media (max-width: 480px) {
    width: calc(100vw - 40px);
    height: calc(100vh - 120px);
    bottom: 80px;
    right: 20px;
  }
`;

const ChatHeader = styled.div`
  background: linear-gradient(135deg, #cf0404, #a00303);
  color: white;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const HeaderInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

const HeaderTitle = styled.div`
  font-weight: 600;
  font-size: 16px;
`;

const HeaderSubtitle = styled.div`
  font-size: 12px;
  opacity: 0.9;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f8f9fa;
`;

const Message = styled.div`
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  align-items: ${(props) => (props.isUser ? "flex-end" : "flex-start")};
`;

const MessageBubble = styled.div`
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  background: ${(props) =>
    props.isUser ? "linear-gradient(135deg, #cf0404, #a00303)" : "white"};
  color: ${(props) => (props.isUser ? "white" : "#333")};
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  line-height: 1.4;
  white-space: pre-wrap;
  word-wrap: break-word;
  text-align: left;
`;

const MessageTime = styled.div`
  font-size: 11px;
  color: #666;
  margin-top: 4px;
  opacity: 0.7;
`;

const InputContainer = styled.div`
  padding: 16px;
  background: white;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 12px;
  align-items: flex-end;
`;

const MessageInput = styled.textarea`
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
  transition: border-color 0.2s;

  &:focus {
    border-color: #cf0404;
  }

  &::placeholder {
    color: #999;
  }
`;

const SendButton = styled.button`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #cf0404, #a00303);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;

  &:hover:not(:disabled) {
    transform: scale(1.05);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  color: #666;
  font-size: 14px;
  font-style: italic;
`;

const TypingDots = styled.div`
  display: flex;
  gap: 4px;

  span {
    width: 6px;
    height: 6px;
    background: #cf0404;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;

    &:nth-child(1) {
      animation-delay: -0.32s;
    }
    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }

  @keyframes typing {
    0%,
    80%,
    100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }
`;

const WelcomeMessage = styled.div`
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
`;

// Main ChatBubble Component
const ChatBubble = ({ apiUrl = "http://localhost:8000" }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      // Add welcome message when chat opens for the first time
      setMessages([
        {
          id: 1,
          text: "Hi!! How can I help you today?",
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    }
  }, [isOpen, messages.length]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue.trim(),
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await axios.post(`${apiUrl}/chat`, {
        message: userMessage.text,
        session_id: sessionId,
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, botMessage]);
      setSessionId(response.data.session_id);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting to the server. Please make sure the API is running and try again.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <ChatContainer>
      <ChatWindow isOpen={isOpen}>
        <ChatHeader>
          <HeaderInfo>
            <FaRobot size={24} />
            <div>
              <HeaderTitle>Qunix Smart Support</HeaderTitle>
            </div>
          </HeaderInfo>
          <CloseButton onClick={toggleChat}>
            <FaTimes />
          </CloseButton>
        </ChatHeader>

        <MessagesContainer>
          {messages.map((message) => (
            <Message key={message.id} isUser={message.isUser}>
              <MessageBubble isUser={message.isUser}>
                {message.text}
              </MessageBubble>
              <MessageTime>{message.timestamp}</MessageTime>
            </Message>
          ))}

          {isLoading && (
            <Message isUser={false}>
              <MessageBubble isUser={false}>
                <TypingIndicator>
                  Thinking
                  <TypingDots>
                    <span></span>
                    <span></span>
                    <span></span>
                  </TypingDots>
                </TypingIndicator>
              </MessageBubble>
            </Message>
          )}

          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputContainer>
          <MessageInput
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about TechnoNJR..."
            disabled={isLoading}
            rows={1}
          />
          <SendButton
            onClick={sendMessage}
            disabled={isLoading || !inputValue.trim()}
          >
            <FaPaperPlane />
          </SendButton>
        </InputContainer>
      </ChatWindow>

      <ChatToggle onClick={toggleChat}>
        {isOpen ? <FaTimes /> : <FaComments />}
      </ChatToggle>
    </ChatContainer>
  );
};

export default ChatBubble;
