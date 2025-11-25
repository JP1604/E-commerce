// Chatbot Repository Implementation (n8n integration)
import { ChatbotResponse } from '@domain/entities/Chat';
import { IChatbotRepository } from '@domain/repositories/IChatbotRepository';
import axios from 'axios';

const N8N_WEBHOOK_URL = import.meta.env.VITE_N8N_WEBHOOK_URL || 'http://localhost:5678/webhook/chatbot';

export class ChatbotRepository implements IChatbotRepository {
  async sendMessage(userId: string, message: string): Promise<ChatbotResponse> {
    try {
      const response = await axios.post<ChatbotResponse>(N8N_WEBHOOK_URL, {
        user_id: userId,
        message: message,
      });
      
      return response.data;
    } catch (error) {
      console.error('Error sending message to chatbot:', error);
      throw new Error('No se pudo conectar con el chatbot. Por favor, intenta de nuevo.');
    }
  }
}
