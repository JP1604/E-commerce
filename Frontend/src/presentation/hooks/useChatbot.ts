// Custom Hook - useChatbot
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { container } from '@infrastructure/di/container';
import { ChatMessage } from '@domain/entities/Chat';

export const useChatbot = (userId: string) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const sendMessageMutation = useMutation({
    mutationFn: (message: string) => container.sendChatMessageUseCase.execute(userId, message),
    onMutate: (message) => {
      // Add user message immediately
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        user_id: userId,
        message,
        timestamp: new Date(),
        isUser: true,
      };
      setMessages((prev) => [...prev, userMessage]);
    },
    onSuccess: (response) => {
      // Add bot response
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        user_id: 'bot',
        message: response.response,
        timestamp: new Date(),
        isUser: false,
      };
      setMessages((prev) => [...prev, botMessage]);
    },
    onError: (error) => {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        user_id: 'bot',
        message: 'Lo siento, hubo un error. Por favor intenta de nuevo.',
        timestamp: new Date(),
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    },
  });

  return {
    messages,
    sendMessage: sendMessageMutation.mutate,
    isLoading: sendMessageMutation.isPending,
    clearMessages: () => setMessages([]),
  };
};
