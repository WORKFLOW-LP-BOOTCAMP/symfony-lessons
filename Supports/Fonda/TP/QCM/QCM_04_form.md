# QCM 03 formulaire

## 1. Quel composant de Symfony facilite la gestion des formulaires HTML ?
- A) `symfony/form`
- B) `symfony/form-builder`
- C) `symfony/form-handling`
- D) Composant de formulaire robuste

## 2. Quelle commande Composer est utilisée pour installer les composants nécessaires pour les formulaires dans Symfony 7 ?
- A) `composer require symfony/form-builder symfony/form-handling`
- B) `composer require symfony/form`
- C) `composer require symfony/form symfony/validator`
- D) `composer require symfony/form-builder symfony/validator`

## 3. Où doit-on définir les formulaires dans Symfony 7 ?
- A) Dans le fichier `config/forms.yaml`
- B) Dans le fichier `src/FormBuilder/`
- C) Dans des classes dédiées
- D) Directement dans les contrôleurs

## 4. Quelle méthode de Symfony 7 permet d'afficher un formulaire dans une vue Twig ?
- A) `form_show(form)`
- B) `render_form(form)`
- C) `{{ form(form) }}`
- D) `print_form(form)`

## 5. Comment peut-on gérer la soumission d'un formulaire dans un contrôleur Symfony ?
- A) Avec `form_handleSubmit()`
- B) En appelant `handleRequest()` sur le formulaire
- C) En utilisant `form_submit()`
- D) En utilisant `process_form()`

## 6. Quelle est la fonction de la classe `TrainerType` dans Symfony ?
- A) Afficher les détails d'un formateur
- B) Valider les données du formateur
- C) Définir la structure et les options du formulaire pour l'entité Trainer
- D) Gérer la logique métier du formateur

## 7. Quelle option permet de spécifier la classe de données associée à un formulaire dans Symfony ?
- A) `form_data_class`
- B) `data_class`
- C) `class_data`
- D) `form_class`

## 8. Comment peut-on personnaliser le rendu d'un formulaire avec un thème spécifique comme Bootstrap 5 dans Symfony 7 ?
- A) En modifiant le fichier `form_themes.yml`
- B) En ajoutant un thème dans le fichier `config/packages/twig.yaml` avec `form_themes`
- C) En utilisant des annotations dans le fichier de formulaire
- D) En modifiant directement les classes CSS du formulaire

## 9. Quelle commande permet de créer une nouvelle entité de type formulaire dans Symfony 7 ?
- A) `php bin/console make:form`
- B) `php bin/console create:form`
- C) `php bin/console form:create`
- D) `php bin/console generate:form`

## 10. Quelle configuration dans `config/packages/twig.yaml` est nécessaire pour activer la validation automatique des entités dans les formulaires ?
- A) `auto_mapping: true`
- B) `validation: auto_mapping`
- C) `auto_mapping: []`
- D) `auto_mapping: true`