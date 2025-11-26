import { userApi } from '../api/apiClient';
import { createUser } from '../../domain/entities/User';

export class UserRepositoryImpl {
  async getAll() {
    const response = await userApi.get('/users/');
    return response.data.map(createUser);
  }

  async getById(id) {
    const response = await userApi.get(`/users/${id}`);
    return createUser(response.data);
  }

  async create(userData) {
    const response = await userApi.post('/users/', userData);
    return createUser(response.data);
  }

  async update(id, userData) {
    const response = await userApi.put(`/users/${id}`, userData);
    return createUser(response.data);
  }

  async delete(id) {
    await userApi.delete(`/users/${id}`);
  }

  async login(credentials) {
    // En el backend deberías tener un endpoint /users/login
    console.log('🔐 Intentando login con:', credentials.email);
    try {
      const response = await userApi.post('/users/login', credentials);
      console.log('✅ Respuesta del backend:', response.data);
      const user = createUser(response.data);
      console.log('✅ Usuario creado:', user);
      return user;
    } catch (error) {
      console.error('❌ Error en login:', error.response?.data || error.message);
      // Si no existe endpoint de login, buscar por email
      if (error.response?.status === 404) {
        const allUsersResponse = await userApi.get('/users/');
        const user = allUsersResponse.data.find(u => u.email === credentials.email);
        if (user) {
          return createUser(user);
        }
      }
      throw error;
    }
  }
}

export const userRepository = new UserRepositoryImpl();
