#  Exercice 1: Récupérer tous les formateurs

```php
// TrainerRepository.php
public function findAllTrainers()
{
    return $this->createQueryBuilder('t')
        ->getQuery()
        ->getResult();
}
```

### Exercice 2: Rechercher un formateur par son nom

```php
// TrainerRepository.php
public function findTrainerByName($name)
{
    return $this->createQueryBuilder('t')
        ->where('t.name = :name')
        ->setParameter('name', $name)
        ->getQuery()
        ->getResult();
}
```

### Exercice 3: Récupérer tous les articles

```php
// ArticleRepository.php
public function findAllArticles()
{
    return $this->createQueryBuilder('a')
        ->getQuery()
        ->getResult();
}
```

### Exercice 4: Rechercher des articles par leur titre

```php
// ArticleRepository.php
public function findArticlesByTitle($keyword)
{
    return $this->createQueryBuilder('a')
        ->where('a.title LIKE :keyword')
        ->setParameter('keyword', '%' . $keyword . '%')
        ->getQuery()
        ->getResult();
}
```

### Exercice 5: Récupérer les articles d'un formateur spécifique

```php
// ArticleRepository.php
public function findArticlesByTrainer(Trainer $trainer)
{
    return $this->createQueryBuilder('a')
        ->where('a.trainer = :trainer')
        ->setParameter('trainer', $trainer)
        ->getQuery()
        ->getResult();
}
```

### Exercice 6: Récupérer tous les sujets

```php
// SubjectRepository.php
public function findAllSubjects()
{
    return $this->createQueryBuilder('s')
        ->getQuery()
        ->getResult();
}
```

### Exercice 7: Récupérer les articles liés à un sujet spécifique

```php
// ArticleRepository.php
public function findArticlesBySubject(Subject $subject)
{
    return $this->createQueryBuilder('a')
        ->leftJoin('a.subjects', 's')
        ->where('s = :subject')
        ->setParameter('subject', $subject)
        ->getQuery()
        ->getResult();
}
```

### Exercice 8: Récupérer les formateurs qui ont écrit au moins un article

```php
// TrainerRepository.php
public function findTrainersWithArticles()
{
    return $this->createQueryBuilder('t')
        ->innerJoin('t.articles', 'a')
        ->getQuery()
        ->getResult();
}
```

### Exercice 9: Récupérer le nombre total d'articles par sujet

```php
// SubjectRepository.php
public function findArticleCountBySubject()
{
    return $this->createQueryBuilder('s')
        ->select('s.name as subjectName', 'COUNT(a.id) as articleCount')
        ->leftJoin('s.articles', 'a')
        ->groupBy('s.id')
        ->getQuery()
        ->getResult();
}
```

### Exercice 10: Récupérer les sujets avec le nombre d'articles associés

```php
// SubjectRepository.php
public function findSubjectsWithArticleCount()
{
    return $this->createQueryBuilder('s')
        ->select('s', 'COUNT(a.id) as articleCount')
        ->leftJoin('s.articles', 'a')
        ->groupBy('s.id')
        ->orderBy('articleCount', 'DESC')
        ->getQuery()
        ->getResult();
}
```

Ces méthodes sont conçues pour fonctionner avec Symfony et Doctrine en utilisant les repositories correspondants pour chaque entité (`Trainer`, `Article` et `Subject`). Assurez-vous que vos entités sont correctement configurées avec les annotations Doctrine appropriées (`@Entity`, `@OneToMany`, `@ManyToOne`, `@ManyToMany`, etc.) en fonction de vos relations de base de données.

Vous pouvez les tester en appelant ces méthodes à partir de vos contrôleurs Symfony, en passant les résultats à vos vues pour affichage ou traitement supplémentaire dans votre application.