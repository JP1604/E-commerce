// Domain Repository Interface - Chatbot
import { ChatbotResponse } from '../entities/Chat';

export interface IChatbotRepository {
  sendMessage(userId: string, message: string): Promise<ChatbotResponse>;
}
