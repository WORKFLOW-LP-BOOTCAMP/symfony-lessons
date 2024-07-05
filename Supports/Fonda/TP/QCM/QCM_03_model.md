# QCM 03 Modèle

# Configuration et création de notre première base de données

## 1. Quel est le rôle principal de Doctrine dans Symfony ?
- A) Gérer les routes de l'application
- B) Faciliter l'interaction entre une application orientée objet et une base de données relationnelle 
- C) Configurer les services de l'application
- D) Générer des fichiers de configuration

## 2. Quelle commande permet d'ajouter Doctrine ORM à un projet Symfony ?
- A) `composer require symfony/doctrine-orm`
- B) `composer require symfony/orm-pack` 
- C) `composer require symfony/database`
- D) `composer require symfony/doctrine-bundle`

## 3. Quel fichier doit être configuré pour indiquer à Symfony où trouver la base de données ?
- A) `config/packages/doctrine.yaml`
- B) `config/services.yaml`
- C) `.env` 
- D) `composer.json`

## 4. Quelle commande permet de créer la base de données configurée dans Symfony ?
- A) `php bin/console doctrine:database:initialize`
- B) `php bin/console doctrine:database:setup`
- C) `php bin/console doctrine:database:create` 
- D) `php bin/console doctrine:database:generate`

## 5. Que représente une "entity" dans le contexte de Doctrine ?
- A) Une vue de l'application
- B) Une table de la base de données représentée par une classe dans l'application 
- C) Un contrôleur de l'application
- D) Un service de l'application

## 6. Quelle commande est utilisée pour créer une nouvelle entité dans Symfony ?
- A) `php bin/console generate:entity`
- B) `php bin/console create:entity`
- C) `php bin/console make:entity` 
- D) `php bin/console new:entity`

## 7. Quelle commande génère le fichier de migration contenant les requêtes SQL pour créer les tables ?
- A) `php bin/console doctrine:migrations:generate`
- B) `php bin/console make:migration` 
- C) `php bin/console doctrine:generate:migrations`
- D) `php bin/console create:migration`

## 8. Quelle commande exécute les migrations pour créer les tables dans la base de données ?
- A) `php bin/console doctrine:database:migrate`
- B) `php bin/console migrate:database`
- C) `php bin/console database:migrate`
- D) `php bin/console doctrine:migrations:migrate` 

## 9. Quelle relation ORM est utilisée pour définir qu'une entité A peut avoir plusieurs instances d'une entité B associées ?
- A) One-To-One
- B) One-To-Many 
- C) Many-To-One
- D) Many-To-Many

## 10. Quelle dépendance permet d'ajouter des données fictives dans les tables de la base de données ?
- A) `symfony/faker-bundle`
- B) `symfony/fixtures-bundle`
- C) `orm-fixtures` 
- D) `faker-php`