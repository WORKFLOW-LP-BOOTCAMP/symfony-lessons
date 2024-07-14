# Exemple avec une Base de Données

Voici un exemple qui montre comment créer un écouteur d'événements dans Symfony qui interagit avec une base de données. L'exemple se concentre sur la capture d'un événement d'enregistrement d'utilisateur et l'enregistrement d'un journal dans la base de données.

## Créer une Entité User et une Entité Log

1. **Créer l'entité User**

   ```php
   // src/Entity/User.php
   namespace App\Entity;

   use Doctrine\ORM\Mapping as ORM;

   #[ORM\Entity]
   class User
   {
       #[ORM\Id, ORM\GeneratedValue, ORM\Column(type: 'integer')]
       private ?int $id = null;

       #[ORM\Column(type: 'string', length: 255)]
       private string $username;

       #[ORM\Column(type: 'string', length: 255)]
       private string $email;

       // Getters et setters
       public function getId(): ?int
       {
           return $this->id;
       }

       public function getUsername(): string
       {
           return $this->username;
       }

       public function setUsername(string $username): self
       {
           $this->username = $username;
           return $this;
       }

       public function getEmail(): string
       {
           return $this->email;
       }

       public function setEmail(string $email): self
       {
           $this->email = $email;
           return $this;
       }
   }
   ```

2. **Créer l'entité Log**

   ```php
   // src/Entity/Log.php
   namespace App\Entity;

   use Doctrine\ORM\Mapping as ORM;

   #[ORM\Entity]
   class Log
   {
       #[ORM\Id, ORM\GeneratedValue, ORM\Column(type: 'integer')]
       private ?int $id = null;

       #[ORM\Column(type: 'string', length: 255)]
       private string $action;

       #[ORM\Column(type: 'datetime')]
       private \DateTimeInterface $createdAt;

       // Getters et setters
       public function getId(): ?int
       {
           return $this->id;
       }

       public function getAction(): string
       {
           return $this->action;
       }

       public function setAction(string $action): self
       {
           $this->action = $action;
           return $this;
       }

       public function getCreatedAt(): \DateTimeInterface
       {
           return $this->createdAt;
       }

       public function setCreatedAt(\DateTimeInterface $createdAt): self
       {
           $this->createdAt = $createdAt;
           return $this;
       }
   }
   ```

3. **Créer la migration et mettre à jour la base de données**

   ```sh
   php bin/console make:migration
   php bin/console doctrine:migrations:migrate
   ```

##  Créer un Événement et un Écouteur

1. **Créer un événement UserRegisteredEvent**

   ```php
   // src/Event/UserRegisteredEvent.php
   namespace App\Event;

   use App\Entity\User;
   use Symfony\Contracts\EventDispatcher\Event;

   class UserRegisteredEvent extends Event
   {
       public const NAME = 'user.registered';

       private User $user;

       public function __construct(User $user)
       {
           $this->user = $user;
       }

       public function getUser(): User
       {
           return $this->user;
       }
   }
   ```

2. **Créer un écouteur UserRegisteredListener**

   ```php
   // src/EventListener/UserRegisteredListener.php
   namespace App\EventListener;

   use App\Event\UserRegisteredEvent;
   use App\Entity\Log;
   use Doctrine\ORM\EntityManagerInterface;

   class UserRegisteredListener
   {
       private EntityManagerInterface $entityManager;

       public function __construct(EntityManagerInterface $entityManager)
       {
           $this->entityManager = $entityManager;
       }

       public function onUserRegistered(UserRegisteredEvent $event): void
       {
           $log = new Log();
           $log->setAction('User registered: ' . $event->getUser()->getUsername());
           $log->setCreatedAt(new \DateTime());

           $this->entityManager->persist($log);
           $this->entityManager->flush();
       }
   }
   ```

3. **Enregistrer l'écouteur comme service**

   ```yaml
   # config/services.yaml
   services:
       App\EventListener\UserRegisteredListener:
           tags:
               - { name: kernel.event_listener, event: 'user.registered', method: 'onUserRegistered' }
   ```

## Déclencher l'Événement dans le Contrôleur

1. **Créer un contrôleur pour enregistrer l'utilisateur**

   ```php
   // src/Controller/UserController.php
   namespace App\Controller;

   use App\Entity\User;
   use App\Event\UserRegisteredEvent;
   use Doctrine\ORM\EntityManagerInterface;
   use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
   use Symfony\Component\HttpFoundation\Request;
   use Symfony\Component\HttpFoundation\Response;
   use Symfony\Component\Routing\Annotation\Route;
   use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

   class UserController extends AbstractController
   {
       #[Route('/register', name: 'user_register', methods: ['POST'])]
       public function register(Request $request, EntityManagerInterface $entityManager, EventDispatcherInterface $eventDispatcher): Response
       {
           $username = $request->request->get('username');
           $email = $request->request->get('email');

           $user = new User();
           $user->setUsername($username);
           $user->setEmail($email);

           $entityManager->persist($user);
           $entityManager->flush();

           $event = new UserRegisteredEvent($user);
           $eventDispatcher->dispatch($event, UserRegisteredEvent::NAME);

           return new Response('User registered successfully');
       }
   }
   ```

## Tester l'Application

1. **Démarrer le serveur Symfony**

   ```sh
   symfony serve
   ```

2. **Envoyer une requête POST pour enregistrer un utilisateur**

   Utilisez un outil comme Postman ou curl pour envoyer une requête POST à `http://localhost:8000/register` avec les paramètres `username` et `email`.

   ```sh
   curl -X POST http://localhost:8000/register -d "username=john_doe&email=john@example.com"
   ```

3. **Vérifier la base de données**

   Consultez la table `log` dans votre base de données pour voir le journal de l'inscription de l'utilisateur.

# Explication

- **UserRegisteredEvent** : Un événement personnalisé déclenché après l'enregistrement d'un utilisateur.
- **UserRegisteredListener** : Un écouteur qui réagit à l'événement d'enregistrement d'utilisateur en créant une entrée de journal dans la base de données.
- **Contrôleur** : Gère l'enregistrement de l'utilisateur et déclenche l'événement `UserRegisteredEvent`.
