# Cours sur la gestion des formulaires avec Symfony

## Introduction

Créer et traiter des formulaires HTML est une tâche complexe et répétitive. 

Symfony simplifie cette tâche avec une puissante fonctionnalité de formulaire offrant un ensemble complet de fonctionnalités, allant de la génération des champs de formulaire HTML à la validation des données soumises et leur mappage vers des objets.

## Installation

Pour installer la fonctionnalité de formulaire dans un projet utilisant **Symfony Flex**, exécutez la commande suivante :

```bash
composer require symfony/form

# ainsi que des maker dev utils
composer require --dev symfony/maker-bundle

# debug
php bin/console debug:form

composer require symfony/validator
```

## Workflow recommandé pour commencer

1. **Construire le formulaire** : Dans un contrôleur Symfony ou une classe dédiée.
   
2. **Afficher le formulaire** : Dans un template pour que l'utilisateur puisse le remplir et le soumettre.
   
3. **Traiter le formulaire** : Valider les données soumises, les transformer en données PHP et effectuer des actions (par exemple, les enregistrer dans une base de données).

## Exemple : Application de liste de tâches

### Entité Task
```php
// src/Entity/Task.php
namespace App\Entity;

class Task
{
    protected string $task;
    protected ?\DateTimeInterface $dueDate;

    public function getTask(): string
    {
        return $this->task;
    }

    public function setTask(string $task): void
    {
        $this->task = $task;
    }

    public function getDueDate(): ?\DateTimeInterface
    {
        return $this->dueDate;
    }

    public function setDueDate(?\DateTimeInterface $dueDate): void
    {
        $this->dueDate = $dueDate;
    }
}
```

### Création de formulaires dans les contrôleurs
```php
// src/Controller/TaskController.php
namespace App\Controller;

use App\Entity\Task;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Form\Extension\Core\Type\DateType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class TaskController extends AbstractController
{
    public function new(Request $request): Response
    {
        $task = new Task();
        $task->setTask('Write a blog post');
        $task->setDueDate(new \DateTimeImmutable('tomorrow'));

        $form = $this->createFormBuilder($task)
            ->add('task', TextType::class)
            ->add('dueDate', DateType::class)
            ->add('save', SubmitType::class, ['label' => 'Create Task'])
            ->getForm();

        // ...
    }
}
```

### Classes de formulaire - plus séparé et donc une meilleur approche

Pour minimiser la logique dans les contrôleurs, il est recommandé de créer des classes de formulaire réutilisables.

```php
// src/Form/Type/TaskType.php
namespace App\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\DateType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class TaskType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('task', TextType::class)
            ->add('dueDate', DateType::class)
            ->add('save', SubmitType::class);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Task::class,
        ]);
    }
}
```

### Affichage des formulaires
```php
// src/Controller/TaskController.php
namespace App\Controller;

use App\Entity\Task;
use App\Form\Type\TaskType;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class TaskController extends AbstractController
{
    public function new(Request $request): Response
    {
        $task = new Task();
        $form = $this->createForm(TaskType::class, $task);

        return $this->render('task/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
```

Template Twig :

```twig
{# templates/task/new.html.twig #}
{{ form_start(form) }}
{{ form_widget(form) }}
{{ form_end(form) }}
```

## Faite à ce stade le TP suivant 



### Traitement des formulaires
```php
// src/Controller/TaskController.php

use Symfony\Component\HttpFoundation\Request;

class TaskController extends AbstractController
{
    public function new(Request $request): Response
    {
        $task = new Task();
        $form = $this->createForm(TaskType::class, $task);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();
            // Enregistrer la tâche dans la base de données
            return $this->redirectToRoute('task_success');
        }

        return $this->render('task/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
```

## Validation des formulaires
Pour valider les données d'un formulaire, ajoutez des contraintes de validation à la classe de l'entité.

```yaml
# config/validator/validation.yaml
App\Entity\Task:
    properties:
        task:
            - NotBlank: ~
        dueDate:
            - NotBlank: ~
            - Type: \DateTimeInterface
```

## Options de formulaire

Il est possible de passer des options personnalisées aux formulaires et de les utiliser dans les classes de formulaire.

```php
// src/Controller/TaskController.php
namespace App\Controller;

use App\Form\Type\TaskType;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class TaskController extends AbstractController
{
    public function new(): Response
    {
        $task = new Task();
        $form = $this->createForm(TaskType::class, $task, [
            'require_due_date' => true,
        ]);

        return $this->render('task/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
```

```php
// src/Form/Type/TaskType.php
namespace App\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\DateType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class TaskType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('task')
            ->add('dueDate', DateType::class, [
                'required' => $options['require_due_date'],
            ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Task::class,
            'require_due_date' => false,
        ]);
        $resolver->setAllowedTypes('require_due_date', 'bool');
    }
}
```
