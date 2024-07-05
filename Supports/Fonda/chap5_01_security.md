## Cours sur la Sécurité dans Symfony

### Introduction
Symfony propose divers outils pour sécuriser votre application. Parmi ceux-ci, on trouve la protection des cookies de session et la protection CSRF, activées par défaut. Le SecurityBundle fournit toutes les fonctionnalités nécessaires pour l'authentification et l'autorisation.

### Installation du SecurityBundle
Pour commencer, installez le SecurityBundle :
```bash
composer require symfony/security-bundle
```
Si Symfony Flex est installé, un fichier de configuration `security.yaml` sera créé automatiquement.

### Configuration de base
Voici un exemple de configuration de base dans `security.yaml` :

```yaml
# config/packages/security.yaml
security:
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'
    providers:
        users_in_memory: { memory: null }
    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        main:
            lazy: true
            provider: users_in_memory
    access_control:
        # - { path: ^/admin, roles: ROLE_ADMIN }
        # - { path: ^/profile, roles: ROLE_USER }
```

### Les éléments principaux

1. **Le User (providers)** : Le provider de users charge les utilisateurs depuis n'importe quel stockage (base de données, etc.) en se basant sur un identifiant unique.
2. **Le Firewall et l'authentification des utilisateurs (firewalls)** : Le firewall vérifie chaque requête pour voir si elle nécessite un utilisateur authentifié et s'occupe de l'authentification.
3. **Contrôle d'accès (Authorization) (access_control)** : Contrôle les permissions requises pour accéder à une URL spécifique ou effectuer une action.

### Création d'une classe User

Utilisez la commande suivante pour générer une classe User :
```bash
php bin/console make:user
```
Répondez aux questions pour configurer votre classe User. Voici un exemple de la classe générée :

```php
// src/Entity/User.php
namespace App\Entity;

use App\Repository\UserRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;

#[ORM\Entity(repositoryClass: UserRepository::class)]
class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 180, unique: true)]
    private ?string $email;

    #[ORM\Column(type: 'json')]
    private array $roles = [];

    #[ORM\Column(type: 'string')]
    private string $password;

    // getters and setters...
}
```

### Fournisseur d'utilisateurs (User Provider)

Le `make:user` ajoute également une configuration pour un fournisseur d'utilisateurs dans votre `security.yaml` :

```yaml
# config/packages/security.yaml
security:
    # ...
    providers:
        app_user_provider:
            entity:
                class: App\Entity\User
                property: email
```

### Hachage des mots de passe

Assurez-vous que votre classe User implémente `PasswordAuthenticatedUserInterface` :

```php
// src/Entity/User.php
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;

class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    public function getPassword(): string
    {
        return $this->password;
    }

    // ...
}
```

Configurez le hasher de mot de passe dans `security.yaml` :

```yaml
# config/packages/security.yaml
security:
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'
```

### Utilisation du hasher de mot de passe

Utilisez le service `UserPasswordHasherInterface` pour hacher le mot de passe avant de sauvegarder les utilisateurs :

```php
// src/Controller/RegistrationController.php
namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

class RegistrationController extends AbstractController
{
    public function index(UserPasswordHasherInterface $passwordHasher): Response
    {
        $user = new User();
        $plaintextPassword = 'password';

        $hashedPassword = $passwordHasher->hashPassword(
            $user,
            $plaintextPassword
        );
        $user->setPassword($hashedPassword);

        // save the user
    }
}
```

### Configuration des firewalls

La section firewalls de `security.yaml` est essentielle. Elle définit les parties sécurisées de votre application et les méthodes d'authentification.

```yaml
# config/packages/security.yaml
security:
    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        main:
            lazy: true
            provider: app_user_provider
```

Un firewall peut avoir plusieurs modes d'authentification, et l'ordre des firewalls est important car la requête sera traitée par le premier firewall correspondant.
