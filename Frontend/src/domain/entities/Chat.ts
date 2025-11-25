// Domain Entity - Chat Message
export interface ChatMessage {
  id: string;
  user_id: string;
  message: string;
  response?: string;
  timestamp: Date;
  isUser: boolean;
}

export interface ChatbotResponse {
  response: string;
}
