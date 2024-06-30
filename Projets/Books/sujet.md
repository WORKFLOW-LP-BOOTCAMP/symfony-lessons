# Brief du Projet - Plateforme de Vente de Livres d'Occasion

Pour le dossier voyez les indications à la fin du document.

#### Objectif

Développer une plateforme en ligne pour la vente de livres d'occasion, offrant une expérience utilisateur fluide et sécurisée, ainsi qu'une gestion efficace des transactions et des stocks.

#### Technologies Requises

- Symfony 7 pour le framework PHP
- PostgreSQL pour la base de données

#### Fonctionnalités Principales

1. **Inscription et Authentification**
   - Permettre aux utilisateurs de s'inscrire, de se connecter et de gérer leur profil.
   - Intégration de l'authentification sécurisée avec Symfony 7.

2. **Gestion des Livres**
   - Ajout, modification et suppression de livres par les utilisateurs et les administrateurs.
   - Chaque livre doit inclure des détails tels que le titre, l'auteur, la catégorie, l'état du livre (comme neuf, bon état, usé), le prix, et des images.

3. **Recherche et Filtrage**
   - Moteur de recherche permettant aux utilisateurs de trouver des livres par titre, auteur, catégorie, état, etc.
   - Filtrage par prix, catégorie, état du livre, etc.

4. **Panier d'Achat**
   - Fonctionnalité de panier permettant aux utilisateurs d'ajouter des livres et de passer à la commande.
   - Gestion des commandes avec état (en attente, payé, expédié, reçu).

5. **Système de Paiement**
   - Intégration d'un système de paiement sécurisé pour le traitement des transactions.
   - Utilisation de services comme Stripe, PayPal, ou autre selon exigences de sécurité et de fonctionnalité.

6. **Gestion des Utilisateurs et des Administrateurs**
   - Gestion des rôles et des permissions avec Symfony 7.
   - Tableau de bord administrateur pour gérer les utilisateurs, les livres, les commandes, etc.

7. **Gestion des Commentaires et Évaluations**
   - Possibilité pour les utilisateurs de laisser des commentaires et des évaluations sur les livres achetés.

8. **Notifications**
   - Système de notifications pour informer les utilisateurs sur les commandes, les mises à jour de profil, etc.

9. **Performance et Sécurité**
   - Optimisation des performances avec Symfony 7 et PostgreSQL pour assurer une expérience utilisateur rapide et fiable.
   - Sécurisation des données utilisateur, des transactions et des interactions sur la plateforme.

#### Contraintes Techniques

- Utilisation obligatoire de Symfony 7 pour le back-end.
- Utilisation de PostgreSQL comme système de gestion de base de données.
- Respect des bonnes pratiques de développement et des standards de sécurité.

#### Livrables Attendus

- Code source complet du projet avec documentation détaillée sur l'installation, la configuration et l'utilisation.
- Déploiement de l'application sur un serveur de test pour la validation des fonctionnalités, alwaysdata, pour le projet version gratuite.

#### Calendrier
- **Phase de Planification et Conception** : 0.5 semaines
- **Phase de Développement** : 1.5 semaines
- **Phase de Test et Correction** : 0.5 semaines
- **Déploiement et Finalisation** : 0.5 semaine

#### Équipe Impliquée

- Concepteur Développeur Symfony 7 : 1 personne
- Testeur : 1 personne
- Chef de Projet : Supervision et coordination

Ce projet peut-être fait également seul.

## Indications et aides

- [UML et MERISE](./docs/Data.md)
- [useCase exemple](./docs/useCase.md)
- [Plan de tests](./docs/plantests.md)
- [dossier de soutenance](./docs/dossier.md)
- [exemple de charte graphique](./docs/charte-graphique.md)