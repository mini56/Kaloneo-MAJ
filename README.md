# KALONÉO — Mises à jour Windows

Ce dépôt sert **uniquement à distribuer les mises à jour de KALONÉO**.
Les installateurs sont compilés et testés séparément, puis copiés ici après
vérification de leur empreinte SHA-256. Aucune compilation du logiciel n'a lieu dans ce dépôt.

## Fichiers officiels à télécharger

Pour chaque version, seuls **deux fichiers** sont publiés par notre système :

- `KALONEO-Setup-<version>.exe` : l'installateur Windows ;
- `KALONEO-Setup-<version>.exe.sha256` : son empreinte de vérification.

**[Consulter les mises à jour KALONÉO](https://github.com/mini56/Kaloneo-MAJ/releases)**

### Pourquoi GitHub affiche aussi « Source code » ?

GitHub ajoute **automatiquement** les liens `Source code (zip)` et
`Source code (tar.gz)` à chaque Release, sans possibilité de les retirer.
Ces archives contiennent uniquement les fichiers du **présent dépôt de
distribution** (ce README et son workflow technique), **pas le code source
de l'application KALONÉO**. Elles ne sont ni des installateurs ni des
fichiers à télécharger pour une mise à jour.

L'installation est protégée par le mot de passe d'installation prévu.
La vérification d'une mise à jour nécessite Internet ; l'évaluation des
candidats reste utilisable hors connexion.

**Confidentialité :** dépôt public, sans dossiers candidats, données
personnelles, mot de passe ni archives privées.

## Compilation privée et synchronisation des Releases

Le dépôt de développement `mini56/Kaloneo` peut rester privé. Dans ce cas,
le jeton GitHub automatique du **présent dépôt public** ne peut pas lire
directement les Releases du dépôt privé.

Pour autoriser la copie automatique des futures versions, le propriétaire
du dépôt `Kaloneo-MAJ` doit créer dans **Settings → Secrets and variables
→ Actions** un secret de dépôt nommé `KALONEO_SOURCE_READ_TOKEN`.
Sa valeur doit être un **jeton GitHub fine-grained**, autorisé uniquement
sur `mini56/Kaloneo`, avec le droit **Contents: Read-only** (et Metadata:
Read-only, accordé automatiquement). Ne jamais placer ce jeton dans le code,
un fichier README, une Release ou un journal.

Le workflow de copie utilise ce secret lorsqu'il est disponible ; sinon il
utilise le jeton standard pour les Releases publiques. Les contrôles du
SHA256, des deux fichiers officiels et de la possibilité de télécharger
le Setup restent obligatoires dans les deux cas.

La compilation Windows se déroule uniquement sur le dépôt principal.
Un échec de synchronisation ne retire pas les versions déjà publiées,
mais les nouveaux Setup restent indisponibles pour les mises à jour
intégrées jusqu'à la résolution du problème.
