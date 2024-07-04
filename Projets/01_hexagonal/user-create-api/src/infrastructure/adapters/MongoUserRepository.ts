import { UserRepository } from '../../domain/ports/UserRepository';
import { User } from '../../domain/entities/User';
import mongoose, { Document, Schema } from 'mongoose';

interface UserDocument extends Document {
  name: string;
  email: string;
}

const userSchema = new Schema<UserDocument>({
  name: { type: String, required: true },
  email: { type: String, required: true }
})

const UserModel = mongoose.model<UserDocument>('User', userSchema)

export class MongoUserRepository implements UserRepository {
  async saveUser(user: User): Promise<void> {
    const userDocument = new UserModel({ name: user.name, email: user.email });
    await userDocument.save();
  }

  async getUserById(userId: string): Promise<User | null> {
    const user = await UserModel.findById(userId).exec();
    if (!user) return null;
    return new User(user.id, user.name, user.email);
  }

  async getAllUsers(): Promise<User[] | null> {
    const userDocuments = await UserModel.find().exec()
    if (!userDocuments) return null
    const users : User[] = [] 

    for(const user of userDocuments) users.push(new User(user.id, user.name, user.email))

    return users
  }
}