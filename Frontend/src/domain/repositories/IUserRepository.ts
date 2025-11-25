// User Repository Interface
import { User, UserRegistration, UserLogin } from '@domain/entities/User';

export interface IUserRepository {
  register(data: UserRegistration): Promise<User>;
  login(data: UserLogin): Promise<{ status: string; user_id: string }>;
  getById(id: string): Promise<User>;
  getAll(): Promise<User[]>;
}
