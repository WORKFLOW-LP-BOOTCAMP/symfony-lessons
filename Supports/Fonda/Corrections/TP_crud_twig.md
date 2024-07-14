# 1. Ajouter Bootstrap 5 à votre projet Symfony

Pour inclure Bootstrap 5 dans votre projet, vous pouvez utiliser le CDN dans votre fichier `base.html.twig`.

## `templates/base.html.twig`

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

# 2. Trainer Views

## `templates/trainer/list.html.twig`

```twig
{% extends 'base.html.twig' %}

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

## `templates/trainer/create.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Create Trainer</h1>
{{ form_start(form) }}
<div class="mb-3">
    {{ form_label(form.firstName, 'First Name', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.firstName, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.lastName, 'Last Name', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.lastName, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.profession, 'Profession', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.profession, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.bio, 'Bio', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.bio, { 'attr': {'class': 'form-control'} }) }}
</div>
<button type="submit" class="btn btn-primary">Save</button>
{{ form_end(form) }}
<a href="{{ path('list_trainers') }}" class="btn btn-secondary mt-3">Back to list</a>
{% endblock %}
```

## `templates/trainer/edit.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Edit Trainer</h1>
{{ form_start(form) }}
<div class="mb-3">
    {{ form_label(form.firstName, 'First Name', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.firstName, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.lastName, 'Last Name', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.lastName, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.profession, 'Profession', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.profession, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.bio, 'Bio', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.bio, { 'attr': {'class': 'form-control'} }) }}
</div>
<button type="submit" class="btn btn-primary">Save</button>
{{ form_end(form) }}
<a href="{{ path('list_trainers') }}" class="btn btn-secondary mt-3">Back to list</a>
{% endblock %}
```

## `templates/trainer/show.html.twig`

```twig
{% extends 'base.html.twig' %}

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

# 3. Article Views

## `templates/article/list.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Articles List</h1>
<a href="{{ path('create_article') }}" class="btn btn-primary mb-3">Create New Article</a>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Title</th>
            <th>Created At</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for article in articles %}
            <tr>
                <td>{{ article.title }}</td>
                <td>{{ article.createdAt|date('Y-m-d H:i:s') }}</td>
                <td>
                    <a href="{{ path('show_article', {id: article.id}) }}" class="btn btn-info btn-sm">View</a>
                    <a href="{{ path('update_article', {id: article.id}) }}" class="btn btn-warning btn-sm">Edit</a>
                    <form action="{{ path('delete_article', {id: article.id}) }}" method="post" style="display:inline;">
                        <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ article.id) }}">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

## `templates/article/create.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Create Article</h1>
{{ form_start(form) }}
<div class="mb-3">
    {{ form_label(form.title, 'Title', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.title, { 'attr':

 {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.createdAt, 'Created At', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.createdAt, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.content, 'Content', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.content, { 'attr': {'class': 'form-control'} }) }}
</div>
<button type="submit" class="btn btn-primary">Save</button>
{{ form_end(form) }}
<a href="{{ path('list_articles') }}" class="btn btn-secondary mt-3">Back to list</a>
{% endblock %}
```

## `templates/article/edit.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Edit Article</h1>
{{ form_start(form) }}
<div class="mb-3">
    {{ form_label(form.title, 'Title', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.title, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.createdAt, 'Created At', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.createdAt, { 'attr': {'class': 'form-control'} }) }}
</div>
<div class="mb-3">
    {{ form_label(form.content, 'Content', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.content, { 'attr': {'class': 'form-control'} }) }}
</div>
<button type="submit" class="btn btn-primary">Save</button>
{{ form_end(form) }}
<a href="{{ path('list_articles') }}" class="btn btn-secondary mt-3">Back to list</a>
{% endblock %}
```

## `templates/article/show.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">{{ article.title }}</h1>
<p><strong>Created At:</strong> {{ article.createdAt|date('Y-m-d H:i:s') }}</p>
<p>{{ article.content }}</p>
<a href="{{ path('list_articles') }}" class="btn btn-secondary">Back to list</a>
<a href="{{ path('update_article', {id: article.id}) }}" class="btn btn-warning">Edit</a>
<form action="{{ path('delete_article', {id: article.id}) }}" method="post" style="display:inline;">
    <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ article.id) }}">
    <button type="submit" class="btn btn-danger">Delete</button>
</form>
{% endblock %}
```

# 4. Subject Views

## `templates/subject/list.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Subjects List</h1>
<a href="{{ path('create_subject') }}" class="btn btn-primary mb-3">Create New Subject</a>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Name</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for subject in subjects %}
            <tr>
                <td>{{ subject.name }}</td>
                <td>
                    <a href="{{ path('show_subject', {id: subject.id}) }}" class="btn btn-info btn-sm">View</a>
                    <a href="{{ path('update_subject', {id: subject.id}) }}" class="btn btn-warning btn-sm">Edit</a>
                    <form action="{{ path('delete_subject', {id: subject.id}) }}" method="post" style="display:inline;">
                        <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ subject.id) }}">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

## `templates/subject/create.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Create Subject</h1>
{{ form_start(form) }}
<div class="mb-3">
    {{ form_label(form.name, 'Name', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.name, { 'attr': {'class': 'form-control'} }) }}
</div>
<button type="submit" class="btn btn-primary">Save</button>
{{ form_end(form) }}
<a href="{{ path('list_subjects') }}" class="btn btn-secondary mt-3">Back to list</a>
{% endblock %}
```

## `templates/subject/edit.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">Edit Subject</h1>
{{ form_start(form) }}
<div class="mb-3">
    {{ form_label(form.name, 'Name', { 'label_attr': {'class': 'form-label'} }) }}
    {{ form_widget(form.name, { 'attr': {'class': 'form-control'} }) }}
</div>
<button type="submit" class="btn btn-primary">Save</button>
{{ form_end(form) }}
<a href="{{ path('list_subjects') }}" class="btn btn-secondary mt-3">Back to list</a>
{% endblock %}
```

## `templates/subject/show.html.twig`

```twig
{% extends 'base.html.twig' %}

{% block body %}
<h1 class="mb-4">{{ subject.name }}</h1>
<a href="{{ path('list_subjects') }}" class="btn btn-secondary">Back to list</a>
<a href="{{ path('update_subject', {id: subject.id}) }}" class="btn btn-warning">Edit</a>
<form action="{{ path('delete_subject', {id: subject.id}) }}" method="post" style="display:inline;">
    <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ subject.id) }}">
    <button type="submit" class="btn btn-danger">Delete</button>
</form>
{% endblock %}
```

# 5. Conclusion

Avec ces ajustements, vos vues Twig utilisent désormais Bootstrap 5 pour un meilleur rendu visuel. Vous pouvez maintenant bénéficier de l'apparence élégante et des fonctionnalités de Bootstrap dans votre application Symfony. Bon codage !