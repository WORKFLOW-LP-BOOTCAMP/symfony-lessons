# Introduction à Stimulus et SweetAlert2

Sweet JS [doc](https://sweetalert2.github.io)

## Les commandes utiles

```bash
# stimulus JS
composer require symfony/stimulus-bundle
php bin/console importmap:require sweetalert2

# supprimer le cache si quelque chose vous semble pas normale
php bin/console cache:clear
```

### le formulaire de delete d'un trainer

- déjà vu le code du formulaire, cependant celui-ci est refactoré dans un fichier _form_delete.html.twig
  
Les imports dans vos templates twig se feront comme suit :

```twig
{% include 'admin/trainer/partials/_form_delete.html.twig' with {'id': trainer.id } %}
```

```html
<!-- dans le dossier partials/_form_delete.html.twig -->
<form 
    data-controller="confirm"
    action="{{ path('delete_trainer', {id: id}) }}" 
    method="post" 
    style="display:inline;">
    
    <input type="hidden" name="_token" value="{{ csrf_token('delete' ~ id) }}">
    
    <button data-action="click->confirm#next" type="submit" class="btn btn-danger btn-sm">Delete</button>
  
</form>
```

1. **Balise `<form>`**:
   - `data-controller="confirm"` : Cette ligne indique l'utilisation d'un contrôleur JavaScript nommé "confirm". Cela suggère que vous utilisez probablement Stimulus pour gérer des comportements interactifs côté client.

2. **Champ `_token`** :
   - `<input type="hidden" name="_token" value="{{ csrf_token('delete' ~ id) }}">` : C'est un champ caché qui inclut le jeton CSRF (Cross-Site Request Forgery) généré par Symfony. Il est utilisé pour protéger le formulaire contre les attaques CSRF. Le jeton est généré en concaténant le mot-clé `'delete'` avec l'ID du trainer, assurant ainsi un jeton unique pour chaque formulaire de suppression.

### Fonctionnement général

Lorsque l'utilisateur clique sur le bouton "Delete", le formulaire est soumis en utilisant la méthode POST vers l'URL définie par `action`. Le champ `_token` garantit la sécurité CSRF. Le contrôleur JavaScript `confirm` (implémenté avec Stimulus) intercepte l'événement de clic et peut afficher une boîte de dialogue de confirmation à l'aide d'une bibliothèque comme SweetAlert2 ou simplement avec JavaScript natif. 

## Code Expliqué JS pour la confirmation de la suppression

```javascript
// assets/confirm_controller.js
import { Controller } from '@hotwired/stimulus';
import Swal from 'sweetalert2';

export default class extends Controller {

    // on montage 
    connect() {
        console.log('🐉');
    }

    next(e) {
        e.preventDefault(); // Empêche le comportement par défaut du lien ou du formulaire
        
        // Affiche une boîte de dialogue SweetAlert2
        Swal.fire({
            title: 'Are you sure little Padawan La Passerelle ?',
            text: "You won't be able to revert trainer!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!',
        }).then((result) => {
            if (result.isConfirmed) { // Si l'utilisateur clique sur le bouton de confirmation
                Swal.fire(
                    'Deleted!',
                    'Your trainer has been deleted.',
                    'success',
                );

                this.element.submit(); // Soumet le formulaire associé au contrôleur
            }
        });
    }
}
```

## Explication Ligne par Ligne

1. **Imports**:
   - `import { Controller } from '@hotwired/stimulus';` : Importe le contrôleur de Stimulus pour définir un nouveau comportement.
   - `import Swal from 'sweetalert2';` : Importe SweetAlert2 pour afficher des boîtes de dialogue.

2. **Définition du Contrôleur** (`export default class extends Controller`):
   - Étend la classe `Controller` de Stimulus pour créer un nouveau comportement.
   
3. **Méthode `connect()`**:
   - Cette méthode est appelée lorsque le contrôleur est connecté à un élément HTML. Ici, elle affiche simplement un message dans la console lorsque le contrôleur est initialisé.

4. **Méthode `next(e)`**:
   - Cette méthode est déclenchée lorsqu'un événement (probablement un clic sur un lien ou un bouton) est intercepté.
   - `e.preventDefault();` : Empêche le comportement par défaut de l'événement (comme la soumission d'un formulaire ou le suivi d'un lien).
   - `Swal.fire({ ... })` : Affiche une boîte de dialogue modale avec des options personnalisées (titre, texte, icône, boutons).
   - `.then((result) => { ... })` : Exécute du code après que l'utilisateur a interagi avec la boîte de dialogue.
   - `if (result.isConfirmed) { ... }` : Vérifie si l'utilisateur a cliqué sur le bouton de confirmation dans la boîte de dialogue.
   - `Swal.fire('Deleted!', 'Your trainer has been deleted.', 'success');` : Affiche une autre boîte de dialogue pour informer l'utilisateur que l'action a été effectuée avec succès.
   - `this.element.submit();` : Soumet le formulaire associé à l'élément contrôlé par Stimulus.
