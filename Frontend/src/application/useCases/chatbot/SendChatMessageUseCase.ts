// Use Case - Send Message to Chatbot
import { ChatbotResponse } from '@domain/entities/Chat';
import { IChatbotRepository } from '@domain/repositories/IChatbotRepository';

export class SendChatMessageUseCase {
  constructor(private chatbotRepository: IChatbotRepository) {}

  async execute(userId: string, message: string): Promise<ChatbotResponse> {
    return await this.chatbotRepository.sendMessage(userId, message);
  }
}
