// Cart Repository Implementation
import { Cart, CartItem } from '@domain/entities/Cart';
import { ICartRepository } from '@domain/repositories/ICartRepository';
import { apiClient } from '../http/httpClient';

export class CartRepository implements ICartRepository {
  private readonly basePath = '/api/v1/carts/';

  async getCart(userId: string): Promise<Cart> {
    try {
      // Try to get existing active cart for user
      const response = await apiClient.get<Cart>(`${this.basePath}user/${userId}`);
      return response.data;
    } catch (error: any) {
      // If no cart exists (404), create one
      if (error.response?.status === 404) {
        const createResponse = await apiClient.post<Cart>(this.basePath, {
          user_id: userId,
          status: 'activo'
        });
        return createResponse.data;
      }
      throw error;
    }
  }

  async addItem(cartId: string, item: Omit<CartItem, 'id_item' | 'product_name' | 'id_cart' | 'created_at' | 'updated_at'>): Promise<Cart> {
    // Add item to cart
    await apiClient.post(`${this.basePath}${cartId}/items`, {
      product_id: item.product_id,
      quantity: item.quantity,
      price: item.price
    });
    
    // Fetch updated cart
    const response = await apiClient.get<Cart>(`${this.basePath}${cartId}`);
    return response.data;
  }

  async removeItem(cartId: string, itemId: string): Promise<Cart> {
    await apiClient.delete(`${this.basePath}${cartId}/items/${itemId}`);
    const response = await apiClient.get<Cart>(`${this.basePath}${cartId}`);
    return response.data;
  }

  async clearCart(cartId: string): Promise<void> {
    await apiClient.delete(`${this.basePath}${cartId}`);
  }
}
