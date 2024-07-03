# TP Modèle et données avec Doctrine dans Symfony

1. Créez des données pour Trainer et Article (Fixtures)

2. Exercice affichez les données, les trainers uniquement pour l'instant

Pour récupérer nos données, nous devons indiquer le namespace du repository avec le mot-clé `use`, utiliser le repository et lui appliquer la méthode `findAll()` pour obtenir une liste de nos données.

```php
<?php

namespace App\Controller;

// Namespace de TrainersRepository
use App\Repository\TrainersRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class TrainersController extends AbstractController
{
    #[Route('/trainers', name: 'app_trainers')]
    public function index(TrainersRepository $trainersRepository): Response
    {
        $trainers = $trainersRepository->findAll();

        return $this->render('trainers/index.html.twig', [
            'trainers' => $trainers,
        ]);
    }
}
```

1. Implémentez les relations

Si ce n'est pas déjà fait créez les relations entre les deux entités.

Hydratez cette table avec les DataFixtures ( même fichier ).

Rappels des commandes :

```bash
# création des migrations
php bin/console make:migration
# update database
php bin/console doctrine:migrations:migrate

# vérifiez que les données sont bien dans les tables
php bin/console dbal:run-sql 'SELECT * FROM trainer'
```

1. ChatGPT

Maintenant que vous avez le modèle de données créer d'autres formateurs en utilisant ChatGPT pour les générer.

1. Modifier une Entity Trainer existante

Modifiez l'entité Trainer en ajoutant le champs **stars** (notation sur 5) de type **numérique**.

- stars type numérique

Hydratez cette table avec les DataFixtures ( même fichier ).

1. Affichez les données d'exemple dans un nouveau contrôleur

   1. Créez le contrôleur TrainerController et créez les routes pour afficher : 
      1. Tous les professeurs
      2. Un professeur en fonction de son id (FK) vous pouvez utiliser l'injection de dépendance. 
    ```php
        //use Doctrine\ORM\EntityManagerInterface;
        public function index(EntityManagerInterface $em): Response
        {
            // ...
        }
    ```
2. Créer une Relation Many-to-Many entre Trainer et Subject

Pour illustrer une relation Many-to-Many avec Doctrine, nous allons ajouter une nouvelle entité `Subject` et établir une relation Many-to-Many avec l'entité `Trainer`. Chaque formateur peut enseigner plusieurs matières, et chaque matière peut être enseignée par plusieurs formateurs.

   1. Créez l'entité `Subject` en utilisant la commande Symfony suivante :
    ```shell
    php bin/console make:entity Subject
    ```

   2. Ajoutez le champ `name` de type `string` à l'entité `Subject`.


1. Ajoutez une relation Many-to-Many dans l'entité `Trainer` pour l'associer avec l'entité `Subject`. Utilisez la commande :
    ```shell
    php bin/console make:entity Trainer
    ```

2. Ajoutez le champ `subjects` dans l'entité `Trainer`.

3. Générez une nouvelle migration pour mettre à jour la base de données avec les nouvelles relations :
    ```shell
    php bin/console make:migration
    ```

4. Exécutez la migration :
    ```shell
    php bin/console doctrine:migrations:migrate
    ```

5. Modifiez votre fixture pour ajouter des données pour les entités `Trainer` et `Subject` ainsi que pour établir des relations Many-to-Many.

6. Chargez les fixtures pour peupler la base de données :
    ```shell
    php bin/console doctrine:fixtures:load
    ```

7. Dans la page qui affiche le détails d'un formateur afficher ces articles et les matières enseignées par le formateur.
