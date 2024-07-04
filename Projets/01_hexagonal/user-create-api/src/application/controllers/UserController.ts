// application/controllers/UserController.ts
import { Request, Response } from 'express';
import { CreateUserUseCase } from '../../domain/usecases/CreateUserUseCase';
import { UserRepository } from '../../domain/ports/UserRepository';

export class UserController {
  constructor(
    private createUserUseCase: CreateUserUseCase,
    private userRepository: UserRepository
  ) {}

  async createUser(req: Request, res: Response): Promise<void> {
    const { name, email } = req.body;
    try {
      const user = await this.createUserUseCase.execute(name, email);
      res.status(201).json(user);
    } catch (err) {
      res.status(500).send('error');
    }
  }

  async getUserById(req: Request, res: Response): Promise<void> {
    const userId = req.params.id;
    console.log("userID" , userId)
    try {
      const user = await this.userRepository.getUserById(userId);
      if (user) {
        res.json(user);
      } else {
        res.status(404).send('User not found');
      }
    } catch (err) {
      res.status(500).send('error');
    }
  }

  async getAllUsers(req: Request, res: Response): Promise<void> {
    
    try {
      const users = await this.userRepository.getAllUsers();
      res.status(200).json(users);
    } catch (err) {
      res.status(500).send('error');
    }
  }
}
