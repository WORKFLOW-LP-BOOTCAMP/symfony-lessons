# CRUD - Trainer

Avant de commencer créer un lien dans le menu principal vers tous les articles. 

## 1. Créer les Entités

Déjà vu dans le cours.

## 2. Configurer les Contrôleurs

### TrainerController

Nous allons créer les méthodes suivantes dans notre contrôleur.

1. listTrainers
    *Sur cette pagae afficher tous les trainers avec leurs données ainsi que 3 boutons cliquable pour respectivement voir le détails d'un trainer, éditer un trainer et le supprimer.*
2. createTrainer
   *Mettez en place le bootstrap dans la configuration dans twig*
3. showTrainer
4. updateTrainer
5. deleteTrainer

```php
// src/Controller/TrainerController.php
namespace App\Controller;

use App\Entity\Trainer;
use App\Form\TrainerType;
use App\Repository\TrainerRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class TrainerController extends AbstractController
{
    #[Route('/trainers', name: 'list_trainers')]
    public function listTrainers(TrainerRepository $trainerRepository): Response
    {
        $trainers = $trainerRepository->findAll();
        return $this->render('admin/trainer/list.html.twig', [
            'trainers' => $trainers,
        ]);
    }

    #[Route('/trainers/new', name: 'create_trainer')]
    public function createTrainer(Request $request, EntityManagerInterface $em): Response
    {
        $trainer = new Trainer();
        $form = $this->createForm(TrainerType::class, $trainer);
        
        $form->handleRequest($request);
        if ($form->isSubmitted() && $form->isValid()) {
            $em->persist($trainer);
            $em->flush();

            return $this->redirectToRoute('list_trainers');
        }

        return $this->render('admin/trainer/create.html.twig', [
            'form' => $form->createView(),
        ]);
    }

    #[Route('/trainers/{id}', name: 'show_trainer')]
    public function showTrainer(Trainer $trainer): Response
    {
        return $this->render('admin/trainer/show.html.twig', [
            'trainer' => $trainer,
        ]);
    }

    #[Route('/trainers/{id}/edit', name: 'update_trainer')]
    public function updateTrainer(Request $request, Trainer $trainer, EntityManagerInterface $em): Response
    {
        $form = $this->createForm(TrainerType::class, $trainer);

        $form->handleRequest($request);
        if ($form->isSubmitted() && $form->isValid()) {
            $em->flush();

            return $this->redirectToRoute('list_trainers');
        }

        return $this->render('admin/trainer/edit.html.twig', [
            'form' => $form->createView(),
            'trainer' => $trainer,
        ]);
    }

    #[Route('/trainers/{id}/delete', name: 'delete_trainer', methods: ['POST'])]
    public function deleteTrainer(Request $request, Trainer $trainer, EntityManagerInterface $em): Response
    {
        if ($this->isCsrfTokenValid('delete' . $trainer->getId(), $request->request->get('_token'))) {
            $em->remove($trainer);
            $em->flush();
        }

        return $this->redirectToRoute('list_trainers');
    }
}
```

## 3. Créer les Formulaires

### TrainerType

```php
// src/Form/TrainerType.php
namespace App\Form;

use App\Entity\Trainer;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class TrainerType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('firstName', TextType::class)
            ->add('lastName', TextType::class)
            ->add('profession', TextType::class)
            ->add('bio', TextareaType::class);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Trainer::class,
        ]);
    }
}
```

## 4. Créer les Vues Twig

### Trainer Views

- `templates/admin.html.twig`

```twig
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My Symfony App{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css">
    {% block stylesheets %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">My Symfony App</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ path('list_trainers') }}">Trainers</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ path('list_articles') }}">Articles</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ path('list_subjects') }}">Subjects</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block body %}{% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
    {% block javascripts %}{% endblock %}
</body>
</html>
```

- `templates/trainer/list.html.twig`

- `templates/trainer/create.html.twig`

- `templates/trainer/edit.html.twig`

- `templates/trainer/show.html.twig`
