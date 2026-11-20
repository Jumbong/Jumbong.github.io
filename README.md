# Jumbong.github.io

## Publications Towards Data Science

Sur GitHub, choisir **Settings → Pages → Source → GitHub Actions**. Une fois
le workflow présent sur `main`, lancer **Publier le site et actualiser les
articles** depuis l’onglet **Actions** pour effectuer la première synchronisation.

Le workflow vérifie chaque jour le flux RSS du profil Towards Data Science. Il
ajoute les titres, dates, extraits et liens des nouveaux articles à
`publications.yml`. Le catalogue conserve les entrées et les résumés existants.
GitHub Pages publie le dossier `docs/` après le rendu des pages qui utilisent
le catalogue. Pour les autres pages, garder le rendu Quarto habituel avant
d’envoyer le dossier `docs/` sur `main`.

Le flux contient les 20 publications les plus récentes. Si le workflow est
interrompu suffisamment longtemps pour qu’un article sorte du flux avant d’être
importé, ajouter cet article directement dans `publications.yml`.

## Ouverture progressive des corrections de TD

Les chapitres 3 à 6 sont temporairement désactivés dans la liste
`website.drafts` du fichier `_quarto.yml`. Avec `draft-mode: gone`, Quarto
produit des pages vides, désactive leurs liens et les retire des listes de
l'accueil, de la recherche et du plan du site. Les fichiers sources sont conservés.

Pour rendre un chapitre accessible après sa séance de TD :

1. Retirer uniquement sa ligne de la liste `website.drafts` dans `_quarto.yml`.
2. Exécuter `quarto render --no-clean` à la racine du projet pour conserver
   aussi les ressources déjà publiées dans `docs/`.
3. Publier les fichiers modifiés, notamment le dossier `docs/`, sur GitHub Pages.

Pour désactiver à nouveau un chapitre, remettre son chemin dans la liste puis
refaire le rendu et la publication. Quand tous les chapitres sont ouverts,
supprimer la clé `drafts` et sa liste.

Vérifier le résultat du rendu dans `docs/` avant publication.
Cette mise en attente ne rend pas privés les fichiers sources ni les versions
déjà présentes dans l'historique d'un dépôt public.
