import { cartApi } from '../api/apiClient';
import { createCart, createCartItem } from '../../domain/entities/Cart';

export class CartRepositoryImpl {
  async getByUserId(userId) {
    const response = await cartApi.get(`/carts/user/${userId}`);
    return createCart(response.data);
  }

  async getById(cartId) {
    const response = await cartApi.get(`/carts/${cartId}`);
    return createCart(response.data);
  }

  async create(userId, status = 'activo') {
    const response = await cartApi.post('/carts/', { user_id: userId, status });
    return createCart(response.data);
  }

  async addItem(cartId, productId, quantity) {
    const response = await cartApi.post(`/carts/${cartId}/items`, {
      product_id: productId,
      quantity,
    });
    return createCartItem(response.data);
  }

  async updateItem(cartId, itemId, quantity) {
    const response = await cartApi.put(`/carts/${cartId}/items/${itemId}`, { quantity });
    return createCartItem(response.data);
  }

  async removeItem(cartId, itemId) {
    await cartApi.delete(`/carts/${cartId}/items/${itemId}`);
  }

  async getItems(cartId) {
    const response = await cartApi.get(`/carts/${cartId}/items`);
    return response.data.map(createCartItem);
  }
}

export const cartRepository = new CartRepositoryImpl();
