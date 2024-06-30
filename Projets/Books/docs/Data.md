# Complément du Projet - Plateforme de Vente de Livres d'Occasion

## Modélisation UML

### Diagramme de Cas d'Utilisation

- **Acteurs** :
  - Utilisateur
  - Administrateur

- **Cas d'Utilisation Principaux** :
  - Inscription et Connexion
  - Recherche de Livres
  - Ajout au Panier
  - Gestion du Panier
  - Gestion des Livres (ajout, modification, suppression)
  - Passer une Commande
  - Gestion des Utilisateurs (administrateurs seulement)
  - Gestion des Commandes (administrateurs seulement)
  - Gestion des Commentaires et Évaluations (utilisateurs seulement)

### Diagramme de Classes

- **Classes Principales** :
  - Utilisateur
  - Livre
  - Panier
  - Commande
  - Commentaire
  - Administrateur

- **Relations** :
  - Utilisateur <> Panier (1-n)
  - Utilisateur <> Commande (1-n)
  - Livre <> Commentaire (1-n)
  - Administrateur <> Livre (n-m)

### Diagramme de Séquence (Exemple : Processus d'Achat)

- **Scénario** :
  1. Utilisateur recherche un livre.
  2. Utilisateur ajoute le livre au panier.
  3. Utilisateur passe la commande.
  4. Système confirme la commande et effectue le paiement.
  5. Système met à jour l'état de la commande.

## Modélisation MERISE

### Modèle Conceptuel de Données (MCD)

- **Entités Principales** :
  - Utilisateur
  - Livre
  - Panier
  - Commande
  - Commentaire

- **Relations** :
  - Utilisateur - Panier : (1-n)
  - Utilisateur - Commande : (1-n)
  - Livre - Commentaire : (1-n)

### Modèle Logique de Données (MLD)

- **Tables Principales** :
  - Utilisateur (id_utilisateur, nom, email, mot_de_passe, ...)
  - Livre (id_livre, titre, auteur, prix, état, ...)
  - Panier (id_panier, id_utilisateur, id_livre, quantité, ...)
  - Commande (id_commande, id_utilisateur, id_livre, statut, date_commande, ...)
  - Commentaire (id_commentaire, id_utilisateur, id_livre, commentaire, date_commentaire, ...)

- **Contraintes d'Intégrité** :
  - Clés primaires, clés étrangères pour assurer l'intégrité des données.

### Modèle Physique de Données (MPD)

- **Schéma de Base de Données PostgreSQL** :

```sql
CREATE TABLE Utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    -- autres champs nécessaires
);

CREATE TABLE Livre (
    id_livre SERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    auteur VARCHAR(100) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL,
    etat VARCHAR(50) NOT NULL,
    -- autres champs nécessaires
);

CREATE TABLE Panier (
    id_panier SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    quantite INT NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES Livre(id_livre)
    -- autres champs nécessaires
);

CREATE TABLE Commande (
    id_commande SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    statut VARCHAR(50) NOT NULL,
    date_commande DATE NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES Livre(id_livre)
    -- autres champs nécessaires
);

CREATE TABLE Commentaire (
    id_commentaire SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    commentaire TEXT NOT NULL,
    date_commentaire DATE NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES Livre(id_livre)
    -- autres champs nécessaires
);
```
