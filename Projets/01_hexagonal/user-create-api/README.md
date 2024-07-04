### TP : Création d'une Application de Gestion d'Utilisateurs avec Port et Adaptateur et Intégration de MongoDB

#### Contexte

Vous devez créer une application simple pour gérer les utilisateurs. Vous utiliserez une base de données MongoDB pour stocker les données.

L'application doit permettre de créer des utilisateurs et de les récupérer par leur identifiant.

Vous utiliserez le design pattern Port et Adaptateur pour séparer la logique métier de la logique d'accès aux données.

#### Exigences

1. **Entités** : Créez une classe `User` pour représenter les utilisateurs avec les propriétés `id`, `name`, et `email`.
2. **Ports** : Créez une interface `UserRepository` qui définira les méthodes `saveUser` et `getUserById`.
3. **Use Case** : Créez une classe `CreateUserUseCase` qui contiendra la logique pour créer un utilisateur.
4. **Adaptateurs** : Implémentez un adaptateur `MongoUserRepository` qui stockera les utilisateurs dans MongoDB.
5. **Point d'entrée de l'application** : Créez une API HTTP avec Express.js pour exposer les opérations de création et de récupération des utilisateurs.
6. **Dockerisation** : Configurez des fichiers Docker pour le développement et la production, et utilisez `docker-compose` pour orchestrer les conteneurs incluant MongoDB.

### Structure du Projet

Voici la structure de votre projet :

```
create-user
├── domain
│   ├── entities
│   │   └── User.ts
│   ├── ports
│   │   └── UserRepository.ts
│   └── usecases
│       └── CreateUserUseCase.ts
├── infrastructure
│   └── adapters
│       └── MongoUserRepository.ts
├── application
│   └── UserController.ts
├── app.ts
├── Dockerfile.dev
├── Dockerfile.prod
├── docker-compose.yml
├── package.json
└── tsconfig.json
```

### 1. Entités

Créez la classe `User` dans `domain/entities/User.ts`.

```typescript
// domain/entities/User.ts
export class User {
  constructor(
    public id: string,
    public name: string,
    public email: string
  ) {}
}
```

### 2. Ports

Créez l'interface `UserRepository` dans `domain/ports/UserRepository.ts`.

```typescript
// domain/ports/UserRepository.ts
import { User } from '../entities/User';

export interface UserRepository {
  saveUser(user: User): Promise<void>;
  getUserById(userId: string): Promise<User | null>;
}
```

### 3. Use Case

Créez la classe `CreateUserUseCase` dans `domain/usecases/CreateUserUseCase.ts`.

```typescript
// domain/usecases/CreateUserUseCase.ts
import { UserRepository } from '../ports/UserRepository';
import { User } from '../entities/User';

export class CreateUserUseCase {
  constructor(private userRepository: UserRepository) {}

  async execute(name: string, email: string): Promise<User> {
    const user = new User(Date.now().toString(), name, email);
    await this.userRepository.saveUser(user);
    return user;
  }
}
```

### 4. Adaptateurs

Implémentez `MongoUserRepository` dans `infrastructure/adapters/MongoUserRepository.ts`.

```typescript
// infrastructure/adapters/MongoUserRepository.ts
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
});

const UserModel = mongoose.model<UserDocument>('User', userSchema);

export class MongoUserRepository implements UserRepository {
  async saveUser(user: User): Promise<void> {
    const userDocument = new UserModel({ name: user.name, email: user.email });
    await userDocument.save();
  }

  async getUserById(userId: string): Promise<User | null> {
    const userDocument = await UserModel.findById(userId).exec();
    if (!userDocument) return null;
    return new User(userDocument.id, userDocument.name, userDocument.email);
  }
}
```

### 5. Point d'entrée de l'application

Créez le contrôleur `UserController` dans `application/UserController.ts`.

```typescript
// application/UserController.ts
import express, { Request, Response } from 'express';
import mongoose from 'mongoose';
import { CreateUserUseCase } from '../domain/usecases/CreateUserUseCase';
import { MongoUserRepository } from '../infrastructure/adapters/MongoUserRepository';

const app = express();
app.use(express.json());

mongoose.connect(process.env.MONGO_URI || '', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const userRepository = new MongoUserRepository();
const createUserUseCase = new CreateUserUseCase(userRepository);

app.post('/users', async (req: Request, res: Response) => {
  const { name, email } = req.body;
  try {
    const user = await createUserUseCase.execute(name, email);
    res.status(201).json(user);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

app.get('/users/:id', async (req: Request, res: Response) => {
  const userId = req.params.id;
  try {
    const user = await userRepository.getUserById(userId);
    if (user) {
      res.json(user);
    } else {
      res.status(404).send('User not found');
    }
  } catch (err) {
    res.status(500).send(err.message);
  }
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### 6. Point d'entrée principal

Créez le fichier `app.ts` pour démarrer l'application.

```typescript
// app.ts
import './application/UserController';
```

### 7. Dockerisation

Créez deux fichiers Docker, un pour le développement (`Dockerfile.dev`) et un pour la production (`Dockerfile.prod`), ainsi qu'un fichier `docker-compose.yml` pour orchestrer les conteneurs, incluant MongoDB.

#### Dockerfile pour le Développement

```dockerfile
# Dockerfile.dev

# Utilisation de l'image officielle Node.js 20.14.0 pour le développement
FROM node:20.14.0

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers package.json et package-lock.json dans le répertoire de travail
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tous les fichiers du projet dans le répertoire de travail
COPY . .

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 3000

# Commande pour démarrer l'application en mode développement
CMD ["npm", "run", "dev"]
```

#### Dockerfile pour la Production

```dockerfile
# Dockerfile.prod

# Étape 1 : Construction de l'image
FROM node:20.14.0 AS build

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers package.json et package-lock.json dans le répertoire de travail
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tous les fichiers du projet dans le répertoire de travail
COPY . .

# Compiler le code TypeScript
RUN npm run build

# Étape 2 : Création de l'image pour l'exécution
FROM node:20.14.0

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers package.json et package-lock.json dans le répertoire de travail
COPY package*.json ./

# Installer uniquement les dépendances de production
RUN npm install --only=production

# Copier les fichiers compilés et les autres fichiers nécessaires depuis l'étape de build
COPY --from=build /app/dist ./dist
COPY --from=build /app/src ./src

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 3000

# Commande pour démarrer l'application
CMD ["node", "dist/app.js"]
```

#### docker-compose.yml

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      MONGO_URI: mongodb://mongo:27017/create-user
    depends_on:
      - mongo

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

### Commandes Docker

Pour construire et exécuter les conteneurs, utilisez les commandes suivantes :

1. **Pour le développement** :

   ```bash
   docker-compose up
   ```

2. **Pour la production** :

   Modifiez le fichier `docker-compose.yml` pour utiliser le `Dockerfile.prod` au lieu de `Dockerfile.dev`


## Annexes

1. Requêtes pour insérer un utilisateur

```bash
curl -X POST http://localhost:3000/api/user -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com"}'
```

2. Insérer des données dans la base de données, ces données sont montées dans le conteneur (voir le docker-compose)

```bash
mongoimport --db create-user --collection users --file users.json --jsonArray --drop
```