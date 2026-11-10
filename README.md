# Jumbong.github.io

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
