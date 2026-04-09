import React, { useState, useRef, useEffect } from "react";
import styled, { keyframes, createGlobalStyle } from "styled-components";
import {
  FaComments,
  FaTimes,
  FaPaperPlane,
  FaRobot,
  FaUser,
} from "react-icons/fa";
import { FaRobot } from "react-icons/fa";
import { BiMinimize } from "react-icons/bi";
import axios from "axios";

// Global styles to prevent conflicts
const GlobalStyle = createGlobalStyle`
  .mongodb-chat-widget * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
`;

// Animations
const slideUp = keyframes`
  from {
    transform: translateY(100%) scale(0.8);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const typing = keyframes`
  0%, 80%, 100% { 
    transform: scale(0.8); 
    opacity: 0.5; 
  }
  40% { 
    transform: scale(1); 
    opacity: 1; 
  }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// Styled Components
const ChatContainer = styled.div`
  position: fixed;
  z-index: 999999;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Cantarell", sans-serif;

  ${(props) => {
    const positions = {
      "bottom-right": "bottom: 20px; right: 20px;",
      "bottom-left": "bottom: 20px; left: 20px;",
      "top-right": "top: 20px; right: 20px;",
      "top-left": "top: 20px; left: 20px;",
    };
    return positions[props.position] || positions["bottom-right"];
  }}

  @media (max-width: 768px) {
    bottom: 10px;
    right: 10px;
    left: 10px;
  }
`;

const ChatToggle = styled.button`
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: ${(props) =>
    `linear-gradient(135deg, ${props.primaryColor}dd, ${props.primaryColor})`};
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

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
  }

  &:active {
    transform: scale(0.95);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      transparent,
      rgba(255, 255, 255, 0.1),
      transparent
    );
    transform: translateX(-100%);
    transition: transform 0.6s;
  }

  &:hover::before {
    transform: translateX(100%);
  }

  ${(props) =>
    props.hasNotification &&
    `
    animation: ${pulse} 2s infinite;
    
    &::after {
      content: '';
      position: absolute;
      top: -2px;
      right: -2px;
      width: 12px;
      height: 12px;
      background: #ff4757;
      border-radius: 50%;
      border: 2px solid white;
    }
  `}
`;

const ChatWindow = styled.div`
  position: absolute;
  ${(props) =>
    props.position?.includes("top") ? "top: 80px;" : "bottom: 80px;"}
  ${(props) => (props.position?.includes("left") ? "left: 0;" : "right: 0;")}
  width: 380px;
  height: 600px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  display: ${(props) => (props.isOpen ? "flex" : "none")};
  flex-direction: column;
  overflow: hidden;
  animation: ${(props) => (props.isOpen ? slideUp : "none")} 0.4s
    cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.05);

  @media (max-width: 768px) {
    width: calc(100vw - 20px);
    height: calc(100vh - 120px);
    ${(props) =>
      props.position?.includes("top") ? "top: 80px;" : "bottom: 80px;"}
    left: 0;
    right: 0;
    margin: 0 auto;
  }
`;

const ChatHeader = styled.div`
  background: ${(props) =>
    `linear-gradient(135deg, ${props.primaryColor}, ${props.primaryColor}dd)`};
  color: white;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.1;
  }
`;

const HeaderInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
`;

const HeaderIcon = styled.div`
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
`;

const HeaderText = styled.div``;

const HeaderTitle = styled.div`
  font-weight: 600;
  font-size: 18px;
  margin-bottom: 2px;
`;

const HeaderSubtitle = styled.div`
  font-size: 13px;
  opacity: 0.9;
`;

const HeaderActions = styled.div`
  display: flex;
  gap: 8px;
  position: relative;
  z-index: 1;
`;

const HeaderButton = styled.button`
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
  font-size: 14px;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(to bottom, #f8f9fa, #ffffff);

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }
`;

const Message = styled.div`
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: ${(props) => (props.isUser ? "flex-end" : "flex-start")};
  animation: ${fadeIn} 0.3s ease-out;
`;

const MessageHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 12px;
  color: #666;
`;

const MessageAvatar = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: ${(props) => (props.isUser ? "#007bff" : props.primaryColor)};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
`;

const MessageBubble = styled.div`
  max-width: 85%;
  padding: 14px 18px;
  border-radius: ${(props) =>
    props.isUser ? "20px 20px 4px 20px" : "20px 20px 20px 4px"};
  background: ${(props) =>
    props.isUser ? "linear-gradient(135deg, #cf0404, #a00303)" : "white"};
  color: ${(props) => (props.isUser ? "white" : "#333")};
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  text-align: left;
  position: relative;
  border: ${(props) =>
    props.isUser ? "none" : "1px solid rgba(0, 0, 0, 0.05)"};

  &::before {
    content: "";
    position: absolute;
    ${(props) =>
      props.isUser ? "right: -8px; bottom: 4px;" : "left: -8px; bottom: 4px;"}
    width: 0;
    height: 0;
    border: 8px solid transparent;
    ${(props) =>
      props.isUser
        ? "border-left-color: #0056b3; border-right: none;"
        : "border-right-color: white; border-left: none;"}
  }
`;

const MessageTime = styled.div`
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  ${(props) => (props.isUser ? "text-align: right;" : "text-align: left;")}
`;

const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 18px;
  background: white;
  border-radius: 20px 20px 20px 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.05);
  max-width: 85%;
`;

const TypingDots = styled.div`
  display: flex;
  gap: 4px;

  span {
    width: 8px;
    height: 8px;
    background: ${(props) => props.primaryColor};
    border-radius: 50%;
    animation: ${typing} 1.4s infinite ease-in-out;

    &:nth-child(1) {
      animation-delay: -0.32s;
    }
    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
`;

const InputContainer = styled.div`
  padding: 20px;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 12px;
  align-items: flex-end;
`;

const MessageInput = styled.textarea`
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

  &:focus {
    border-color: ${(props) => props.primaryColor};
    background: white;
    box-shadow: 0 0 0 3px ${(props) => props.primaryColor}20;
  }

  &::placeholder {
    color: #999;
  }
`;

const SendButton = styled.button`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: ${(props) =>
    props.disabled
      ? "#e9ecef"
      : `linear-gradient(135deg, ${props.primaryColor}, ${props.primaryColor}dd)`};
  border: none;
  color: white;
  cursor: ${(props) => (props.disabled ? "not-allowed" : "pointer")};
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
  font-size: 16px;

  &:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 12px ${(props) => props.primaryColor}40;
  }

  &:active:not(:disabled) {
    transform: scale(0.95);
  }
`;

const PoweredBy = styled.div`
  padding: 8px 20px;
  background: #f8f9fa;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  text-align: center;
  font-size: 11px;
  color: #666;

  a {
    color: ${(props) => props.primaryColor};
    text-decoration: none;
    font-weight: 500;

    &:hover {
      text-decoration: underline;
    }
  }
`;

// Main Component
const ProfessionalChatBubble = ({
  apiUrl = "http://localhost:8000",
  primaryColor = "#cf0404",
  title = "Qunix Smart Support",
  subtitle = "Hi!! How can I help you today?",
  position = "bottom-right",
  showPoweredBy = true,
  welcomeMessage = "Hi!! How can I help you today?",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [hasNotification, setHasNotification] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          id: 1,
          text: welcomeMessage,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    }
  }, [isOpen, messages.length, welcomeMessage]);

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

      // Show notification if chat is closed
      if (!isOpen) {
        setHasNotification(true);
      }
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
    setHasNotification(false);
  };

  const minimizeChat = () => {
    setIsMinimized(!isMinimized);
  };

  return (
    <>
      <GlobalStyle />
      <ChatContainer className="mongodb-chat-widget" position={position}>
        <ChatWindow isOpen={isOpen && !isMinimized} position={position}>
          <ChatHeader primaryColor={primaryColor}>
            <HeaderInfo>
              <HeaderIcon>
                <SiMongodb />
              </HeaderIcon>
              <HeaderText>
                <HeaderTitle>{title}</HeaderTitle>
              </HeaderText>
            </HeaderInfo>
            <HeaderActions>
              <HeaderButton onClick={minimizeChat} title="Minimize">
                <BiMinimize />
              </HeaderButton>
              <HeaderButton onClick={toggleChat} title="Close">
                <FaTimes />
              </HeaderButton>
            </HeaderActions>
          </ChatHeader>

          <MessagesContainer>
            {messages.map((message) => (
              <Message key={message.id} isUser={message.isUser}>
                <MessageHeader>
                  <MessageAvatar
                    isUser={message.isUser}
                    primaryColor={primaryColor}
                  >
                    {message.isUser ? <FaUser /> : <FaRobot />}
                  </MessageAvatar>
                  <span>{message.isUser ? "You" : "Assistant"}</span>
                </MessageHeader>
                <MessageBubble isUser={message.isUser}>
                  {message.text}
                </MessageBubble>
                <MessageTime isUser={message.isUser}>
                  {message.timestamp}
                </MessageTime>
              </Message>
            ))}

            {isLoading && (
              <Message isUser={false}>
                <MessageHeader>
                  <MessageAvatar primaryColor={primaryColor}>
                    <FaRobot />
                  </MessageAvatar>
                  <span>Assistant</span>
                </MessageHeader>
                <TypingIndicator primaryColor={primaryColor}>
                  <span>Thinking</span>
                  <TypingDots primaryColor={primaryColor}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </TypingDots>
                </TypingIndicator>
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
              primaryColor={primaryColor}
              rows={1}
            />
            <SendButton
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              primaryColor={primaryColor}
            >
              <FaPaperPlane />
            </SendButton>
          </InputContainer>

          {showPoweredBy && (
            <PoweredBy primaryColor={primaryColor}>
              Powered by{" "}
              <a href="#" target="_blank">
                MongoDB RAG Assistant
              </a>
            </PoweredBy>
          )}
        </ChatWindow>

        <ChatToggle
          onClick={toggleChat}
          primaryColor={primaryColor}
          hasNotification={hasNotification}
          title={isOpen ? "Close chat" : "Open chat"}
        >
          {isOpen ? <FaTimes /> : <FaComments />}
        </ChatToggle>
      </ChatContainer>
    </>
  );
};

export default ProfessionalChatBubble;
