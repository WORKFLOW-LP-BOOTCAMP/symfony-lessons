# Projet Dev Trainer - partie 1 

## Trainer - sans base de données

Dans un nouveau projet dev-trainer, vous allez créer la home page.

1. Réinstallez un projet SF trainer sur votre machine avec la configuration que nous avons faite dans le cours.

1. Introduction au projet fil rouge.  

Vous allez réaliser une page princiaple sur deux colonnes avec le  **Bootstrap** CSS, aidez vous des wireframe ci-après.

Bien sûr vous allez utiliser Twig pour réaliser l'intégration de cette première. Vous pouvez vous aider de la documentation officiel, Twig et Symfony.

1. Dans le cas où vous voulez changer de Framework CSS voyez la documentation en ligne : [assetmapper](https://symfony.com/doc/current/frontend/asset_mapper.html)

2. Nous allons construire l'arborescence cette semaine dans notre projet fil rouge.

```mermaid
graph TD
  A[Home] -->|Contenu Home| B(Trainers)
  A -->|Contenu Home| D(Contact)
  B -->|Liste des trainers| EE(Bob)
  B -->|Liste des trainers| FF(Alan)
  B -->|Liste des trainers| GG(John)
  B -->|Liste des trainers| HH(Alice)
```

🚧 

1. Créez le controller Home (fournit)

### Détails de la page à réaliser, pour l'instant uniquement la page home

1. Home (page d'accueil) :
  1. Elle présente les formateurs sous le titre du site.
  1. Elle répertoriera les derniers articles rédigés par les formateurs colonne de droite sous la présentation des formateurs.

Utilisez le dataset suivant : 
[dataset](./Data/trainers.php) pour afficher les données en page d'accueil.

### Wireframe

1. home page

![homepage](../images/homewireframe.png)

Vous pouvez vous aider de cette page pour réaliser l'intégration CSS : [home page](../Corrections/Models-pages/index.html)


## Indications

Dans le contrôleur HomeController créer une méthode privée data comme suit pour traiter les données dans la méthode index pour la page d'accueil.

```php
// Dans le controller HomeController 
// ...
  private function data(): array
      {

          return [
              "trainers" => [
                  [
                      "firstName" => "Antoine",
                      "lastName" => "L",
                      "profession" => "Professor Symfony",
                      "bio" => "Antoine L is a certified Symfony coach with over 10 years of experience.",
                      "articles" => [
                          [
                              "title" => "The Benefits of Morning Exercise",
                              "date" => "Nov 11",
                              "content" => "Exercising in the morning can boost your metabolism and energy levels throughout the day."
                          ],
                          [
                              "title" => "Healthy Eating Tips",
                              "date" => "Nov 10",
                              "content" => "Eating a balanced diet is crucial for maintaining good health and fitness."
                          ]
                      ]
                  ],
                  [
                      "firstName" => "Aurélien",
                      "lastName" => "S",
                      "profession" => "Professor React",
                      "bio" => "Aurélien has been teaching yoga for over 8 years and specializes in Vinyasa and Hatha yoga.",
                      "articles" => [
                          [
                              "title" => "The Power of Meditation",
                              "date" => "Nov 12",
                              "content" => "Meditation can help reduce stress and improve overall well-being."
                          ],
                          [
                              "title" => "Yoga for Beginners",
                              "date" => "Nov 5",
                              "content" => "Starting a yoga practice can be intimidating, but with these tips, you can get started with confidence."
                          ]
                      ]
                  ]
              ]
          ];
      }
  ```
