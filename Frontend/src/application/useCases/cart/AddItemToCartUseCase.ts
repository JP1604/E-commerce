// Use Case - Add Item to Cart
import { Cart, CartItem } from '@domain/entities/Cart';
import { ICartRepository } from '@domain/repositories/ICartRepository';

export class AddItemToCartUseCase {
  constructor(private cartRepository: ICartRepository) {}

  async execute(
    cartId: string,
    item: Omit<CartItem, 'id_item' | 'product_name' | 'id_cart' | 'created_at' | 'updated_at'>
  ): Promise<Cart> {
    return await this.cartRepository.addItem(cartId, item);
  }
}
