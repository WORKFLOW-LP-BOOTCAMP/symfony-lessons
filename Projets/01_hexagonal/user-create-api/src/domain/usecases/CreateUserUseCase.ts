import { UserRepository } from '../ports/UserRepository'

import { User } from '../entities/User'

export class CreateUserUseCase {
  constructor(private userRepository: UserRepository) {}

  async execute(name: string, email: string): Promise<User> {
    const user = new User(Date.now().toString(), name, email)
    await this.userRepository.saveUser(user)
    
    return user
  }
}