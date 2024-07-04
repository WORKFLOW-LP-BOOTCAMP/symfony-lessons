import express from 'express';
import mongoose from 'mongoose';
import routes from './application/routes/userRoutes';
import { MongoUserRepository } from './infrastructure/adapters/MongoUserRepository';
import { CreateUserUseCase } from './domain/usecases/CreateUserUseCase';
import { UserController } from './application/controllers/UserController';

// Initialize Express app
const app = express()

// Parse JSON request body
app.use(express.json())

// Connect to MongoDB
mongoose.connect('mongodb://mongo:27017/create-user', {})

// Create MongoUserRepository instance
const userRepository = new MongoUserRepository()

// Create CreateUserUseCase instance
const createUserUseCase = new CreateUserUseCase(userRepository)

// Create UserController instance
const userController = new UserController(createUserUseCase, userRepository)

// Mount user routes
app.use('/api', routes)

// Start the server
const PORT = process.env.PORT || 3000

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`)
});
