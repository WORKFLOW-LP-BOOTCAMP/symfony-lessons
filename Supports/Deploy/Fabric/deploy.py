from fabric import task, Connection

import os
import bcrypt
import pymysql.cursors

# Constantes repository - serveur Alwaysdata
REPO_URL = 'https://github.com/formation-aah/dev-trainer'
BRANCH = 'main'

APP_DIR = 'www'
EXCLUDE = ['vendor', 'var']
SSH_KEY_PATH = '/Users/antoinelucsko/.ssh/alwaysdata'
SERVER_ADDRESS = 'ssh-lu07.alwaysdata.net'
FILE_HTACCESS='./.htaccess'

## Constantes base de données
user_password = 'admin'
bcrypt_cost = 4
db_user = 'lu07'
host = 'mysql-lu07.alwaysdata.net'
db_password = 'devtrainer75'
db_name = 'lu07_dev-trainer'
sql = None

## Connexion au serveur de base de données
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

@task
def reset(c):
   
    if connServer.run(f'test -d {APP_DIR}', warn=True).ok:
        connServer.run(f'rm -rf {APP_DIR}')
    
    try:
        with connData.cursor() as cursor:
            # Préparer la commande SQL pour insérer l'utilisateur
            sql = """
            DROP TABLE subject_trainer, article, user, Property, log, subject, doctrine_migration_versions
            """
            cursor.execute(sql)
            connData.commit()
    except Exception as e:
        print("Database PB ", e)
    finally:
        connData.close()
        print("It's double time coeffe")

@task
def deploy(c):

    # Clone repository if it does not exist
    if not connServer.run(f'test -d {APP_DIR}', warn=True).ok:
        connServer.run(f'git clone {REPO_URL} {APP_DIR}')
    
    with connServer.cd(APP_DIR):
        if connServer.run('git rev-parse --is-inside-work-tree', warn=True).failed:
            connServer.run(f'git init && git remote add origin {REPO_URL}')
        
        connServer.run('git fetch --all')
        connServer.run('git reset --hard origin/main')
        
        # Run composer commands
        connServer.run('composer2 require symfony/requirements-checker')
        connServer.run('composer2 dump-env prod')

        env_local_php_path = '.env.local.php'
        
        # Retrieve environment variables
        try:
            pattern= f"s|'DATABASE_URL' => '[^']*'|'DATABASE_URL' => 'mysql://lu07:devtrainer75@mysql-lu07.alwaysdata.net:3306/lu07_dev-trainer'|"
            connServer.run(f'sed -i "{pattern}" "{env_local_php_path}"')
        except Exception as e:
            print(f"Erreur lors de la récupération des variables d'environnement : {e}")
            return
        
        # Optimize
        connServer.run('composer2 install --no-dev --optimize-autoloader')
        connServer.run('chmod -R 755 var')
        connServer.run('chmod -R 755 vendor')
        
        connServer.run('php bin/console cache:clear')
        
        connServer.run('php bin/console cache:warmup --env=prod')
        connServer.run('yes |php bin/console doctrine:migration:migrate')
        connServer.run('php bin/console asset-map:compile')
        
        # htaccess
        local_file = os.path.abspath('.htaccess')
        remote_path='/home/lu07/www/public'
        try:
            connServer.put(local_file, remote_path)
            print(f'Fichier {local_file} copié vers {remote_path} sur le serveur ')
            print("It's coeffe time")
            
        except Exception as e:
            print(f"Erreur lors de la copie du fichier : {e}")
        

@task
def create_user(c):
    hashed_password = bcrypt.hashpw(
        user_password.encode('utf-8'), 
        bcrypt.gensalt(bcrypt_cost)
    ).decode('utf-8')
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
        print("It's time to double coeffe")
    
@task
def check(c: Connection):
    
    with connServer.cd(APP_DIR):
        # Récupérer la branche distante
        connServer.run('git fetch origin')
        
        # Comparer les commits locaux et distants
        local_commit = connServer.run(f'git rev-parse HEAD', hide=True).stdout.strip()
        remote_commit = connServer.run(f'git rev-parse origin/{BRANCH}', hide=True).stdout.strip()
        
        if local_commit != remote_commit:
            print("Des changements ont été détectés. Déploiement en cours...")
            # Mettre à jour le dépôt local
            connServer.run(f'git pull origin {BRANCH}')
            connServer.run('php bin/console cache:clear')
        else:
            print("Aucun changement détecté.")