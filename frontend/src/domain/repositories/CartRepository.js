/**
 * @interface CartRepository
 * @description Interface for cart data operations
 */

export const CartRepositoryInterface = {
  getByUserId: async (userId) => { throw new Error('Not implemented'); },
  getById: async (cartId) => { throw new Error('Not implemented'); },
  create: async (userId) => { throw new Error('Not implemented'); },
  addItem: async (cartId, productId, quantity) => { throw new Error('Not implemented'); },
  updateItem: async (cartId, itemId, quantity) => { throw new Error('Not implemented'); },
  removeItem: async (cartId, itemId) => { throw new Error('Not implemented'); },
  getItems: async (cartId) => { throw new Error('Not implemented'); },
};
