# Synthèse sur l'Authentification des Utilisateurs avec Symfony

## Introduction

L'authentification permet d'identifier un utilisateur visitant une page web. Symfony offre divers moyens d'authentification via le SecurityBundle :

- Form Login
- JSON Login
- HTTP Basic
- Login Link
- X.509 Client Certificates
- Remote Users
- Custom Authenticators

### Form Login

L'authentification par formulaire est courante sur les sites web, utilisant un identifiant (email ou nom d'utilisateur) et un mot de passe.

#### Mise en place

1. **Générer le code nécessaire** :
    ```bash
    php bin/console make:security:form-login
    ```

2. **Créer un contrôleur de login** :
    ```bash
    php bin/console make:controller Login
    ```

    ```php
    // src/Controller/LoginController.php
    namespace App\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Annotation\Route;
    use Symfony\Component\Security\Http\Authentication\AuthenticationUtils;

    class LoginController extends AbstractController
    {
        #[Route('/login', name: 'app_login')]
        public function index(AuthenticationUtils $authenticationUtils): Response
        {
            // Récupérer les erreurs et le dernier nom d'utilisateur saisi
            $error = $authenticationUtils->getLastAuthenticationError();
            $lastUsername = $authenticationUtils->getLastUsername();

            return $this->render('login/index.html.twig', [
                'last_username' => $lastUsername,
                'error' => $error,
            ]);
        }
    }
    ```

3. **Configurer `form_login` dans `security.yaml`** :
    ```yaml
    # config/packages/security.yaml
    security:
        firewalls:
            main:
                form_login:
                    login_path: app_login
                    check_path: app_login
    ```

4. **Créer le template de login** :
    ```twig
    {# templates/login/index.html.twig #}
    {% extends 'base.html.twig' %}

    {% block body %}
        {% if error %}
            <div>{{ error.messageKey|trans(error.messageData, 'security') }}</div>
        {% endif %}

        <form action="{{ path('app_login') }}" method="post">
            <label for="username">Email:</label>
            <input type="text" id="username" name="_username" value="{{ last_username }}">

            <label for="password">Password:</label>
            <input type="password" id="password" name="_password">

            <input type="hidden" name="_csrf_token" value="{{ csrf_token('authenticate') }}">

            <button type="submit">login</button>
        </form>
    {% endblock %}
    ```

### JSON Login

Permet de sécuriser une API via des tokens.

1. **Configurer `json_login` dans `security.yaml`** :
    ```yaml
    security:
        firewalls:
            main:
                json_login:
                    check_path: api_login
    ```

2. **Créer un contrôleur pour `api_login`** :
    ```bash
    php bin/console make:controller --no-template ApiLogin
    ```

    ```php
    // src/Controller/ApiLoginController.php
    namespace App\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Annotation\Route;
    use App\Entity\User;
    use Symfony\Component\Security\Http\Attribute\CurrentUser;

    class ApiLoginController extends AbstractController
    {
        #[Route('/api/login', name: 'api_login', methods: ['POST'])]
        public function index(#[CurrentUser] ?User $user): Response
        {
            if (null === $user) {
                return $this->json([
                    'message' => 'missing credentials',
                ], Response::HTTP_UNAUTHORIZED);
            }

            $token = ...; // Générer un token API pour l'utilisateur

            return $this->json([
                'user'  => $user->getUserIdentifier(),
                'token' => $token,
            ]);
        }
    }
    ```

3. **Exemple de requête JSON** :
    ```json
    {
        "username": "dunglas@example.com",
        "password": "MyPassword"
    }
    ```

### HTTP Basic

Authentification via une boîte de dialogue du navigateur.

1. **Configurer `http_basic` dans `security.yaml`** :
    ```yaml
    security:
        firewalls:
            main:
                http_basic:
                    realm: Secured Area
    ```

### Protection contre les attaques CSRF

1. **Activer CSRF pour `form_login`** :
    ```yaml
    security:
        firewalls:
            main:
                form_login:
                    enable_csrf: true
    ```

2. **Ajouter le token CSRF au formulaire** :
    ```twig
    <form action="{{ path('app_login') }}" method="post">
        <!-- champs de login -->

        <input type="hidden" name="_csrf_token" value="{{ csrf_token('authenticate') }}">
        
        <button type="submit">login</button>
    </form>
    ```
