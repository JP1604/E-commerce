// Cart Repository Interface
import { Cart, CartItem } from '../entities/Cart';

export interface ICartRepository {
  getCart(userId: string): Promise<Cart>;
  addItem(cartId: string, item: Omit<CartItem, 'id_item' | 'product_name' | 'id_cart' | 'created_at' | 'updated_at'>): Promise<Cart>;
  removeItem(cartId: string, itemId: string): Promise<Cart>;
  clearCart(cartId: string): Promise<void>;
}
