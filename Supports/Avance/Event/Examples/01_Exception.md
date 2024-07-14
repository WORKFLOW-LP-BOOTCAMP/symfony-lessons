# Exemple pour comprendre les Événements et Écouteurs d'Événements dans Symfony

## Créer un Écouteur d'Événements

1. **Créer une classe d'écouteur d'événements**

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
           // Récupère l'exception depuis l'événement
           $exception = $event->getThrowable();
           $message = sprintf(
               'Une erreur est survenue : %s avec le code : %s',
               $exception->getMessage(),
               $exception->getCode()
           );

           // Personnalise l'objet de réponse pour afficher les détails de l'exception
           $response = new Response();
           $response->setContent($message);

           if ($exception instanceof HttpExceptionInterface) {
               $response->setStatusCode($exception->getStatusCode());
               $response->headers->replace($exception->getHeaders());
           } else {
               $response->setStatusCode(Response::HTTP_INTERNAL_SERVER_ERROR);
           }

           // Envoie l'objet de réponse modifié à l'événement
           $event->setResponse($response);
       }
   }
   ```

2. **Enregistrer l'écouteur comme service**

   ```yaml
   # config/services.yaml
   services:
       App\EventListener\ExceptionListener:
           tags: [kernel.event_listener]
   ```

## Créer un Contrôleur qui Déclenche une Exception

1. **Créer une classe de contrôleur**

   ```php
   // src/Controller/DemoController.php
   namespace App\Controller;

   use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
   use Symfony\Component\HttpFoundation\Response;
   use Symfony\Component\Routing\Annotation\Route;

   class DemoController extends AbstractController
   {
       #[Route('/exception', name: 'exception_demo')]
       public function exceptionDemo(): Response
       {
           // Déclenche une exception pour tester l'écouteur
           throw new \Exception('Ceci est une exception test.');
       }
   }
   ```

## Tester l'Écouteur

1. **Démarrer le serveur Symfony**

   ```sh
   symfony serve
   ```

2. **Accéder à l'URL qui déclenche l'exception**

   Ouvrez votre navigateur et accédez à l'URL `http://localhost:8000/exception`. Vous devriez voir un message personnalisé provenant de l'ExceptionListener.

# Explication

- **ExceptionListener** : Cette classe écoute les événements d'exception. Lorsqu'une exception se produit, elle capture l'exception, crée une réponse personnalisée et l'envoie à l'utilisateur.
- **Enregistrement de l'Écouteur** : En enregistrant ExceptionListener comme service avec le tag `kernel.event_listener`, Symfony sait que cette classe doit être appelée lorsqu'un événement d'exception est déclenché.
- **Déclenchement de l'Exception** : Le contrôleur `DemoController` déclenche une exception en accédant à `/exception`. Cela permet de tester si l'ExceptionListener fonctionne correctement.

Cet exemple montre comment réagir à une exception avec un écouteur d'événements dans Symfony, en personnalisant la réponse envoyée à l'utilisateur.