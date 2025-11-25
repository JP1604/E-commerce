// Login User Use Case
import { UserLogin } from '@domain/entities/User';
import { IUserRepository } from '@domain/repositories/IUserRepository';

export class LoginUserUseCase {
  constructor(private userRepository: IUserRepository) {}

  async execute(data: UserLogin): Promise<{ status: string; user_id: string }> {
    return await this.userRepository.login(data);
  }
}
