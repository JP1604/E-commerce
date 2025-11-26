import React, { useState, useRef, useEffect } from 'react';
import { Button } from '../ui/Button';

const N8N_WEBHOOK_URL = 'http://localhost:30678/webhook-test/chat';

export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: '¡Hola! 👋 Soy Nova, tu asistente virtual. ¿En qué puedo ayudarte hoy?',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const quickReplies = [
    { id: 1, text: '¿Qué productos tienen?', icon: '📦' },
    { id: 2, text: '¿Cómo realizo un pedido?', icon: '🛒' },
    { id: 3, text: '¿Cuál es el tiempo de entrega?', icon: '🚚' },
    { id: 4, text: 'Métodos de pago', icon: '💳' },
  ];

  const getBotResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('producto') || lowerMessage.includes('catálogo') || lowerMessage.includes('venden')) {
      return '¡Tenemos una amplia variedad de productos! 🎉 Encuentra desde tecnología hasta accesorios. Puedes explorar nuestro catálogo completo en esta página o usar el buscador para encontrar algo específico. ¿Buscas algo en particular?';
    }
    
    if (lowerMessage.includes('pedido') || lowerMessage.includes('comprar') || lowerMessage.includes('orden')) {
      return '¡Realizar un pedido es muy fácil! 🛍️\n\n1. Explora nuestros productos\n2. Haz clic en "Agregar al carrito" en los que te gusten\n3. Ve al carrito (ícono en la esquina superior)\n4. Haz clic en "Realizar Pedido"\n5. Completa la información de entrega\n6. ¡Listo! Recibirás una confirmación\n\n¿Necesitas ayuda con algún paso?';
    }
    
    if (lowerMessage.includes('entrega') || lowerMessage.includes('envío') || lowerMessage.includes('llega')) {
      return '¡Nuestros envíos son súper rápidos! 🚀\n\nEl tiempo de entrega depende de tu ubicación:\n• Ciudad: 1-2 días hábiles\n• Nacional: 3-5 días hábiles\n\n¡Todos nuestros envíos incluyen seguimiento en tiempo real! 📍';
    }
    
    if (lowerMessage.includes('pago') || lowerMessage.includes('pagar') || lowerMessage.includes('tarjeta')) {
      return '¡Aceptamos varios métodos de pago! 💳\n\n• Tarjetas de crédito/débito\n• Transferencias bancarias\n• Pago contra entrega (efectivo)\n\nTodas las transacciones son 100% seguras 🔒';
    }
    
    if (lowerMessage.includes('precio') || lowerMessage.includes('costo') || lowerMessage.includes('cuánto')) {
      return 'Los precios varían según el producto. 💰\n\nPuedes ver el precio de cada artículo en su tarjeta en el catálogo. ¡Tenemos productos para todos los presupuestos!\n\n¿Te interesa algún producto en específico?';
    }
    
    if (lowerMessage.includes('ayuda') || lowerMessage.includes('soporte') || lowerMessage.includes('contacto')) {
      return '¡Estoy aquí para ayudarte! 🤗\n\nPuedes preguntarme sobre:\n• Productos y catálogo\n• Cómo realizar pedidos\n• Métodos de pago\n• Tiempos de entrega\n• Estado de tu pedido\n\n¿Qué necesitas saber?';
    }
    
    if (lowerMessage.includes('gracias') || lowerMessage.includes('genial') || lowerMessage.includes('perfecto')) {
      return '¡De nada! 😊 Estoy aquí para ayudarte cuando lo necesites. ¡Felices compras! ✨';
    }
    
    if (lowerMessage.includes('hola') || lowerMessage.includes('hey') || lowerMessage.includes('buenas')) {
      return '¡Hola! 👋 Bienvenido a NovaMarket. ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre productos, pedidos, envíos o cualquier otra cosa. 😊';
    }
    
    // Respuesta por defecto
    return '🤔 Interesante pregunta. Aunque no tengo una respuesta específica, puedo ayudarte con:\n\n• Información sobre productos\n• Proceso de compra\n• Métodos de pago\n• Tiempos de entrega\n\n¿Sobre cuál de estos temas te gustaría saber más?';
  };

  const sendMessageToN8N = async (message) => {
    try {
      const response = await fetch(N8N_WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Error al conectar con el servidor');
      }

      const data = await response.json();
      
      // El formato de respuesta puede variar según tu flujo de n8n
      // Ajusta esto según la estructura de respuesta de tu webhook
      if (data.output || data.response || data.message) {
        return data.output || data.response || data.message;
      }
      
      // Si la respuesta es un array de productos, formatearla
      if (Array.isArray(data)) {
        let productList = '📦 **Lista de Productos:**\n\n';
        data.forEach((product, index) => {
          productList += `${index + 1}. **${product.name || product.title}**\n`;
          if (product.price) productList += `   💰 Precio: $${product.price}\n`;
          if (product.description) productList += `   📝 ${product.description}\n`;
          productList += '\n';
        });
        return productList;
      }

      // Si es un objeto, intentar extraer el texto
      return JSON.stringify(data, null, 2);
    } catch (error) {
      console.error('Error al comunicarse con n8n:', error);
      // Fallback a respuestas locales si n8n no está disponible
      return null;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputValue;
    setInputValue('');
    setIsTyping(true);

    // Intentar obtener respuesta de n8n primero
    const n8nResponse = await sendMessageToN8N(messageToSend);
    
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        type: 'bot',
        text: n8nResponse || getBotResponse(messageToSend),
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, n8nResponse ? 300 : 800);
  };

  const handleQuickReply = async (reply) => {
    const messageText = reply.text;
    
    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: messageText,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Intentar obtener respuesta de n8n primero
    const n8nResponse = await sendMessageToN8N(messageText);
    
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        type: 'bot',
        text: n8nResponse || getBotResponse(messageText),
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, n8nResponse ? 300 : 800);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 group"
          aria-label="Abrir chat"
        >
          <div className="relative">
            {/* Glow effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full blur-xl opacity-60 group-hover:opacity-100 transition-opacity animate-pulse"></div>
            
            {/* Button */}
            <div className="relative bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-full p-4 shadow-2xl hover:shadow-primary-500/50 transition-all duration-300 group-hover:scale-110">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              
              {/* Notification badge */}
              <div className="absolute -top-1 -right-1 w-6 h-6 bg-accent-500 rounded-full flex items-center justify-center text-xs font-bold animate-bounce">
                1
              </div>
            </div>
          </div>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[380px] sm:w-[420px] h-[600px] flex flex-col bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden animate-slideUp">
          {/* Header */}
          <div className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center text-2xl">
                  🤖
                </div>
                <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h3 className="font-bold text-lg">Nova Assistant</h3>
                <p className="text-xs text-white/80">Siempre disponible para ti</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/80 hover:text-white hover:bg-white/10 rounded-lg p-2 transition-colors"
              aria-label="Cerrar chat"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
              >
                <div className={`flex items-end gap-2 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  {message.type === 'bot' && (
                    <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">
                      🤖
                    </div>
                  )}
                  <div
                    className={`rounded-2xl px-4 py-3 shadow-sm ${
                      message.type === 'user'
                        ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-br-md'
                        : 'bg-white border border-gray-200 text-gray-800 rounded-bl-md'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-line">{message.text}</p>
                    <p className={`text-xs mt-1 ${message.type === 'user' ? 'text-white/70' : 'text-gray-400'}`}>
                      {message.timestamp.toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start animate-fadeIn">
                <div className="flex items-end gap-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-sm">
                    🤖
                  </div>
                  <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Replies */}
          {messages.length === 1 && (
            <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
              <p className="text-xs text-gray-500 mb-2 font-medium">Preguntas frecuentes:</p>
              <div className="flex flex-wrap gap-2">
                {quickReplies.map((reply) => (
                  <button
                    key={reply.id}
                    onClick={() => handleQuickReply(reply)}
                    className="text-xs bg-white border border-gray-200 hover:border-primary-500 hover:bg-primary-50 text-gray-700 hover:text-primary-700 px-3 py-2 rounded-full transition-all duration-200 flex items-center gap-1"
                  >
                    <span>{reply.icon}</span>
                    <span>{reply.text}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="p-4 bg-white border-t border-gray-200">
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu mensaje..."
                className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim()}
                className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white p-3 rounded-xl hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:scale-105 active:scale-95"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-2 text-center">Presiona Enter para enviar</p>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes slideUp {
          from {
            transform: translateY(100px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-slideUp {
          animation: slideUp 0.3s ease-out;
        }

        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
    </>
  );
};
