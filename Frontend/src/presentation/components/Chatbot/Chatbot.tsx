// Chatbot Component
import { useState, useRef, useEffect } from 'react';
import { useChatbot } from '@presentation/hooks/useChatbot';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRobot, FaTimes, FaPaperPlane } from 'react-icons/fa';
import './Chatbot.css';

interface ChatbotProps {
  userId: string;
}

export const Chatbot: React.FC<ChatbotProps> = ({ userId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const { messages, sendMessage, isLoading } = useChatbot(userId);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (inputMessage.trim() && !isLoading) {
      sendMessage(inputMessage);
      setInputMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Quick actions buttons
  const quickActions = [
    'ver productos',
    'ver carrito',
    'mis órdenes',
    'ayuda',
  ];

  return (
    <>
      {/* Chatbot Toggle Button */}
      <motion.button
        className="chatbot-toggle"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        {isOpen ? <FaTimes size={24} /> : <FaRobot size={24} />}
      </motion.button>

      {/* Chatbot Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="chatbot-window"
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            {/* Header */}
            <div className="chatbot-header">
              <div className="chatbot-header-content">
                <FaRobot size={24} />
                <div>
                  <h3>Asistente Virtual</h3>
                  <span className="chatbot-status">● En línea</span>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="chatbot-messages">
              {messages.length === 0 && (
                <div className="chatbot-welcome">
                  <FaRobot size={48} />
                  <p>¡Hola! Soy tu asistente virtual 🤖</p>
                  <p>¿En qué puedo ayudarte hoy?</p>
                </div>
              )}

              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  className={`chatbot-message ${
                    message.isUser ? 'user-message' : 'bot-message'
                  }`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="message-content">
                    <p className="message-text">{message.message}</p>
                    <span className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString('es-ES', {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>
                </motion.div>
              ))}

              {isLoading && (
                <div className="chatbot-message bot-message">
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Actions */}
            {messages.length === 0 && (
              <div className="chatbot-quick-actions">
                {quickActions.map((action) => (
                  <button
                    key={action}
                    className="quick-action-btn"
                    onClick={() => {
                      sendMessage(action);
                    }}
                  >
                    {action}
                  </button>
                ))}
              </div>
            )}

            {/* Input */}
            <div className="chatbot-input">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu mensaje..."
                rows={1}
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={!inputMessage.trim() || isLoading}
                className="send-btn"
              >
                <FaPaperPlane />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
