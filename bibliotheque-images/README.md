# Bibliothèque d’images KALONÉO — fonctionnement automatique

## Pour ajouter des images

1. Ouvrir le dossier [originaux](./originaux) sur GitHub.
2. Cliquer sur **Add file → Upload files** et déposer des images PNG, JPG, WebP, GIF ou BMP. On peut envoyer plusieurs images à la fois.
3. Valider le dépôt sur la branche `main`. **GitHub Actions génère automatiquement les miniatures et le catalogue.**

Pour classer les images par thème, les placer dans un sous-dossier de `originaux/` nommé `horloges`, `metiers`, `outils`, `transports`, `calcul`, `puzzles`, `documents` ou `divers`. Les images déposées directement dans `originaux/` seront classées dans `divers`.

**Ne pas** modifier `catalogue.json` ni créer les miniatures manuellement. La suppression d'un original provoque la suppression de sa miniature et de son entrée du catalogue lors du prochain traitement.

Si aucun fichier n'apparaît après dépôt, vérifier l'onglet **Actions** du dépôt et les autorisations de GitHub Actions en écriture (Settings → Actions → General → Workflow permissions). Un lancement manuel est aussi possible via **Actions → Bibliothèque images - miniatures et catalogue → Run workflow**.

## Technique

- Miniatures WebP 240 × 240 px maximum (proportions conservées), créées par Pillow.
- Catalogue `catalogue.json` enrichi automatiquement (titre, catégorie, chemin de l'original, chemin de la miniature, SHA-256, taille).
- Formats originaux autorisés : PNG, JPEG, WebP, GIF, BMP ; taille maximale de 30 Mio chacun.
- Identifiants fondés sur le dossier de catégorie et le nom du fichier ; éviter les noms identiques dans une catégorie.
- Les fichiers sont publics sur GitHub : n'y déposer que des images redistribuables, sans données personnelles.
- Le workflow ne modifie **ni les Releases ni les installateurs**. Il ne relie pas encore le programme KALONÉO au catalogue.

**Catalogue public :** https://raw.githubusercontent.com/mini56/Kaloneo-MAJ/main/bibliotheque-images/catalogue.json

**Important :** la bibliothèque reste vide jusqu'à l'ajout des premières images. Le Builder devra ultérieurement télécharger les miniatures pour prévisualisation et les originaux sélectionnés à la demande.
