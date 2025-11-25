// Register User Use Case
import { User, UserRegistration } from '@domain/entities/User';
import { IUserRepository } from '@domain/repositories/IUserRepository';

export class RegisterUserUseCase {
  constructor(private userRepository: IUserRepository) {}

  async execute(data: UserRegistration): Promise<User> {
    return await this.userRepository.register(data);
  }
}
