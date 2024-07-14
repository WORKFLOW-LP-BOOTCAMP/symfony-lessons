# Exercice : Créer une Relation Many-to-Many entre Trainer et Subject

Pour illustrer une relation Many-to-Many avec Doctrine, nous allons ajouter une nouvelle entité `Subject` et établir une relation Many-to-Many avec l'entité `Trainer`. Chaque formateur peut enseigner plusieurs matières, et chaque matière peut être enseignée par plusieurs formateurs.

## Étape 1 : Création de l'Entité Subject

Commençons par créer l'entité `Subject` en utilisant la commande Symfony :

```shell
php bin/console make:entity Subject
```

Répondez aux questions pour ajouter les champs suivants :

- `name` : string

Voici le code généré pour l'entité `Subject` :

```php
// src/Entity/Subject.php

namespace App\Entity;

use App\Repository\SubjectRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: SubjectRepository::class)]
class Subject
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $name = null;

    #[ORM\ManyToMany(targetEntity: Trainer::class, inversedBy: 'subjects')]
    private Collection $trainers;

    public function __construct()
    {
        $this->trainers = new ArrayCollection();
    }

    // Getters et setters...

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    /**
     * @return Collection<int, Trainer>
     */
    public function getTrainers(): Collection
    {
        return $this->trainers;
    }

    public function addTrainer(Trainer $trainer): self
    {
        if (!$this->trainers->contains($trainer)) {
            $this->trainers->add($trainer);
        }

        return $this;
    }

    public function removeTrainer(Trainer $trainer): self
    {
        $this->trainers->removeElement($trainer);

        return $this;
    }
}
```

## Étape 2 : Modifier l'Entité Trainer

Ajoutez une relation Many-to-Many dans l'entité `Trainer` en utilisant la commande suivante :

```shell
php bin/console make:entity Trainer
```

Ajoutez le champ `subjects` :

```php
// src/Entity/Trainer.php

// Ajoutez les use statements suivants en haut du fichier
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;

class Trainer
{
    // Ajoutez ce code dans la classe Trainer

    #[ORM\ManyToMany(targetEntity: Subject::class, mappedBy: 'trainers')]
    private Collection $subjects;

    public function __construct()
    {
        $this->subjects = new ArrayCollection();
    }

    /**
     * @return Collection<int, Subject>
     */
    public function getSubjects(): Collection
    {
        return $this->subjects;
    }

    public function addSubject(Subject $subject): self
    {
        if (!$this->subjects->contains($subject)) {
            $this->subjects->add($subject);
            $subject->addTrainer($this);
        }

        return $this;
    }

    public function removeSubject(Subject $subject): self
    {
        if ($this->subjects->removeElement($subject)) {
            $subject->removeTrainer($this);
        }

        return $this;
    }
}
```

## Étape 3 : Générer et Exécuter les Migrations

Générez une nouvelle migration pour mettre à jour la base de données avec les nouvelles relations :

```shell
php bin/console make:migration
php bin/console doctrine:migrations:migrate
```

## Étape 4 : Ajouter des Données de Test ou d'exemple avec Fixtures

Modifiez votre fixture pour ajouter des données pour les entités `Trainer` et `Subject` ainsi que pour établir des relations Many-to-Many :

```php
// src/DataFixtures/AppFixtures.php

namespace App\DataFixtures;

use App\Entity\Trainer;
use App\Entity\Subject;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use Faker\Factory;
use Faker\Generator;

class AppFixtures extends Fixture
{
    private Generator $faker;

    public function __construct()
    {
        $this->faker = Factory::create('fr_FR');
    }

    public function load(ObjectManager $manager): void
    {
        // Création de 10 sujets
        $subjects = [];
        for ($i = 0; $i < 10; $i++) {
            $subject = new Subject();
            $subject->setName($this->faker->word());
            $manager->persist($subject);
            $subjects[] = $subject;
        }

        // Création de 10 formateurs
        for ($i = 0; $i < 10; $i++) {
            $trainer = new Trainer();
            $trainer->setFirstName($this->faker->firstName());
            $trainer->setLastName($this->faker->lastName());
            $trainer->setProfession($this->faker->jobTitle());
            $trainer->setBio($this->faker->paragraph());

            // Attribution de 1 à 3 sujets à chaque formateur
            $assignedSubjects = $this->faker->randomElements($subjects, $this->faker->numberBetween(1, 3));
            foreach ($assignedSubjects as $subject) {
                $trainer->addSubject($subject);
            }

            $manager->persist($trainer);
        }

        $manager->flush();
    }
}
```

Chargez les fixtures pour peupler la base de données :

```shell
php bin/console doctrine:fixtures:load
```

## Étape 5 : Afficher les Données dans un Contrôleur

Créez un contrôleur pour afficher les formateurs et leurs sujets :

```php
// src/Controller/TrainerController.php

namespace App\Controller;

use App\Repository\TrainerRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class TrainerController extends AbstractController
{
    #[Route('/trainers', name: 'app_trainers')]
    public function index(TrainerRepository $trainerRepository): Response
    {
        $trainers = $trainerRepository->findAll();

        return $this->render('trainer/index.html.twig', [
            'trainers' => $trainers,
        ]);
    }
}
```

Créez un template Twig pour afficher les formateurs et leurs sujets :

```twig
{# templates/trainer/index.html.twig #}

{% extends 'base.html.twig' %}

{% block title %}Trainers{% endblock %}

{% block body %}
    <h1>Trainers</h1>
    <ul>
        {% for trainer in trainers %}
            <li>
                {{ trainer.firstName }} {{ trainer.lastName }} - {{ trainer.profession }}
                <ul>
                    {% for subject in trainer.subjects %}
                        <li>{{ subject.name }}</li>
                    {% endfor %}
                </ul>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
```
