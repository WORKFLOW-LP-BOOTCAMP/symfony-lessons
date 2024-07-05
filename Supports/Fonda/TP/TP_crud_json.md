# Exercice CRUD Symfony 7

Dans cet exercice, nous allons créer un CRUD complet pour une application Symfony 7 utilisant les entités `Trainer`, `Article`, et `Subject`. Vous allez apprendre à mettre en place des opérations de création, lecture, mise à jour et suppression (CRUD) pour ces entités.

## 1. Créer les Entités

Tout d'abord, nous devons créer les entités `Trainer`, `Article`, et `Subject` avec les relations mentionnées.

```php
// src/Entity/Trainer.php
namespace App\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
class Trainer
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 100)]
    private string $firstName;

    #[ORM\Column(type: 'string', length: 100)]
    private string $lastName;

    #[ORM\Column(type: 'string', length: 100)]
    private string $profession;

    #[ORM\Column(type: 'text')]
    private string $bio;

    #[ORM\OneToMany(mappedBy: 'trainer', targetEntity: Article::class)]
    private Collection $articles;

    #[ORM\ManyToMany(targetEntity: Subject::class, inversedBy: 'trainers')]
    private Collection $subjects;

    public function __construct()
    {
        $this->articles = new ArrayCollection();
        $this->subjects = new ArrayCollection();
    }

    // getters and setters...
}

// src/Entity/Article.php
namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
class Article
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 100)]
    private string $title;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $createdAt;

    #[ORM\Column(type: 'text')]
    private string $content;

    #[ORM\ManyToOne(targetEntity: Trainer::class, inversedBy: 'articles')]
    private Trainer $trainer;

    // getters and setters...
}

// src/Entity/Subject.php
namespace App\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
class Subject
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 100)]
    private string $name;

    #[ORM\ManyToMany(targetEntity: Trainer::class, mappedBy: 'subjects')]
    private Collection $trainers;

    public function __construct()
    {
        $this->trainers = new ArrayCollection();
    }

    // getters and setters...
}
```

## 2. Configurer le CRUD

Ensuite, nous devons créer les contrôleurs pour gérer les opérations CRUD.

### TrainerController - déjà vu

```php
// src/Controller/TrainerController.php
namespace App\Controller;

use App\Entity\Trainer;
use App\Repository\TrainerRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\SerializerInterface;

class TrainerController extends AbstractController
{
    #[Route('/api/trainers', name: 'create_trainer', methods: ['POST'])]
    public function createTrainer(Request $request, SerializerInterface $serializer, EntityManagerInterface $em): JsonResponse
    {
        $trainer = $serializer->deserialize($request->getContent(), Trainer::class, 'json');
        $em->persist($trainer);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_CREATED);
    }

    #[Route('/api/trainers', name: 'list_trainers', methods: ['GET'])]
    public function listTrainers(TrainerRepository $trainerRepository): JsonResponse
    {
        $trainers = $trainerRepository->findAll();
        return $this->json($trainers);
    }

    #[Route('/api/trainers/{id}', name: 'show_trainer', methods: ['GET'])]
    public function showTrainer(Trainer $trainer): JsonResponse
    {
        return $this->json($trainer);
    }

    #[Route('/api/trainers/{id}', name: 'update_trainer', methods: ['PUT'])]
    public function updateTrainer(Request $request, Trainer $trainer, SerializerInterface $serializer, EntityManagerInterface $em): JsonResponse
    {
        $updatedTrainer = $serializer->deserialize($request->getContent(), Trainer::class, 'json', ['object_to_populate' => $trainer]);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_NO_CONTENT);
    }

    #[Route('/api/trainers/{id}', name: 'delete_trainer', methods: ['DELETE'])]
    public function deleteTrainer(Trainer $trainer, EntityManagerInterface $em): JsonResponse
    {
        $em->remove($trainer);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_NO_CONTENT);
    }
}
```

### ArticleController

```php
// src/Controller/ArticleController.php
namespace App\Controller;

use App\Entity\Article;
use App\Repository\ArticleRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\SerializerInterface;

class ArticleController extends AbstractController
{
    #[Route('/api/articles', name: 'create_article', methods: ['POST'])]
    public function createArticle(Request $request, SerializerInterface $serializer, EntityManagerInterface $em): JsonResponse
    {
        $article = $serializer->deserialize($request->getContent(), Article::class, 'json');
        $em->persist($article);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_CREATED);
    }

    #[Route('/api/articles', name: 'list_articles', methods: ['GET'])]
    public function listArticles(ArticleRepository $articleRepository): JsonResponse
    {
        $articles = $articleRepository->findAll();
        return $this->json($articles);
    }

    #[Route('/api/articles/{id}', name: 'show_article', methods: ['GET'])]
    public function showArticle(Article $article): JsonResponse
    {
        return $this->json($article);
    }

    #[Route('/api/articles/{id}', name: 'update_article', methods: ['PUT'])]
    public function updateArticle(Request $request, Article $article, SerializerInterface $serializer, EntityManagerInterface $em): JsonResponse
    {
        $updatedArticle = $serializer->deserialize($request->getContent(), Article::class, 'json', ['object_to_populate' => $article]);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_NO_CONTENT);
    }

    #[Route('/api/articles/{id}', name: 'delete_article', methods: ['DELETE'])]
    public function deleteArticle(Article $article, EntityManagerInterface $em): JsonResponse
    {
        $em->remove($article);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_NO_CONTENT);
    }
}
```

### SubjectController

```php
// src/Controller/SubjectController.php
namespace App\Controller;

use App\Entity\Subject;
use App\Repository\SubjectRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\SerializerInterface;

class SubjectController extends AbstractController
{
    #[Route('/api/subjects', name: 'create_subject', methods: ['POST'])]
    public function createSubject(Request $request, SerializerInterface $serializer, EntityManagerInterface $em): JsonResponse
    {
        $subject = $serializer->deserialize($request->getContent(), Subject::class, 'json');
        $em->persist($subject);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_CREATED);
    }

    #[Route('/api/subjects', name: 'list_subjects', methods: ['GET'])]
    public function listSubjects(SubjectRepository $subjectRepository): JsonResponse
    {
        $subjects = $subjectRepository->findAll();
        return $this->json($subjects);
    }

    #[Route('/api/subjects/{id}', name: 'show_subject', methods: ['GET'])]
    public function showSubject(Subject $subject): JsonResponse
    {
        return $this->json($subject);
    }

    #[Route('/api/subjects/{id}', name: 'update_subject', methods: ['PUT'])]
    public function updateSubject(Request $request, Subject $subject, SerializerInterface $serializer, EntityManagerInterface $em): JsonResponse
    {
        $updatedSubject = $serializer->deserialize($request->getContent(), Subject::class, 'json', ['object_to_populate' => $subject]);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_NO_CONTENT);
    }

    #[Route('/api/subjects/{id}', name: 'delete_subject', methods: ['DELETE'])]
    public function deleteSubject(Subject $subject, EntityManagerInterface $em): JsonResponse
    {
        $em->remove($

subject);
        $em->flush();

        return new JsonResponse(null, JsonResponse::HTTP_NO_CONTENT);
    }
}
```

## 3. Tester les Routes

Avec ces contrôleurs en place, vous pouvez tester les opérations CRUD avec des outils comme Postman ou curl.
