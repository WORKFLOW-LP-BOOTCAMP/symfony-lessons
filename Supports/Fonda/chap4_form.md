# Cours sur la gestion des formulaires avec Symfony 7

## Introduction

Symfony 7 facilite la gestion des formulaires HTML avec son composant de formulaire robuste, utilisant les nouveaux attributs #[...] pour simplifier la définition des formulaires.

## Installation

Pour utiliser les formulaires avec Symfony 7, assurez-vous d'installer les composants nécessaires via Composer :

```bash
composer require symfony/form symfony/validator
```

Pour validator voyez la suite du cours dans ce chapitre.

## Workflow recommandé pour commencer

1. **Création du formulaire** : Définissez les formulaires dans des classes dédiées.
   
2. **Affichage du formulaire** : Intégrez le formulaire dans vos vues Twig pour l'affichage.
   
3. **Traitement du formulaire** : Validez les données, traitez-les et persistez-les si nécessaire.

## Exemple : Application de gestion des formateurs

### Entité Trainer
```php
// src/Entity/Trainer.php
namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
class Trainer
{
    #[ORM\Id]
    #[ORM\GeneratedValue(strategy: "AUTO")]
    #[ORM\Column(type: "integer")]
    private int $id;

    #[ORM\Column(type: "string")]
    private string $name;

    #[ORM\Column(type: "string")]
    private string $profession;

    // Getters and setters
}
```

### Création de formulaires dans les contrôleurs
```php
// src/Controller/TrainerController.php
namespace App\Controller;

use App\Entity\Trainer;
use App\Form\Type\TrainerType;
use Doctrine\Persistence\ManagerRegistry;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/trainer')]
class TrainerController extends AbstractController
{
    #[Route('/new', name: 'trainer_new', methods: ['GET', 'POST'])]
    public function new(Request $request, ManagerRegistry $doctrine): Response
    {
        $trainer = new Trainer();
        $form = $this->createForm(TrainerType::class, $trainer);

        // Gestion de la soumission du formulaire
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            // Enregistrer le formateur dans la base de données
            $entityManager = $doctrine->getManager();
            $entityManager->persist($trainer);
            $entityManager->flush();

            return $this->redirectToRoute('trainer_success');
        }

        return $this->render('trainer/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
```

### Classe de formulaire TrainerType

```php
// src/Form/Type/TrainerType.php
namespace App\Form\Type;

use App\Entity\Trainer;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class TrainerType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('name')
            ->add('profession');
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Trainer::class,
        ]);
    }
}
```

### Affichage des formulaires

Utilisez le Bootstrap, vérifiez que ce dernier est bien installé avec AssetMapper, puis dans le fichier de configuration de twig `config/packages/twig.yaml`, ajoutez la ligne suivante :

```yaml
twig:
    file_name_pattern: '*.twig'
    form_themes:
        - 'bootstrap_5_layout.html.twig'
```

Le template twig devrait ressembler à ce qui suit

```twig
{# templates/trainer/new.html.twig #}
{{ form_start(form) }}
{{ form_widget(form) }}
{{ form_end(form) }}
```

### Traitement des formulaires

Le contrôleur peut traiter la soumission du formulaire comme suit :

```php
// Extrait de TrainerController.php

if ($form->isSubmitted() && $form->isValid()) {
    $trainer = $form->getData();
    // Enregistrer le formateur dans la base de données
    $entityManager = $this->getDoctrine()->getManager();
    $entityManager->persist($trainer);
    $entityManager->flush();

    return $this->redirectToRoute('trainer_success');
}
```

## Validation des formulaires - cas où l'on ne souhaite pas avoir la validation activée

Si lors du développement vous ne souhaitez pas avoir la validation dans vos formulaire considérez le code suivant 

```php
{{ form_start(form, {'attr': {'novalidate': 'novalidate'}}) }}
    {{ form_widget(form) }}
{{ form_end(form) }}
```

Utilisez la validation avec les attributs. Dans le fichier `config/packages/twig.yaml` décommentez les lignes suivantes auto_mapping.

```yaml
framework:
    validation:
        # Enables validator auto-mapping support.
        # For instance, basic validation constraints will be inferred from Doctrine's metadata.
        auto_mapping:
            App\Entity\: []
```

Puis dans votre contrôleur, maintenant, utilisez les attributs de validation, voyez l'exemple qui suit:

```php
use Symfony\Component\Validator\Constraints as Assert;

// ... Dans l'entité Trainer

#[Assert\LessThan(value :6, message: 'valeur trop grande' )]
#[Assert\GreaterThan(value :0, message: 'valeur trop petite' )]
#[ORM\Column(type: Types::SMALLINT, nullable: true)]
private ?int $stars = null;
```

### Validation des formulaires

Dans la section précédente, vous avez appris comment un formulaire peut être soumis avec des données valides ou invalides. En Symfony, la question n'est pas de savoir si le "formulaire" est valide, mais si l'objet sous-jacent (`$task` dans cet exemple) est valide après que le formulaire a appliqué les données soumises. Appeler `$form->isValid()` est un raccourci qui demande à l'objet `$task` s'il contient des données valides.

Avant d'utiliser la validation, ajoutez son support dans votre application :

```bash
composer require symfony/validator
```

La validation se fait en ajoutant un ensemble de règles, appelées contraintes de validation, à une classe. Vous pouvez les ajouter soit à la classe de l'entité, soit en utilisant l'option constraints des types de formulaire.

Pour voir la première approche - ajouter des contraintes à l'entité - en action, ajoutez les contraintes de validation pour que le champ task ne puisse pas être vide, et que le champ dueDate ne puisse pas être vide et doit être un objet DateTimeImmutable valide.

```php
// src/Entity/Task.php
namespace App\Entity;

use Symfony\Component\Validator\Constraints as Assert;

class Task
{
    #[Assert\NotBlank]
    public string $task;

    #[Assert\NotBlank]
    #[Assert\Type(\DateTimeInterface::class)]
    protected \DateTimeInterface $dueDate;
}
```
