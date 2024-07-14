# Événements et Écouteurs d'Événements dans Symfony

## Introduction
Dans une application Symfony, de nombreuses notifications d'événements sont déclenchées. Votre application peut écouter ces notifications et y répondre en exécutant n'importe quel morceau de code. Symfony déclenche plusieurs événements liés au kernel lors du traitement de la requête HTTP. Les bundles tiers peuvent également dispatcher des événements, et vous pouvez même dispatcher des événements personnalisés depuis votre propre code.

## Création d'un Écouteur d'Événements

## Exemple de Création
```php
// src/EventListener/ExceptionListener.php
namespace App\EventListener;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Event\ExceptionEvent;
use Symfony\Component\HttpKernel\Exception\HttpExceptionInterface;

class ExceptionListener
{
    public function __invoke(ExceptionEvent $event): void
    {
        $exception = $event->getThrowable();
        $message = sprintf(
            'My Error says: %s with code: %s',
            $exception->getMessage(),
            $exception->getCode()
        );

        $response = new Response();
        $response->setContent($message);

        if ($exception instanceof HttpExceptionInterface) {
            $response->setStatusCode($exception->getStatusCode());
            $response->headers->replace($exception->getHeaders());
        } else {
            $response->setStatusCode(Response::HTTP_INTERNAL_SERVER_ERROR);
        }

        $event->setResponse($response);
    }
}
```

## Enregistrement de l'Écouteur
```yaml
# config/services.yaml
services:
    App\EventListener\ExceptionListener:
        tags: [kernel.event_listener]
```

## Utilisation des Attributs PHP
```php
namespace App\EventListener;

use Symfony\Component\EventDispatcher\Attribute\AsEventListener;

#[AsEventListener]
final class MyListener
{
    public function __invoke(CustomEvent $event): void
    {
        // ...
    }
}
```

## Création d'un Subscriber d'Événements
Les subscribers définissent plusieurs méthodes écoutant divers événements.

## Exemple de Subscriber
```php
// src/EventSubscriber/ExceptionSubscriber.php
namespace App\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\ExceptionEvent;
use Symfony\Component\HttpKernel\KernelEvents;

class ExceptionSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            KernelEvents::EXCEPTION => [
                ['processException', 10],
                ['logException', 0],
                ['notifyException', -10],
            ],
        ];
    }

    public function processException(ExceptionEvent $event): void
    {
        // ...
    }

    public function logException(ExceptionEvent $event): void
    {
        // ...
    }

    public function notifyException(ExceptionEvent $event): void
    {
        // ...
    }
}
```

## Écoute des Requêtes Principales
```php
// src/EventListener/RequestListener.php
namespace App\EventListener;

use Symfony\Component\HttpKernel\Event\RequestEvent;

class RequestListener
{
    public function onKernelRequest(RequestEvent $event): void
    {
        if (!$event->isMainRequest()) {
            return;
        }

        // ...
    }
}
```

## Utilisation de Listeners et Subscribers
Les listeners et subscribers peuvent être utilisés ensemble dans une même application. Les subscribers sont plus faciles à réutiliser car ils contiennent la connaissance des événements, tandis que les listeners sont plus flexibles pour une configuration conditionnelle.

## Exemple de Filtrage Avant et Après

## Avant le Contrôleur
```php
// src/EventSubscriber/TokenSubscriber.php
namespace App\EventSubscriber;

use App\Controller\TokenAuthenticatedController;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\ControllerEvent;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;
use Symfony\Component\HttpKernel\KernelEvents;

class TokenSubscriber implements EventSubscriberInterface
{
    public function __construct(private array $tokens) {}

    public function onKernelController(ControllerEvent $event): void
    {
        $controller = $event->getController();
        if (is_array($controller)) {
            $controller = $controller[0];
        }

        if ($controller instanceof TokenAuthenticatedController) {
            $token = $event->getRequest()->query->get('token');
            if (!in_array($token, $this->tokens)) {
                throw new AccessDeniedHttpException('This action needs a valid token!');
            }
            $event->getRequest()->attributes->set('auth_token', $token);
        }
    }

    public static function getSubscribedEvents(): array
    {
        return [
            KernelEvents::CONTROLLER => 'onKernelController',
        ];
    }
}
```

## Après le Contrôleur
```php
use Symfony\Component\HttpKernel\Event\ResponseEvent;

public function onKernelResponse(ResponseEvent $event): void
{
    if (!$token = $event->getRequest()->attributes->get('auth_token')) {
        return;
    }

    $response = $event->getResponse();
    $hash = sha1($response->getContent() . $token);
    $response->headers->set('X-CONTENT-HASH', $hash);
}

public static function getSubscribedEvents(): array
{
    return [
        KernelEvents::CONTROLLER => 'onKernelController',
        KernelEvents::RESPONSE => 'onKernelResponse',
    ];
}
```

## Debugging des Listeners
Vous pouvez trouver les listeners enregistrés dans le dispatcher d'événements en utilisant la console Symfony :
```sh
php bin/console debug:event-dispatcher
```
Pour obtenir les listeners d'un événement spécifique :
```sh
php bin/console debug:event-dispatcher kernel.exception
```

## Conclusion
Les événements et écouteurs d'événements dans Symfony permettent une grande flexibilité pour exécuter du code en réponse à divers événements tout au long du cycle de vie de la requête HTTP. Les listeners et subscribers offrent des moyens différents mais complémentaires pour écouter et gérer ces événements.