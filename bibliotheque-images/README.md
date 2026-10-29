# Bibliothèque d’images en ligne KALONÉO

Ce dossier est **indépendant des mises à jour du logiciel** et ne contient aucune donnée candidat.

## Organisation

- `catalogue.json` : catalogue public consommable par le Builder KALONÉO.
- `miniatures/` : prévisualisations légères affichées dans le logiciel (WebP conseillé, largeur 240 px).
- `originaux/` : images originales, téléchargées **uniquement à la demande**.

## Ajouter une image

1. Déposer l'image originale dans `originaux/` et sa miniature dans `miniatures/`.
2. Ajouter une entrée dans le tableau `images` de `catalogue.json`. Exemple :

```json
{
  "id": "horloge-01h15",
  "titre": "Horloge 1 h 15",
  "categorie": "horloges",
  "miniature": "miniatures/horloge-01h15.webp",
  "fichier": "originaux/horloge-01h15.png",
  "sha256": "<empreinte SHA-256 réelle de l'original>",
  "taille_octets": 123456
}
```

Les chemins sont relatifs au répertoire `bibliotheque-images/`. Les identifiants doivent être uniques. L'empreinte et la taille doivent être celles du vrai fichier, pas des valeurs d'exemple. Utiliser uniquement des images dont la diffusion est autorisée.

## Intégration future dans le Builder

Le Builder devra lire `catalogue.json`, afficher **seulement les miniatures** pour la consultation, permettre une sélection multiple puis télécharger les originaux choisis. Avant import, vérifier les chemins, la taille, l'empreinte SHA-256 et les doublons. Protéger les téléchargements contre les chemins relatifs malveillants, les fichiers trop gros et les formats non autorisés. Les images locales restent utilisables hors ligne.

**Adresse du catalogue :** `https://raw.githubusercontent.com/mini56/Kaloneo-MAJ/main/bibliotheque-images/catalogue.json`

**État actuel :** structure préparée ; catalogue vide tant qu'aucune image validée n'a été publiée. Ce dossier ne modifie pas le programme KALONÉO et ne déclenche aucun Setup.
