# Utilisation de Doctrine dans Symfony pour la Gestion des Objets

## Introduction
Doctrine est un puissant ORM (Object-Relational Mapping) pour PHP, intégré dans Symfony, qui permet de manipuler les données de la base de données sous forme d'objets PHP. Dans ce cours, nous allons aborder la mise à jour, la suppression et la requête d'objets à l'aide de Doctrine dans Symfony.

## Mise à Jour d'un Objet
Pour modifier un objet existant dans Doctrine, vous devez suivre trois étapes :

1. **Récupérer l'objet depuis Doctrine**.
2. **Modifier l'objet**.
3. **Appeler la méthode `flush()` sur l'Entity Manager**.

Exemple de mise à jour d'un produit :

```php
// src/Controller/ProductController.php
namespace App\Controller;

use App\Entity\Product;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class ProductController extends AbstractController
{
    #[Route('/product/edit/{id}', name: 'product_edit')]
    public function update(EntityManagerInterface $entityManager, int $id): Response
    {
        $product = $entityManager->getRepository(Product::class)->find($id);

        if (!$product) {
            throw $this->createNotFoundException('No product found for id '.$id);
        }

        $product->setName('New product name!');
        $entityManager->flush();

        return $this->redirectToRoute('product_show', ['id' => $product->getId()]);
    }
}
```

## Explications
1. **Récupérer l'objet** :
   ```php
   $product = $entityManager->getRepository(Product::class)->find($id);
   ```
   Utilisation de la méthode `find` pour récupérer le produit par son identifiant.

2. **Modifier l'objet** :
   ```php
   $product->setName('New product name!');
   ```
   Modification de l'attribut `name` de l'objet `Product`.

3. **Sauvegarder les modifications** :
   ```php
   $entityManager->flush();
   ```
   La méthode `flush` enregistre toutes les modifications effectuées sur les objets surveillés par Doctrine.

## Suppression d'un Objet
La suppression d'un objet suit une procédure similaire, mais nécessite un appel à la méthode `remove()` de l'Entity Manager :

```php
$entityManager->remove($product);
$entityManager->flush();
```

## Exemple de Suppression d'un Produit

```php
// src/Controller/ProductController.php
namespace App\Controller;

use App\Entity\Product;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class ProductController extends AbstractController
{
    #[Route('/product/delete/{id}', name: 'product_delete')]
    public function delete(EntityManagerInterface $entityManager, int $id): Response
    {
        $product = $entityManager->getRepository(Product::class)->find($id);

        if (!$product) {
            throw $this->createNotFoundException('No product found for id '.$id);
        }

        $entityManager->remove($product);
        $entityManager->flush();

        return $this->redirectToRoute('product_list');
    }
}
```

## Requêtes sur les Objets : Le Repository
Le Repository permet de faire des requêtes de base sur les entités sans trop d'efforts.

### Exemple de Récupération d'un Produit par son Identifiant

```php
// from inside a controller
$repository = $entityManager->getRepository(Product::class);
$product = $repository->find($id);
```

### Création d'une Méthode de Requête Complexe
Lors de la génération de votre entité avec `make:entity`, une classe `ProductRepository` est également générée. Vous pouvez y ajouter des méthodes de requêtes personnalisées.

```php
// src/Repository/ProductRepository.php
namespace App\Repository;

use App\Entity\Product;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class ProductRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Product::class);
    }

    /**
     * @return Product[]
     */
    public function findAllGreaterThanPrice(int $price): array
    {
        $entityManager = $this->getEntityManager();

        $query = $entityManager->createQuery(
            'SELECT p
            FROM App\Entity\Product p
            WHERE p.price > :price
            ORDER BY p.price ASC'
        )->setParameter('price', $price);

        return $query->getResult();
    }
}
```

## Utilisation de cette Méthode dans un Contrôleur

```php
// from inside a controller
$minPrice = 1000;
$products = $entityManager->getRepository(Product::class)->findAllGreaterThanPrice($minPrice);
```

## Utilisation du Query Builder
Le Query Builder permet d'écrire des requêtes de manière orientée objet, idéal pour les requêtes dynamiques.

```php
// src/Repository/ProductRepository.php
namespace App\Repository;

use App\Entity\Product;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class ProductRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Product::class);
    }

    public function findAllGreaterThanPrice(int $price, bool $includeUnavailableProducts = false): array
    {
        $qb = $this->createQueryBuilder('p')
            ->where('p.price > :price')
            ->setParameter('price', $price)
            ->orderBy('p.price', 'ASC');

        if (!$includeUnavailableProducts) {
            $qb->andWhere('p.available = TRUE');
        }

        return $qb->getQuery()->execute();
    }
}
```

## Requêtes SQL Directes
Si nécessaire, vous pouvez également utiliser des requêtes SQL brutes.

```php
// src/Repository/ProductRepository.php
namespace App\Repository;

use App\Entity\Product;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class ProductRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Product::class);
    }

    public function findAllGreaterThanPrice(int $price): array
    {
        $conn = $this->getEntityManager()->getConnection();

        $sql = '
            SELECT * FROM product p
            WHERE p.price > :price
            ORDER BY p.price ASC
            ';

        $stmt = $conn->prepare($sql);
        $resultSet = $stmt->executeQuery(['price' => $price]);

        return $resultSet->fetchAllAssociative();
    }
}
```

## Exercices - listes

###  Exercice 1: Récupérer tous les formateurs

### Exercice 2: Rechercher un formateur par son nom

### Exercice 3: Récupérer tous les articles

### Exercice 4: Rechercher des articles par leur titre

### Exercice 5: Récupérer les articles d'un formateur spécifique

### Exercice 6: Récupérer tous les sujets

### Exercice 7: Récupérer les articles liés à un sujet spécifique


### Exercice 8: Récupérer les formateurs qui ont écrit au moins un article

### Exercice 9: Récupérer le nombre total d'articles par sujet

### Exercice 10: Récupérer les sujets avec le nombre d'articles associés
