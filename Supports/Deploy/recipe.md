# Introduction

Dans ce tutoriel, nous allons voir comment utiliser Fabric pour automatiser diverses tâches sur un serveur distant. Fabric est une bibliothèque Python utilisée pour déployer des applications ou effectuer des tâches administratives sur des serveurs distants via SSH.

Nous allons travailler avec un exemple de script Fabric qui inclut plusieurs tâches : réinitialiser la base de données, déployer une application, créer un utilisateur et vérifier l'état du dépôt Git.

## Pré-requis

- Python 3.x installé sur votre machine.
- Fabric installé (vous pouvez l'installer avec `pip install fabric`).
- Accès SSH à un serveur distant.
- Un dépôt Git que vous souhaitez cloner et déployer sur le serveur.

## Script Fabric

Voici le script Fabric complet avec des explications détaillées pour chaque commande :

```python
from fabric import task, Connection
import bcrypt
import pymysql.cursors
import os 

# Constantes repository - serveur Alwaysdata
REPO_URL = 'https://github.com/formation-aah/dev-trainer'
BRANCH = 'main'

APP_DIR = 'www'
EXCLUDE = ['vendor', 'var']
SSH_KEY_PATH = '/Users/antoinelucsko/.ssh/alwaysdata'
SERVER_ADDRESS = 'ssh-lu07.alwaysdata.net'
FILE_HTACCESS='./.htaccess'

# Constantes base de données
user_password = 'admin'
bcrypt_cost = 4
db_user = 'lu07'
host = 'mysql-lu07.alwaysdata.net'
db_password = 'devtrainer75'
db_name = 'lu07_dev-trainer'
sql = None

# Remote path serveur
remote_path='/home/lu07/www/public'

# Connexion au serveur via SSH
connServer = Connection(  
    host=SERVER_ADDRESS,
    user='lu07',
    connect_kwargs={"key_filename": SSH_KEY_PATH}
)

# Connexion à la base de données
connData = pymysql.connect(
    host=host, 
    user=db_user, 
    password=db_password, 
    database=db_name, 
    cursorclass=pymysql.cursors.DictCursor
)

# Tâche pour réinitialiser la base de données et le répertoire de l'application
@task
def reset(c):
    # Vérifie si le répertoire de l'application existe et le supprime
    if connServer.run(f'test -d {APP_DIR}', warn=True).ok:
        connServer.run(f'rm -rf {APP_DIR}')
    
    try:
        with connData.cursor() as cursor:
            # Supprime les tables de la base de données
            sql = """
            DROP TABLE subject_trainer, article, user, Property, log, subject, doctrine_migration_versions
            """
            cursor.execute(sql)
            connData.commit()
    except Exception as e:
        print("Database PB ", e)
    finally:
        connData.close()
        print("It's double time coffe")

# Tâche pour déployer l'application
@task
def deploy(c):
    # Clone le dépôt Git si le répertoire n'existe pas
    if not connServer.run(f'test -d {APP_DIR}', warn=True).ok:
        connServer.run(f'git clone {REPO_URL} {APP_DIR}')
    
    with connServer.cd(APP_DIR):
        if connServer.run('git rev-parse --is-inside-work-tree', warn=True).failed:
            connServer.run(f'git init && git remote add origin {REPO_URL}')
        
        connServer.run('git fetch --all')
        connServer.run(f'git reset --hard origin/{BRANCH}')
        
        # Exécute les commandes Composer
        connServer.run('composer2 require symfony/requirements-checker')
        connServer.run('composer2 dump-env prod')

        env_local_php_path = '.env.local.php'
        
        # Met à jour les variables d'environnement dans le fichier .env.local.php
        try:
            pattern= f"s|'DATABASE_URL' => '[^']*'|'DATABASE_URL' => 'mysql://{db_user}:{db_password}@{host}:3306/{db_name}'|"
            connServer.run(f'sed -i "{pattern}" "{env_local_php_path}"')
        except Exception as e:
            print(f"Erreur lors de la récupération des variables d'environnement : {e}")
            return
        
        # Optimise l'installation de Composer
        connServer.run('composer2 install --no-dev --optimize-autoloader')
        connServer.run('chmod -R 755 var')
        connServer.run('chmod -R 755 vendor')
        
        # Nettoie et prépare le cache Symfony
        connServer.run('php bin/console cache:clear')
        connServer.run('php bin/console cache:warmup --env=prod')
        connServer.run('yes | php bin/console doctrine:migration:migrate')
        connServer.run('php bin/console asset-map:compile')

        # Copie le fichier .htaccess
        local_file = os.path.abspath(FILE_HTACCESS)
        try:
            connServer.put(local_file, remote_path)
            print(f'Fichier {local_file} copié vers {remote_path} sur le serveur ')
            print("It's coffe time")
        except Exception as e:
            print(f"Erreur lors de la copie du fichier : {e}")

# Tâche pour créer un utilisateur dans la base de données
@task
def create_user(c):
    # Copie le fichier dump.sql vers le serveur et l'exécute
    local_file = os.path.abspath('dump.sql')
    connServer.put(local_file, APP_DIR)
    with connServer.cd(APP_DIR):
        command = f"mysql -h {host} -u {db_user} -p{db_password} {db_name} < 'dump.sql'"
        try:
            connServer.run(command)
            print("Le script SQL a été exécuté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'exécution du script SQL : {e}")
    print("It's time to double coffe")

# Tâche pour vérifier l'état du dépôt Git
@task
def check(c: Connection):
    with connServer.cd(APP_DIR):
        # Récupère les mises à jour de la branche distante
        connServer.run('git fetch origin')
        
        # Compare les commits locaux et distants
        local_commit = connServer.run(f'git rev-parse HEAD', hide=True).stdout.strip()
        remote_commit = connServer.run(f'git rev-parse origin/{BRANCH}', hide=True).stdout.strip()
        
        if local_commit != remote_commit:
            print("Des changements ont été détectés. Déploiement en cours...")
            # Met à jour le dépôt local
            connServer.run(f'git pull origin {BRANCH}')
            connServer.run('php bin/console cache:clear')
        else:
            print("Aucun changement détecté.")
```

## Explications détaillées

### 1. Imports et constantes

```python
from fabric import task, Connection
import bcrypt
import pymysql.cursors
import os 

REPO_URL = 'https://github.com/formation-aah/dev-trainer'
BRANCH = 'main'
APP_DIR = 'www'
EXCLUDE = ['vendor', 'var']
SSH_KEY_PATH = '/Users/antoinelucsko/.ssh/alwaysdata'
SERVER_ADDRESS = 'ssh-lu07.alwaysdata.net'
FILE_HTACCESS='./.htaccess'
user_password = 'admin'
bcrypt_cost = 4
db_user = 'lu07'
host = 'mysql-lu07.alwaysdata.net'
db_password = 'devtrainer75'
db_name = 'lu07_dev-trainer'
sql = None
remote_path='/home/lu07/www/public'
```

Ces constantes définissent les informations de connexion, les chemins de fichier, et d'autres paramètres nécessaires pour le script.

### 2. Connexions au serveur et à la base de données

```python
connServer = Connection(  
    host=SERVER_ADDRESS,
    user='lu07',
    connect_kwargs={"key_filename": SSH_KEY_PATH}
)

connData = pymysql.connect(
    host=host, 
    user=db_user, 
    password=db_password, 
    database=db_name, 
    cursorclass=pymysql.cursors.DictCursor
)
```

Ici, nous établissons une connexion SSH au serveur distant avec Fabric et une connexion à la base de données MySQL avec `pymysql`.

### 3. Tâche `reset`

```python
@task
def reset(c):
    if connServer.run(f'test -d {APP_DIR}', warn=True).ok:
        connServer.run(f'rm -rf {APP_DIR}')
    
    try:
        with connData.cursor() as cursor:
            sql = """
            DROP TABLE subject_trainer, article, user, Property, log, subject, doctrine_migration_versions
            """
            cursor.execute(sql)
            connData.commit()
    except Exception as e:
        print("Database PB ", e)
    finally:
        connData.close()
        print("It's double time coffe")
```

Cette tâche réinitialise l'état du répertoire de l'application et supprime certaines tables de la base de données.

### 4. Tâche `deploy`

```python
@task
def deploy(c):
    if not connServer.run(f'test -d {APP_DIR}', warn=True).ok:
        connServer.run(f'git clone {REPO_URL} {APP_DIR}')
    
    with connServer.cd(APP_DIR):
        if connServer.run('git rev-parse --is-inside-work-tree', warn=True).failed:
            connServer.run(f'git init && git remote add origin {REPO_URL}')
        
        connServer.run('git fetch --all')
        connServer.run(f'git reset --hard origin/{BRANCH}')
        
        connServer.run('composer2 require symfony/requirements-checker')
        connServer.run('composer2 dump-env prod')

        env_local_php_path = '.env.local.php'
        
        try:
            pattern= f"s|'DATABASE_URL' => '[^']*'|'DATABASE_URL' => 'mysql://{db_user}:{db_password}@{host}:3306/{db_name}'|"
            connServer.run(f'sed -i "{pattern}" "{env_local_php_path}"')
        except Exception as e:
            print(f"Erreur lors de la récupération des variables d'environnement : {e}")
            return
        
        connServer.run('composer2 install --no-dev --optimize-autoloader')
        connServer.run('chmod -R 755 var')
        connServer.run('chmod -R 755 vendor')
        
        connServer.run('php bin/console cache:clear')
        connServer.run('php bin/console cache:warmup --env=prod')
        connServer.run('yes | php bin/console doctrine:migration:migrate')
        connServer.run('php bin/console asset-map:compile')

        local_file = os.path.abspath(FILE_HTACCESS)
        try:
            connServer.put(local_file, remote_path)
            print(f'Fichier {local_file} copié vers {remote_path} sur le serveur ')
            print("It's coffe time")
        except Exception as e:
            print(f"Erreur lors de la copie du fichier : {e}")
```

Cette tâche clone le dépôt Git, exécute les commandes Composer nécessaires, met à jour les variables d'environnement, et optimise l'installation de l'application.

### 5. Tâche `create_user`

```python
@task
def create_user(c):
    local_file = os.path.abspath('dump.sql')
    connServer.put(local_file, APP_DIR)
    with connServer.cd(APP_DIR):
        command = f"mysql -h {host} -u {db_user} -p{db_password} {db_name} < 'dump.sql'"
        try:
            connServer.run(command)
            print("Le script SQL a été exécuté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'exécution du script SQL : {e}")
    print("It's time to double coffe")
```

Cette tâche charge un fichier SQL sur le serveur et l'exécute pour créer un utilisateur dans la base de données.

### 6. Tâche `check`

```python
@task
def check(c: Connection):
    with connServer.cd(APP_DIR):
        connServer.run('git fetch origin')
        
        local_commit = connServer.run(f'git rev-parse HEAD', hide=True).stdout.strip()
        remote_commit = connServer.run(f'git rev-parse origin/{BRANCH}', hide=True).stdout.strip()
        
        if local_commit != remote_commit:
            print("Des changements ont été détectés. Déploiement en cours...")
            connServer.run(f'git pull origin {BRANCH}')
            connServer.run('php bin/console cache:clear')
        else:
            print("Aucun changement détecté.")
```

Cette tâche vérifie si des changements ont été apportés au dépôt Git et les déploie si nécessaire.


## Git détails

La commande `git rev-parse --is-inside-work-tree` est utilisée pour vérifier si le répertoire courant ou un répertoire donné est à l'intérieur d'un dépôt Git. Elle renvoie `true` si vous êtes à l'intérieur d'un dépôt Git et `false` sinon. Cette commande est particulièrement utile dans des scripts pour déterminer si les commandes Git peuvent être exécutées dans le répertoire courant.

### Décomposition de la commande

1. **`git rev-parse`** :
   `git rev-parse` est une commande Git polyvalente utilisée principalement pour manipuler et interroger les révisions et d'autres objets dans un dépôt Git. Elle peut être utilisée pour transformer les révisions en hashes, vérifier des références, obtenir des noms de branches, et plus encore.

2. **`--is-inside-work-tree`** :
   Cette option spécifique de `git rev-parse` renvoie `true` si le répertoire courant est à l'intérieur de l'arborescence de travail d'un dépôt Git. L'arborescence de travail est la partie du dépôt où vous travaillez avec les fichiers et les dossiers de votre projet, en contraste avec les objets Git stockés dans le répertoire `.git`.

### Exemple d'utilisation

Lorsque vous exécutez cette commande dans un répertoire, voici ce qui se passe :

- Si vous êtes à l'intérieur d'un dépôt Git, la commande renvoie `true` :
  ```sh
  $ git rev-parse --is-inside-work-tree
  true
  ```

- Si vous n'êtes pas dans un dépôt Git, elle renvoie une erreur :
  ```sh
  $ git rev-parse --is-inside-work-tree
  fatal: not a git repository (or any of the parent directories): .git
  ```

### Utilisation dans des scripts

Dans un script, cette commande est souvent utilisée pour vérifier si le répertoire courant est bien un dépôt Git avant de procéder à d'autres commandes Git. Par exemple :

```bash
#!/bin/bash

# Vérifie si le répertoire courant est un dépôt Git
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Nous sommes dans un dépôt Git."
  # D'autres commandes Git peuvent être exécutées ici
else
  echo "Ce répertoire n'est pas un dépôt Git."
  # Vous pourriez vouloir initialiser un dépôt Git ou quitter le script
fi
```

### Contexte dans le script Fabric

Dans le script Fabric que nous avons fourni, cette commande est utilisée pour vérifier si le répertoire de l'application (`APP_DIR`) est un dépôt Git :

```python
with connServer.cd(APP_DIR):
    if connServer.run('git rev-parse --is-inside-work-tree', warn=True).failed:
        connServer.run(f'git init && git remote add origin {REPO_URL}')
```

- **Objectif** : Vérifier si `APP_DIR` est déjà un dépôt Git.
- **Action en cas d'échec** : Si `APP_DIR` n'est pas un dépôt Git, le script initialise un nouveau dépôt Git avec `git init` et ajoute l'origine avec `git remote add origin {REPO_URL}`.

Cela permet de s'assurer que les commandes Git suivantes peuvent être exécutées en toute sécurité, sachant que le répertoire est bien configuré comme un dépôt Git.

### `git fetch --all` et `git reset --hard origin/{BRANCH}`

Les commandes `git fetch --all` et `git reset --hard origin/{BRANCH}` sont utilisées pour synchroniser le dépôt local avec le dépôt distant. Voici une explication détaillée de ce que fait chaque commande.

### `git fetch --all`

#### Description

La commande `git fetch` est utilisée pour télécharger les objets et les références des autres dépôts. L'option `--all` indique que la commande doit récupérer les branches et les objets de tous les dépôts distants configurés.

#### Fonctionnement

- **`git fetch`** :
  - Télécharge les objets et les références (comme les branches) depuis le dépôt distant vers le dépôt local.
  - Ne modifie pas l'état de l'arborescence de travail (les fichiers et les répertoires que vous voyez dans votre projet).
  - Met à jour les références distantes (comme `origin/main`) sans modifier les branches locales.

- **`--all`** :
  - Télécharge les objets et les références de **tous** les dépôts distants configurés dans le projet Git.

#### Exemple

```sh
git fetch --all
```

Cela télécharge les mises à jour de toutes les branches de tous les dépôts distants configurés sans modifier votre arborescence de travail.

### `git reset --hard origin/{BRANCH}`

#### Description

La commande `git reset` est utilisée pour réinitialiser le pointeur de la branche courante vers un commit spécifié, et l'option `--hard` indique que l'arborescence de travail doit également être réinitialisée pour correspondre à ce commit. `origin/{BRANCH}` se réfère à la branche distante spécifiée.

#### Fonctionnement

- **`git reset`** :
  - Change le pointeur de la branche actuelle pour qu'il pointe vers un commit différent.
  
- **`--hard`** :
  - Réinitialise l'index et l'arborescence de travail pour correspondre exactement à l'état du commit spécifié.
  - Toutes les modifications non validées dans l'arborescence de travail et dans l'index sont perdues.

- **`origin/{BRANCH}`** :
  - Référence une branche du dépôt distant `origin`.
  - `{BRANCH}` est une variable qui représente le nom de la branche (par exemple, `main` ou `master`).

#### Exemple

```sh
git reset --hard origin/main
```

Cela fait deux choses :
1. **Réinitialisation du pointeur de la branche courante** : La branche locale est mise à jour pour pointer exactement sur le même commit que `origin/main`.
2. **Réinitialisation de l'arborescence de travail** : Tous les fichiers et répertoires de votre projet sont réinitialisés pour correspondre exactement à l'état de `origin/main`, supprimant toutes les modifications non validées.

### Contexte dans le script Fabric

Dans le script Fabric, ces commandes sont utilisées dans la tâche de déploiement pour s'assurer que le dépôt local est synchronisé avec la branche distante spécifiée (`main` dans ce cas). Voici comment ces commandes sont utilisées dans le script :

```python
with connServer.cd(APP_DIR):
    connServer.run('git fetch --all')
    connServer.run(f'git reset --hard origin/{BRANCH}')
```

#### Explication détaillée :

1. **`connServer.run('git fetch --all')`** :
   - Cette commande télécharge les objets et les références de toutes les branches de tous les dépôts distants configurés dans le projet Git du répertoire `APP_DIR` sur le serveur.

2. **`connServer.run(f'git reset --hard origin/{BRANCH}')`** :
   - Cette commande réinitialise la branche locale pour qu'elle corresponde exactement à la branche distante `origin/{BRANCH}`.
   - Toute modification locale non validée sera perdue, et l'arborescence de travail sera mise à jour pour refléter exactement l'état de `origin/{BRANCH}`.

#### But

L'objectif de ces commandes est de s'assurer que le répertoire local de l'application (`APP_DIR`) est parfaitement synchronisé avec l'état le plus récent de la branche distante `main`. Cela garantit que vous travaillez avec la version la plus à jour du code source et que toutes les modifications locales non validées sont supprimées, ce qui est souvent souhaitable dans les scénarios de déploiement automatisé.


## Annexes 

```bash
mysqldump -u root -pantoine db_trainer $(mysql -u root -pantoine -Nse 'show tables from db_trainer' | grep -Ev '^(doctrine_migration_versions)$') > dump.sql

mysqldump -u root -pantoine --no-create-info db_trainer $(mysql -u root -pantoine -Nse 'show tables from db_trainer' | grep -Ev '^(doctrine_migration_versions)$') > dump.sql
```

```python
# connexion à la base de données distante
connData = pymysql.connect(
    host=host, 
    user=db_user, 
    password=db_password, 
    database=db_name, 
    cursorclass=pymysql.cursors.DictCursor
)
 hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt(bcrypt_cost)).decode('utf-8')
 try:
     with connData.cursor() as cursor:
         # Préparer la commande SQL pour insérer l'utilisateur
         sql = """
         INSERT INTO user (`first_name`, `email`, `password`, `roles`, `discr`) VALUES (%s, %s, %s, %s, %s)
         """
         cursor.execute(sql, ('admin', 'admin@admin.fr', hashed_password, '[\"ROLE_ADMIN\"]', 'User'))
         connData.commit()
 except Exception as e:
     print("Database PB ", e)
 finally:
     connData.close()

```