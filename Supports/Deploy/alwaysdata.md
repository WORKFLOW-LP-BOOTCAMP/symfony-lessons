# Alwaysdata

Pour obtenir les permissions `drwxr-xr-x` pour un répertoire (ou un fichier) en utilisant la commande `chmod` sous Linux, vous pouvez utiliser la commande suivante :

```sh
chmod 755 nom_du_repertoire
```

Voici une explication des permissions et de la commande :

- `d` : Indique que c'est un répertoire.
- `rwx` : Les permissions pour le propriétaire (read, write, execute).
- `r-x` : Les permissions pour le groupe (read, execute).
- `r-x` : Les permissions pour les autres utilisateurs (read, execute).

Le chiffre `755` se décompose ainsi :
- `7` pour le propriétaire (`rwx` : 4+2+1).
- `5` pour le groupe (`r-x` : 4+0+1).
- `5` pour les autres (`r-x` : 4+0+1).

Par exemple, si le nom de votre répertoire est `mon_repertoire`, vous pouvez exécuter :

```sh
chmod 755 mon_repertoire
```

Cela attribuera les permissions `drwxr-xr-x` à `mon_repertoire`.