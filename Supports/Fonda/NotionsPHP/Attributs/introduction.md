# Cours : Les Attributs en PHP 8

Les attributs, introduits en PHP 8, permettent d'ajouter des métadonnées à des classes, des méthodes, des propriétés et des paramètres. Ces métadonnées peuvent ensuite être utilisées par des outils ou des bibliothèques pour modifier le comportement de votre code ou pour effectuer des actions spécifiques.

## 1. Introduction aux Attributs

Les attributs sont des annotations structurées qui offrent une alternative aux commentaires docblock utilisés jusqu'à présent pour les annotations en PHP. 

Ils apportent une syntaxe plus formelle et des possibilités plus puissantes pour ajouter des métadonnées.

## 2. Syntaxe des Attributs

Pour définir un attribut, on utilise la syntaxe `#[...]` :

```php
#[Attribute]
class MyAttribute {
    public string $value;

    public function __construct(string $value) {
        $this->value = $value;
    }
}
```

## 3. Utilisation des Attributs

Les attributs peuvent être appliqués à différentes cibles dans le code :

- **Classes**
- **Méthodes**
- **Propriétés**
- **Paramètres**

Voici un exemple d'utilisation des attributs :

```php
#[MyAttribute('Class Attribute')]
class MyClass {
    #[MyAttribute('Property Attribute')]
    public string $property;

    #[MyAttribute('Method Attribute')]
    public function myMethod(#[MyAttribute('Parameter Attribute')] string $param): void {
        // ...
    }
}
```

## 4. Lecture des Attributs

Pour accéder aux attributs, PHP utilise la réflexion (`ReflectionClass`, `ReflectionMethod`, `ReflectionProperty`, etc.). Voici comment lire les attributs :

```php
$reflectionClass = new ReflectionClass(MyClass::class);
$classAttributes = $reflectionClass->getAttributes(MyAttribute::class);

foreach ($classAttributes as $attribute) {
    $instance = $attribute->newInstance();
    echo $instance->value; // Output: Class Attribute
}
```

## 5. Exemple Pratique : Validation de Données

Supposons que nous voulons utiliser des attributs pour valider les données d'un formulaire :

1. **Définir les Attributs de Validation** :

    ```php
    #[Attribute]
    class NotBlank {
        public function __construct() {}
    }

    #[Attribute]
    class Length {
        public int $min;
        public int $max;

        public function __construct(int $min, int $max) {
            $this->min = $min;
            $this->max = $max;
        }
    }

    #[Attribute]
    class Email {
        public function __construct() {}
    }
    ```

2. **Utiliser les Attributs sur une Classe** :

    ```php
    class User {
        #[NotBlank]
        #[Length(3, 50)]
        public string $username;

        #[NotBlank]
        #[Email]
        public string $email;

        #[NotBlank]
        #[Length(8, 20)]
        public string $password;

        public function __construct(string $username, string $email, string $password) {
            $this->username = $username;
            $this->email = $email;
            $this->password = $password;
        }
    }
    ```

3. **Valider les Données en Utilisant les Attributs** :

    ```php
    function validate(object $object): array {
        $errors = [];
        $reflectionClass = new ReflectionClass($object);

        foreach ($reflectionClass->getProperties() as $property) {
            $property->setAccessible(true);
            $value = $property->getValue($object);

            foreach ($property->getAttributes() as $attribute) {
                $instance = $attribute->newInstance();

                if ($instance instanceof NotBlank && empty($value)) {
                    $errors[] = $property->getName() . ' should not be blank';
                }

                if ($instance instanceof Length) {
                    $length = strlen($value);
                    if ($length < $instance->min || $length > $instance->max) {
                        $errors[] = $property->getName() . " should be between {$instance->min} and {$instance->max} characters";
                    }
                }

                if ($instance instanceof Email && !filter_var($value, FILTER_VALIDATE_EMAIL)) {
                    $errors[] = $property->getName() . ' should be a valid email address';
                }
            }
        }

        return $errors;
    }

    $user = new User('', 'invalid-email', 'short');
    $errors = validate($user);

    foreach ($errors as $error) {
        echo $error . PHP_EOL;
    }
    ```

    ### Résultat

    En exécutant ce code avec l'instance `User` fournie, la sortie sera :

    ```
    username should not be blank
    email should be a valid email address
    password should be between 8 and 20 characters
    ```
