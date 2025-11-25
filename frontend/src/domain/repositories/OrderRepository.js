/**
 * @interface OrderRepository
 * @description Interface for order data operations
 */

export const OrderRepositoryInterface = {
  getAll: async () => { throw new Error('Not implemented'); },
  getById: async (id) => { throw new Error('Not implemented'); },
  getByUserId: async (userId) => { throw new Error('Not implemented'); },
  create: async (order) => { throw new Error('Not implemented'); },
  updateStatus: async (id, status) => { throw new Error('Not implemented'); },
};
