# Utilisation de l'EntityValueResolver dans Symfony

## Introduction
L'EntityValueResolver est une fonctionnalité de Symfony qui permet de simplifier la récupération automatique des entités à partir des paramètres de route. Cela permet de réduire le code nécessaire pour effectuer des requêtes et de gérer les entités dans les contrôleurs.

## Pré-requis
Avant de commencer, assurez-vous d'avoir installé et configuré Symfony et Doctrine dans votre projet.

## Exemple de contrôleur avec EntityValueResolver

Prenons l'exemple d'un contrôleur qui affiche un produit en fonction de son identifiant (`id`).

```php
// src/Controller/ProductController.php
namespace App\Controller;

use App\Entity\Product;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class ProductController extends AbstractController
{
    #[Route('/product/{id}', name: 'product_show')]
    public function show(Product $product): Response
    {
        // Utilisation de l'entité Product
        return new Response('Product: ' . $product->getName());
    }
}
```

## Fonctionnement

1. **Route et Paramètre** :
   - La route `/product/{id}` contient un paramètre `id`.
   - Symfony utilise ce paramètre pour rechercher l'entité `Product` correspondante dans la base de données.

2. **Injection de l'Entité** :
   - Le paramètre `Product $product` dans la méthode `show` indique à Symfony d'injecter l'entité `Product` correspondant à l'`id` fourni dans l'URL.
   - Si le produit n'est pas trouvé, Symfony génère automatiquement une page 404.

## Désactivation de l'EntityValueResolver pour un Contrôleur

Si vous souhaitez désactiver cette fonctionnalité pour un contrôleur spécifique, vous pouvez utiliser l'attribut `MapEntity` avec l'option `disabled`.

```php
public function show(
    #[MapEntity(disabled: true)]
    Product $product
): Response {
    // L'entité Product n'est pas résolue automatiquement
}
```
