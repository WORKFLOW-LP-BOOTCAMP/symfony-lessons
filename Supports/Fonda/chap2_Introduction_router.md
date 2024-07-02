# Routage dans Symfony

Le routage dans Symfony est essentiel pour diriger les requêtes entrantes vers les actions spécifiques des contrôleurs en fonction des URLs définies. Ce cours couvre différents aspects de la configuration et de la gestion des routes dans les applications Symfony.

## Introduction au Routage

Lorsqu'une application reçoit une requête, Symfony détermine quelle action de contrôleur exécuter en fonction de l'URL demandée. La configuration du routage spécifie comment les URLs sont mappées vers les actions spécifiques de votre code.

## Création des Routes

Les routes peuvent être configurées à l'aide de différents formats tels que YAML, XML, fichiers PHP ou attributs. Symfony recommande l'utilisation d'attributs en raison de leur simplicité et de leur intégration avec les classes de contrôleurs.

##  Création des Routes avec des Attributs

À partir de PHP 8 et supérieur, Symfony permet de définir les routes directement en tant qu'attributs au sein des classes de contrôleur. Cette approche consolide les définitions de routes avec la logique des contrôleurs, améliorant ainsi la lisibilité et la maintenabilité du code.

```php
// Exemple de définition d'une route à l'aide d'attributs PHP
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class BlogController extends AbstractController
{
    #[Route('/blog', name: 'blog_list')]
    public function list(): Response
    {
        // Logique du contrôleur
    }
}
```

## Configuration Initiale : attribute - par défaut c'est déjà en place 

Pour activer le routage basé sur les attributs, configurez Symfony pour reconnaître les routes définies dans des espaces de noms et des répertoires spécifiques en utilisant des fichiers de configuration comme `attributes.yaml`.

Vérifiez la configuration.

```yaml
# config/routes/attributes.yaml
controllers:
    resource:
        path: ../../src/Controller/
        namespace: App\Controller
    type: attribute
```

## Routage avec Différents Formats

Les routes peuvent également être définies dans des fichiers séparés YAML, XML ou PHP. Chaque format offre des avantages en termes de flexibilité et de maintenabilité, adaptés aux exigences spécifiques du projet.

## Correspondance des Méthodes HTTP

Les routes, par défaut, répondent à toutes les méthodes HTTP (GET, POST, etc.). Utilisez l'option `methods` pour restreindre les routes à des verbes HTTP spécifiques, renforçant la sécurité et respectant les principes RESTful.

## Débogage des Routes

Symfony propose des commandes telles que `debug:router` et `router:match` pour résoudre et vérifier les configurations de routage. Ces outils aident à identifier les problèmes de routage et à garantir que les actions des contrôleurs appropriés sont invoquées pour des URLs spécifiques.

## Fonctionnalités de Routage Avancées

Symfony prend en charge des fonctionnalités de routage avancées telles que :

- **Validation des Paramètres** : Définir des contraintes pour les paramètres de route à l'aide d'expressions régulières pour assurer une correspondance précise des routes.
- **Paramètres Optionnels** : Spécifier des valeurs par défaut pour les paramètres de route afin de gérer élégamment les segments d'URL optionnels.
- **Conversion des Paramètres** : Convertir automatiquement les paramètres de route en objets correspondants (par exemple, des entités de base de données) en utilisant des convertisseurs de paramètres.
- **Paramètre de Priorité** : Contrôler l'ordre d'évaluation des routes en définissant une priorité, assurant que certaines routes ont la priorité sur d'autres.

## Paramètres Spéciaux et Fonctionnalités Supplémentaires

Symfony inclut des paramètres spéciaux tels que `_controller`, `_format` et `_locale` pour la personnalisation du routage. Ces paramètres simplifient les définitions de routes et améliorent la flexibilité de l'application.

### Exemple 1: Définition d'une Route avec des Attributs

Supposons que nous voulons créer une route pour afficher la liste des formateurs.

1. **Création du Contrôleur**

```php
// src/Controller/TrainerController.php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use App\Entity\Trainer; // Import de l'entité Trainer

class TrainerController extends AbstractController
{
    #[Route('/trainers', name: 'trainer_list')]
    public function list(): Response
    {
        // Récupération de la liste des formateurs depuis la base de données
        $trainers = $this->getDoctrine()->getRepository(Trainer::class)->findAll();

        return $this->render('trainer/list.html.twig', [
            'trainers' => $trainers
        ]);
    }
}
```

Ici, la route `/trainers` est définie directement au-dessus de la méthode `list()` à l'aide de l'attribut `#[Route]`. Cette action récupère tous les formateurs depuis la base de données et les passe au modèle Twig pour l'affichage.


### Validation des Paramètres de Route

Supposons que nous voulons une autre route pour afficher les détails d'un formateur spécifique en fonction de son ID.

```yaml
# config/routes.yaml
trainer_show:
    path: /trainer/{id}
    controller: App\Controller\TrainerController::show
    requirements:
        id: '\d+'
```

Ici, `{id}` est un paramètre de route qui doit correspondre au motif spécifié `\d+`, qui autorise uniquement les chiffres.

## Exercice route parametrique uniquement dans HomeController

Mettez en pratique cette route dans notre projet fil rouge, sans re-créer de contrôleur, **dans le contrôleur HomeController**.

### Partie 1

1. Affichez une route boujour paramétrique, si le paramètre de votre route vaut 1 affichez "Bonjour" si il vaut 2, affichez "Hello" 
 routes possible :  `bonjour/1`, `bonjour/2`
2. Créez la méthode qui affiche un trainer.
3. Mettez en place la route et son template spécifique pour afficher le détails d'un formateur.
   
### Partie 2

1. Seules les "pages" dont l'id = 1 ou 2 peuvent s'afficher, gérez cette condition dans validation des paramètre.
2. Créez une page 404, considérez le code suivant à mettre dans le fichier routes.yaml
```yaml
error_404:
    path: /{catchall}
    controller: 'App\Controller\ErrorController::error404'
    requirements:
        catchall: '.*'
```
1. Si on ne renseigne pas une valeur pour le paramètre id dans la route. Utilisez encore le fichier routes.yaml pour afficher la page une défaut.
```yaml
trainer_show:
    path: /trainer/{id}
    controller: App\Controller\HomeController::show
    defaults:
        id: 1
    requirements:
        id: '[1,2]'
```

### Partie 3

1. Créez maintenant les liens pour afficher la page d'accueil.
2. Sous chaque cards de formateur un lien lire la suite permet d'afficher la page du formateur.

#### Indications utilisez la fonction path de Symfony dans Twig

La fonction path dans Twig permet de créer les urls en utilisant la route nommée.

```twig
{{ path('trainer_home') }} == /
{{ path('trainer_show', {id: trainer.id}) }} == /trainer/1
```

### Utilisation de Paramètres Optionnels - pagination

Parfois, nous voulons que certains paramètres de route soient optionnels. Par exemple, pour afficher une liste de formateurs paginée où la page est optionnelle et a une valeur par défaut.

```yaml
# config/routes.yaml
trainer_list:
    path: /trainers/{page}
    controller: App\Controller\TrainerController::list
    defaults:
        page: 1
    requirements:
        page: '\d+'
```

Dans cet exemple, `{page}` est un paramètre de route qui peut être un nombre entier (`\d+`). Si l'utilisateur ne spécifie pas de numéro de page, il sera automatiquement redirigé vers la page 1.

### Conversion des Paramètres en Objets

Imaginons que chaque formateur est représenté par un objet `Trainer` en base de données. Nous voulons que notre route charge automatiquement l'objet `Trainer` correspondant en fonction de l'ID fourni.

```php
// src/Controller/TrainerController.php
namespace App\Controller;

use App\Entity\Trainer;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class TrainerController extends AbstractController
{
    #[Route('/trainer/{id}', name: 'trainer_show')]
    public function show(Trainer $trainer): Response
    {
        // $trainer est l'objet représentant le formateur correspondant à l'ID
        return $this->render('trainer/show.html.twig', [
            'trainer' => $trainer
        ]);
    }
}
```

Symfony utilise un convertisseur de paramètres pour charger automatiquement l'objet `Trainer` dont l'ID correspond à celui de l'URL.

Evidemment il y a beaucoup d'autre chose à apprendre sur les routes [creating routes](https://symfony.com/doc/current/routing.html#creating-routes)