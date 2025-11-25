// User Repository Implementation
import { User, UserRegistration, UserLogin } from '@domain/entities/User';
import { IUserRepository } from '@domain/repositories/IUserRepository';
import { apiClient } from '../http/httpClient';

export class UserRepository implements IUserRepository {
  private readonly basePath = '/api/v1/users/';

  async register(data: UserRegistration): Promise<User> {
    const response = await apiClient.post<User>(this.basePath, data);
    return response.data;
  }

  async login(data: UserLogin): Promise<{ status: string; user_id: string }> {
    const response = await apiClient.post<{ status: string; user_id: string }>(
      `${this.basePath}login`,
      data
    );
    return response.data;
  }

  async getById(id: string): Promise<User> {
    const response = await apiClient.get<User>(`${this.basePath}${id}`);
    return response.data;
  }

  async getAll(): Promise<User[]> {
    const response = await apiClient.get<User[]>(this.basePath);
    return response.data;
  }
}
