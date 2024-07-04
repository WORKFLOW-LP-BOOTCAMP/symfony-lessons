import { User } from '../entities/User'

export interface UserRepository {
  saveUser(user: User): Promise<void>
  getUserById(userId: string): Promise<User | null>
  getAllUsers(): Promise<User[] | null>
}