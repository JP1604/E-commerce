// Dependency Injection Container
import { ProductRepository } from '@infrastructure/repositories/ProductRepository';
import { CartRepository } from '@infrastructure/repositories/CartRepository';
import { ChatbotRepository } from '@infrastructure/repositories/ChatbotRepository';
import { UserRepository } from '@infrastructure/repositories/UserRepository';
import { GetAllProductsUseCase } from '@application/useCases/products/GetAllProductsUseCase';
import { GetProductByIdUseCase } from '@application/useCases/products/GetProductByIdUseCase';
import { AddItemToCartUseCase } from '@application/useCases/cart/AddItemToCartUseCase';
import { GetCartUseCase } from '@application/useCases/cart/GetCartUseCase';
import { SendChatMessageUseCase } from '@application/useCases/chatbot/SendChatMessageUseCase';
import { RegisterUserUseCase } from '@application/useCases/users/RegisterUserUseCase';
import { LoginUserUseCase } from '@application/useCases/users/LoginUserUseCase';

// Repositories
const productRepository = new ProductRepository();
const cartRepository = new CartRepository();
const chatbotRepository = new ChatbotRepository();
const userRepository = new UserRepository();

// Use Cases
const getAllProductsUseCase = new GetAllProductsUseCase(productRepository);
const getProductByIdUseCase = new GetProductByIdUseCase(productRepository);
const addItemToCartUseCase = new AddItemToCartUseCase(cartRepository);
const getCartUseCase = new GetCartUseCase(cartRepository);
const sendChatMessageUseCase = new SendChatMessageUseCase(chatbotRepository);
const registerUserUseCase = new RegisterUserUseCase(userRepository);
const loginUserUseCase = new LoginUserUseCase(userRepository);

// Export container
export const container = {
  // Repositories
  productRepository,
  cartRepository,
  chatbotRepository,
  userRepository,
  // Use Cases
  getAllProductsUseCase,
  getProductByIdUseCase,
  addItemToCartUseCase,
  getCartUseCase,
  sendChatMessageUseCase,
  registerUserUseCase,
  loginUserUseCase,
};
