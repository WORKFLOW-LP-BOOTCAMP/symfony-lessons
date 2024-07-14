# Testing dans Symfony

## Introduction
Les tests sont essentiels pour assurer la fiabilité et la qualité des applications Symfony. On distingue principalement trois types de tests : les tests unitaires, les tests d'intégration et les tests d'application.

## Framework de tests PHPUnit
Symfony utilise PHPUnit comme framework de tests. Pour commencer, installez `symfony/test-pack` :

```bash
composer require --dev symfony/test-pack
```

## Types de tests

1. **Tests Unitaires**
   - Testent des unités individuelles de code source, comme une classe ou une méthode.
   - Exemple : tester une méthode dans un service.

2. **Tests d'Intégration**
   - Testent des combinaisons de classes et souvent interagissent avec le conteneur de services Symfony.
   - Exemple : tester une interaction entre plusieurs services.

3. **Tests d'Application**
   - Testent le comportement d'une application complète via des requêtes HTTP réelles ou simulées.
   - Exemple : tester le rendu d'une page web avec une requête GET.

## Exemples de Tests

### Test Unitaire

```php
// Exemple de test unitaire pour une méthode dans un service
public function testSomeMethod(): void
{
    // Initialisation du service
    $service = new MyService();

    // Appel de la méthode à tester
    $result = $service->someMethod();

    // Assertion pour vérifier le résultat attendu
    $this->assertEquals('expected', $result);
}
```

### Test d'Intégration

```php
// Exemple de test d'intégration avec utilisation du conteneur de services Symfony
public function testServiceIntegration(): void
{
    self::bootKernel();
    $container = self::$container;

    // Récupération d'un service à tester
    $service = $container->get(MyService::class);

    // Utilisation du service et assertions
    $result = $service->doSomething();
    $this->assertTrue($result);
}
```

### Test d'Application

```php
// Exemple de test d'application avec Symfony WebTestCase
public function testHomepage(): void
{
    $client = static::createClient();

    // Requête HTTP GET à une URL spécifique
    $crawler = $client->request('GET', '/');

    // Assertions sur la réponse HTTP
    $this->assertResponseIsSuccessful();
    $this->assertSelectorTextContains('h1', 'Bienvenue sur mon site');
}
```

## Configuration et Environnement de Test

Symfony utilise un environnement de test distinct, configuré dans `.env.test`, pour isoler les tests des autres environnements comme le développement ou la production.
