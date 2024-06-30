# Exemple de useCase

```mermaid
%% Example of a technical use case diagram using Mermaid syntax
%% UseCase: Gestion Avancée des Livres

@startuml
left to right direction

actor Utilisateur as User
actor Administrateur as Admin

rectangle "Gestion Avancée des Livres" {
    usecase (Recherche de Livres) as UC1
    usecase (Gestion des Stocks) as UC2
    usecase (Gestion des Évaluations) as UC3
    usecase (Gestion des Catégories) as UC4
    usecase (Gestion des Transactions) as UC5
}

User --> UC1: Effectue une recherche
User --> UC2: Consulte les stocks
User --> UC3: Laisse une évaluation
Admin --> UC4: Modifie les catégories
Admin --> UC5: Gère les transactions

@enduml
```

### Explication du Diagramme :

1. **Acteurs** :
   - **Utilisateur (User)** : Représente les utilisateurs généraux de la plateforme.
   - **Administrateur (Admin)** : Responsable de la gestion avancée du système.

2. **Cas d'Utilisation Techniques** :
   - **Recherche de Livres (UC1)** : Permet à l'utilisateur d'effectuer des recherches avancées de livres.
   - **Gestion des Stocks (UC2)** : Donne à l'utilisateur la capacité de consulter les stocks disponibles.
   - **Gestion des Évaluations (UC3)** : Permet aux utilisateurs de laisser des évaluations et des commentaires sur les livres.
   - **Gestion des Catégories (UC4)** : Permet à l'administrateur de modifier et gérer les catégories de livres.
   - **Gestion des Transactions (UC5)** : Responsabilité de l'administrateur pour la gestion avancée des transactions et des paiements.

3. **Relations Acteurs-Cas d'Utilisation** :
   - **Utilisateur (User)** interagit principalement avec UC1, UC2, et UC3.
   - **Administrateur (Admin)** interagit principalement avec UC4 et UC5.

Ce diagramme montre comment différents acteurs interagissent avec les cas d'utilisation avancés du système de vente de livres d'occasion. Il illustre les interactions et les responsabilités spécifiques de chaque acteur dans le système.