// Use Case - Get Cart
import { Cart } from '@domain/entities/Cart';
import { ICartRepository } from '@domain/repositories/ICartRepository';

export class GetCartUseCase {
  constructor(private cartRepository: ICartRepository) {}

  async execute(userId: string): Promise<Cart> {
    return await this.cartRepository.getCart(userId);
  }
}
