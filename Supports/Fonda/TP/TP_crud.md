# CRUD - Trainer

## 1. Créer les Entités

Déjà vu dans le cours.

## 2. Configurer les Contrôleurs

### TrainerController

Nous allons créer les méthodes suivantes dans notre contrôleur.

1. listTrainers
2. createTrainer
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

```twig
{% extends 'admin.html.twig' %}

{% block body %}
<h1 class="mb-4">Trainers List</h1>
<a href="{{ path('create_trainer') }}" class="btn btn-primary mb-3">Create New Trainer</a>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Profession</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for trainer in trainers %}
            <tr>
                <td>{{ trainer.firstName }}</td>
                <td>{{ trainer.lastName }}</td>
                <td>{{ trainer.profession }}</td>
                <td>
                    <a href="{{ path('show_trainer', {id: trainer.id}) }}" class="btn btn-info btn-sm">View</a>
                    <a href="{{ path('update_trainer', {id: trainer.id}) }}" class="btn btn-warning btn-sm">Edit</a>
                    <form action="{{ path('delete_trainer', {id: trainer.id}) }}" method="post" style="display:inline;">
                        <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ trainer.id) }}">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

- `templates/trainer/create.html.twig`

```twig
{% extends 'admin.html.twig' %}

{% block body %}
	<h1 class="mb-4">Edit Trainer</h1>

		{{ form_start(form, {'class' : 'row g-3'}) }}
		<div class="col-md-6">
			{{ form_label(form.firstName, 'First Name', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.firstName, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-md-4">
			{{ form_label(form.lastName, 'Last Name', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.lastName, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-2">
			{{ form_label(form.stars, 'Stars', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.stars, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-12">
			{{ form_label(form.profession, 'Profession', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.profession, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-12">
			{{ form_label(form.bio, 'Bio', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.bio, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-6">
			{{ form_label(form.subjects, 'Subjects', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.subjects, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-12">
			<button type="submit" class="btn btn-primary">Add</button>
		</div>
		{{ form_end(form) }}
		<div class="col-12">
			<a href="{{ path('list_trainers') }}" class="btn btn-secondary mt-3">Back to list</a>
		</div>
{% endblock %}

```

- `templates/trainer/edit.html.twig`

```twig
{% extends 'admin.html.twig' %}

{% block body %}
	<h1 class="mb-4">Edit Trainer</h1>

		{{ form_start(form, {'class' : 'row g-3'}) }}
		<div class="col-md-6">
			{{ form_label(form.firstName, 'First Name', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.firstName, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-md-4">
			{{ form_label(form.lastName, 'Last Name', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.lastName, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-2">
			{{ form_label(form.stars, 'Stars', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.stars, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-12">
			{{ form_label(form.profession, 'Profession', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.profession, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-12">
			{{ form_label(form.bio, 'Bio', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.bio, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-6">
			{{ form_label(form.subjects, 'Subjects', { 'label_attr': {'class': 'form-label'} }) }}
			{{ form_widget(form.subjects, { 'attr': {'class': 'form-control'} }) }}
		</div>
		<div class="col-12">
			<button type="submit" class="btn btn-primary">Add</button>
		</div>
		{{ form_end(form) }}
		<div class="col-12">
			<a href="{{ path('list_trainers') }}" class="btn btn-secondary mt-3">Back to list</a>
		</div>
{% endblock %}

```

- `templates/trainer/show.html.twig`

```twig
{% extends 'admin.html.twig' %}

{% block body %}
<h1 class="mb-4">{{ trainer.firstName }} {{ trainer.lastName }}</h1>
<p><strong>Profession:</strong> {{ trainer.profession }}</p>
<p><strong>Bio:</strong> {{ trainer.bio }}</p>
<a href="{{ path('list_trainers') }}" class="btn btn-secondary">Back to list</a>
<a href="{{ path('update_trainer', {id: trainer.id}) }}" class="btn btn-warning">Edit</a>
<form action="{{ path('delete_trainer', {id: trainer.id}) }}" method="post" style="display:inline;">
    <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ trainer.id) }}">
    <button type="submit" class="btn btn-danger">Delete</button>
</form>
{% endblock %}
```
