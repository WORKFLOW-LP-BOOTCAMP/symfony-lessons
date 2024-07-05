## Modèle 

## 1. Constraints (`Assert`)

Les contraintes de validation (`Assert`) en Symfony permettent de valider les données des entités avant de les persister dans la base de données. Elles sont définies à l'aide des annotations dans les entités.

## Exemple dans la classe `Article` :

```php
#[Assert\Length(max: 100, maxMessage: 'Le titre ne peut pas dépasser {{ limit }} caractères.')]
#[ORM\Column(length: 100)]
private ?string $title = null;

#[Assert\LessThan(value: 255, message: 'valeur trop grande')]
#[ORM\Column(type: Types::TEXT, nullable: true)]
private ?string $content = null;
```

- **`@Assert\Length`** : Cette contrainte s'assure que la longueur du champ ne dépasse pas une certaine limite.
- **`@Assert\LessThan`** : Cette contrainte s'assure que la valeur du champ est inférieure à une certaine limite. Notez que l'usage de cette contrainte avec une chaîne de caractères est incorrect et devrait être remplacé par `@Assert\Length`.

### 2. Relations entre Entités

Doctrine permet de définir plusieurs types de relations entre entités : `OneToOne`, `OneToMany`, `ManyToOne`, et `ManyToMany`.

## Exemple `ManyToOne` :

Dans notre exemple, un `Article` est lié à un `Trainer` :

```php
#[ORM\ManyToOne(targetEntity: Trainer::class, inversedBy: 'articles')]
#[ORM\JoinColumn(name: "trainer_id", referencedColumnName: "id", onDelete: "SET NULL")]
private ?Trainer $trainer = null;
```

- **`@ORM\ManyToOne`** : Indique qu'un `Article` peut avoir un seul `Trainer`, mais qu'un `Trainer` peut avoir plusieurs `Article`.
- **`@ORM\JoinColumn`** : Spécifie les détails de la colonne de jointure :
  - `name` : Le nom de la colonne dans la table `article` qui stocke la clé étrangère.
  - `referencedColumnName` : Le nom de la colonne dans la table `trainer` référencée par cette clé étrangère.
  - `onDelete` : Définit le comportement lors de la suppression d'un `Trainer` :
    - `SET NULL` : Définit la clé étrangère à `NULL` lorsque le `Trainer` est supprimé.

## Exemple `OneToMany` :

Du côté du `Trainer`, nous avons une relation `OneToMany` avec les articles :

```php
#[ORM\OneToMany(targetEntity: Article::class, mappedBy: 'trainer', cascade: ['persist', 'remove'], orphanRemoval: false)]
private Collection $articles;
```

- **`@ORM\OneToMany`** : Indique qu'un `Trainer` peut avoir plusieurs `Article`.
- **`mappedBy`** : Indique la propriété dans l'entité `Article` qui est propriétaire de la relation.
- **`cascade`** : Définit les opérations en cascade sur les articles :
  - `persist` : Les `Article` seront persistés automatiquement lorsque le `Trainer` est persité.
  - `remove` : Les `Article` seront supprimés automatiquement lorsque le `Trainer` est supprimé.
- **`orphanRemoval`** : Si défini à `true`, les `Article` sans `Trainer` seront automatiquement supprimés.

### 3. Options de Cascade

Les options de cascade permettent de définir quelles opérations sur une entité doivent être propagées aux entités associées.

- **`persist`** : Lorsqu'une entité est persistée, toutes les entités liées avec cette option sont également persistées.
- **`remove`** : Lorsqu'une entité est supprimée, toutes les entités liées avec cette option sont également supprimées.
- **`detach`** : Lorsqu'une entité est détachée, toutes les entités liées avec cette option sont également détachées.
- **`merge`** : Lorsqu'une entité est fusionnée, toutes les entités liées avec cette option sont également fusionnées.
- **`refresh`** : Lorsqu'une entité est rafraîchie, toutes les entités liées avec cette option sont également rafraîchies.

## Exemple d'utilisation des options de cascade :

Dans l'entité `Trainer`, nous pourrions définir :

```php
#[ORM\OneToMany(targetEntity: Article::class, mappedBy: 'trainer', cascade: ['persist', 'remove'])]
private Collection $articles;
```

Cela signifie que lorsque vous sauvegardez un `Trainer`, tous les `Article` associés seront également sauvegardés. De même, lorsque vous supprimez un `Trainer`, tous les `Article` associés seront également supprimés.
