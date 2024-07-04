// application/routes/UserRoutes.ts
import { Router, Request, Response } from 'express';
import { UserController } from '../controllers/UserController';
import { MongoUserRepository } from '../../infrastructure/adapters/MongoUserRepository';
import { CreateUserUseCase } from '../../domain/usecases/CreateUserUseCase';

const router = Router();

// Create MongoUserRepository instance
const userRepository = new MongoUserRepository();

// Create CreateUserUseCase instance
const createUserUseCase = new CreateUserUseCase(userRepository);

// Create UserController instance
const userController = new UserController(createUserUseCase, userRepository);

router.post('/user', (req, res) => userController.createUser(req, res));
router.get('/user/:id', (req, res) => userController.getUserById(req, res));

router.get('/users', (req : Request, res : Response) => userController.getAllUsers(req, res));


router.get('/a', (req, res) => res.json('hello'))

export default router;
