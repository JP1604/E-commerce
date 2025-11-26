/**
 * @interface ProductRepository
 * @description Interface for product data operations
 */

export const ProductRepositoryInterface = {
  getAll: async () => { throw new Error('Not implemented'); },
  getById: async (id) => { throw new Error('Not implemented'); },
  create: async (product) => { throw new Error('Not implemented'); },
  update: async (id, product) => { throw new Error('Not implemented'); },
  delete: async (id) => { throw new Error('Not implemented'); },
};
