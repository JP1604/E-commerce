/**
 * @interface UserRepository
 * @description Interface for user data operations
 */

export const UserRepositoryInterface = {
  getAll: async () => { throw new Error('Not implemented'); },
  getById: async (id) => { throw new Error('Not implemented'); },
  create: async (user) => { throw new Error('Not implemented'); },
  update: async (id, user) => { throw new Error('Not implemented'); },
  delete: async (id) => { throw new Error('Not implemented'); },
};
