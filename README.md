# Jumbong.github.io

## Publications Towards Data Science

Dans l’onglet **Actions** du dépôt, **Publier le site et actualiser les
articles** permet de consulter les exécutions ou de lancer une synchronisation
manuelle avec **Run workflow**.

Le workflow vérifie chaque jour le flux RSS du profil Towards Data Science. Il
ajoute les titres, dates, extraits et liens des nouveaux articles à
`publications.yml`. Le catalogue conserve les entrées et les résumés existants.
GitHub Pages publie le dossier `docs/` après le rendu des pages qui utilisent
le catalogue. Pour les autres pages, garder le rendu Quarto habituel avant
d’envoyer le dossier `docs/` sur `main`.

Lorsque le flux RSS direct est inaccessible, le workflow lit le même flux
public via RSS2JSON, qui transmet les dix entrées les plus récentes. Si un
article sort du flux avant d’être importé, l’ajouter dans `publications.yml`.
GitHub désactive aussi les exécutions planifiées après 60 jours d’inactivité
du dépôt public. Le workflow peut être réactivé dans l’onglet **Actions**.

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
