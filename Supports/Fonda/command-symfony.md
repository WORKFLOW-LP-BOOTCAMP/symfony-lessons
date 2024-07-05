# Commandes CLI SF


```bash
#debug bar JAMAIS en production
composer require --dev symfony/profiler-pack

curl -sS https://get.symfony.com/cli/installer | bash
mv /Users/votre_nom_de_machine/.symfony/bin/symfony /usr/local/bin/symfony

symfony check:requirements
php bin/console about

# create new app dev-trainer
symfony new dev-trainer

composer create-project symfony/skeleton dev-trainer

symfony help server:start

symfony server:start
symfony server:start --no-tls

# markers
symfony composer req maker --dev

symfony console list make

# moteur de template
composer require twig

composer remove twig

php bin/console debug:config twig

composer require symfony/asset-mapper symfony/asset symfony/twig-pack

php bin/console importmap:require bootstrap
php bin/console importmap:require stimulus

php bin/console importmap:remove stimulus

# production
php bin/console asset-map:compile

# debug map
php bin/console debug:asset-map

# re-install
hp bin/console importmap:install

# creation controller
symfony console make:controller Home

# Creation de formulaire maker
composer require --dev symfony/maker-bundle

# barre de debug
composer require --dev symfony/profiler-pack

################################ ORM Doctrine ####################################################

# Doctrine ORM
composer require symfony/orm-pack
# maker pour SF - ORM Doctrine
composer require symfony/maker-bundle

php bin/console list doctrine:database

php bin/console list doctrine

# create database --> .env
php bin/console doctrine:database:create

# create entity
php bin/console make:entity

# générer le fichier de migration à partir de/des entité(s)
php bin/console make:migration

# Création physique des tables
php bin/console doctrine:migrations:migrate

# Composant 
composer require orm-fixtures --dev

# données faker
composer require fakerphp/faker --dev

# Créer les données d'exemple
php bin/console doctrine:fixtures:load

# vérifiez que les données sont bien dans les tables
php bin/console dbal:run-sql 'SELECT * FROM trainer'

composer require symfony/form

# ainsi que des maker dev utils
composer require --dev symfony/maker-bundle

# debug
php bin/console debug:form

composer require symfony/validator
```
