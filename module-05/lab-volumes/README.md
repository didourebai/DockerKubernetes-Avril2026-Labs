# Lab Volumes Docker -- Comprendre la persistance des données

> **Niveau :** Débutant
> **Durée estimée :** 30 minutes
> **Prérequis :** Module 02 terminé (docker run, docker ps)

---

## Le problème que les volumes résolvent

Un conteneur est comme un Post-it : quand vous l'effacez, tout disparait.

**Démonstration du problème :**

```bash
# Lancer un conteneur et créer un fichier dedans
docker run -it --name test-ephemere alpine sh
```

Dans le conteneur, tapez :
```sh
echo "Bonjour, je suis un fichier important !" > /data/mon-fichier.txt
cat /data/mon-fichier.txt
exit
```

Maintenant supprimez et recréez le conteneur :

**Windows (PowerShell) :**
```powershell
docker rm test-ephemere
docker run -it --name test-ephemere alpine sh
```

**Mac / Linux :**
```bash
docker rm test-ephemere
docker run -it --name test-ephemere alpine sh
```

Dans le nouveau conteneur :
```sh
cat /data/mon-fichier.txt
# Erreur ! Le fichier n'existe plus.
exit
```

> **Conclusion :** Sans volume, les données d'un conteneur disparaissent
> quand le conteneur est supprimé.

---

## Les 3 types de volumes Docker

```
Votre machine (hôte)          Conteneur
--------------------          ---------

Type 1 -- Volume nommé
  Docker gère l'emplacement
  /var/lib/docker/volumes/ --> /data

Type 2 -- Bind Mount
  Vous choisissez l'emplacement
  C:\mon-dossier\          --> /data

Type 3 -- tmpfs (Linux uniquement)
  Stockage en mémoire vive --> /cache
  (disparait à l'arrêt)
```

---

## Étape 1 -- Volume nommé (recommandé pour les données)

Un volume nommé est géré entièrement par Docker.
Vous n'avez pas besoin de savoir où il est stocké.

### Créer un volume

```bash
docker volume create mon-premier-volume
```

### Voir les volumes existants

```bash
docker volume ls
```

**Résultat attendu :**
```
DRIVER    VOLUME NAME
local     mon-premier-volume
```

### Inspecter le volume

```bash
docker volume inspect mon-premier-volume
```

Repérez la ligne `"Mountpoint"` : c'est l'emplacement sur votre machine.

---

### Utiliser le volume dans un conteneur

```bash
docker run -it --name avec-volume -v mon-premier-volume:/data alpine sh
```

**Explication de `-v mon-premier-volume:/data` :**
- `mon-premier-volume` = le volume Docker
- `/data` = le dossier dans le conteneur
- Docker connecte les deux

Dans le conteneur :
```sh
echo "Ces données survivront !" > /data/important.txt
ls /data
exit
```

---

### Vérifier que les données persistent

Supprimez le conteneur et créez-en un nouveau avec le MÊME volume :

**Windows (PowerShell) :**
```powershell
docker rm avec-volume
docker run -it --name nouveau-conteneur -v mon-premier-volume:/data alpine sh
```

**Mac / Linux :**
```bash
docker rm avec-volume
docker run -it --name nouveau-conteneur -v mon-premier-volume:/data alpine sh
```

Dans le nouveau conteneur :
```sh
cat /data/important.txt
# Ces données survivront !   <-- TOUJOURS LÀ !
exit
```

> **Résultat :** Le fichier est toujours présent malgré la suppression
> du conteneur. Le volume a survécu.

---

## Étape 2 -- Bind Mount (recommandé pour le développement)

Un bind mount connecte un dossier de VOTRE machine directement
dans le conteneur. Vous voyez les fichiers des deux côtés.

### Créer un dossier de test

**Windows (PowerShell) :**
```powershell
mkdir C:\docker-test
echo "Fichier créé depuis Windows" > C:\docker-test\windows.txt
```

**Mac / Linux :**
```bash
mkdir ~/docker-test
echo "Fichier créé depuis le terminal" > ~/docker-test/test.txt
```

### Monter le dossier dans un conteneur

**Windows (PowerShell) :**
```powershell
docker run -it --name bind-test -v C:\docker-test:/data alpine sh
```

**Mac / Linux :**
```bash
docker run -it --name bind-test -v ~/docker-test:/data alpine sh
```

Dans le conteneur :
```sh
ls /data
# Vous voyez le fichier créé depuis votre machine !

cat /data/test.txt
# ou cat /data/windows.txt

# Créer un fichier depuis le conteneur
echo "Fichier créé depuis le conteneur" > /data/depuis-conteneur.txt

exit
```

### Vérifier depuis votre machine

**Windows (PowerShell) :**
```powershell
dir C:\docker-test
type C:\docker-test\depuis-conteneur.txt
```

**Mac / Linux :**
```bash
ls ~/docker-test
cat ~/docker-test/depuis-conteneur.txt
```

> **Résultat :** Le fichier créé dans le conteneur est visible
> sur votre machine. C'est le même dossier partagé en temps réel.

---

## Étape 3 -- Cas concret : base de données avec volume

Sans volume, une base de données perd toutes ses données à chaque redémarrage.
Voici comment sauvegarder les données d'une base SQLite.

```bash
docker run -d \
  --name ma-base \
  -v mon-premier-volume:/app/data \
  -e APP_ENV=production \
  python:3.12-slim \
  python3 -c "
import sqlite3, os, time
os.makedirs('/app/data', exist_ok=True)
conn = sqlite3.connect('/app/data/ecole.db')
conn.execute('CREATE TABLE IF NOT EXISTS serveurs (id INTEGER PRIMARY KEY, nom TEXT, statut TEXT)')
conn.execute(\"INSERT INTO serveurs (nom, statut) VALUES ('Serveur-Web-01', 'actif')\")
conn.execute(\"INSERT INTO serveurs (nom, statut) VALUES ('NAS-01', 'actif')\")
conn.commit()
print('Base de données créée dans /app/data/ecole.db')
for row in conn.execute('SELECT * FROM serveurs'):
    print(row)
conn.close()
"
```

Voir les logs :
```bash
docker logs ma-base
```

Supprimer le conteneur mais PAS le volume :
```bash
docker rm ma-base
```

Relancer avec le même volume :

**Windows (PowerShell) :**
```powershell
docker run --rm -v mon-premier-volume:/app/data python:3.12-slim python3 -c "
import sqlite3
conn = sqlite3.connect('/app/data/ecole.db')
print('Données retrouvées apres suppression du conteneur :')
for row in conn.execute('SELECT * FROM serveurs'):
    print(row)
conn.close()
"
```

**Mac / Linux :**
```bash
docker run --rm -v mon-premier-volume:/app/data python:3.12-slim python3 -c "
import sqlite3
conn = sqlite3.connect('/app/data/ecole.db')
print('Données retrouvées apres suppression du conteneur :')
for row in conn.execute('SELECT * FROM serveurs'):
    print(row)
conn.close()
"
```

> **Résultat :** La base de données est intacte malgré la suppression
> du conteneur. C'est exactement ce qui se passe avec MySQL, PostgreSQL, etc.

---

## Étape 4 -- Partager un volume entre deux conteneurs

Un volume peut être monté dans plusieurs conteneurs en même temps.
Exemple : un conteneur écrit, un autre lit.

```bash
# Conteneur 1 : écrit dans le volume
docker run -d --name ecrivain \
  -v partage:/data \
  alpine sh -c "while true; do echo \"$(date)\" >> /data/journal.log; sleep 2; done"
```

**Windows (PowerShell) :**
```powershell
# Conteneur 2 : lit le volume en temps réel
docker run -it --name lecteur -v partage:/data alpine sh
```

**Mac / Linux :**
```bash
# Conteneur 2 : lit le volume en temps réel
docker run -it --name lecteur -v partage:/data alpine sh
```

Dans le conteneur lecteur :
```sh
# Voir le fichier grossir en temps réel
tail -f /data/journal.log
# Ctrl+C pour arrêter
exit
```

---

## Étape 5 -- Sauvegarder et restaurer un volume

### Sauvegarder le contenu d'un volume dans un fichier ZIP

**Windows (PowerShell) :**
```powershell
docker run --rm -v mon-premier-volume:/data -v ${PWD}:/backup alpine tar czf /backup/sauvegarde-volume.tar.gz -C /data .
```

**Mac / Linux :**
```bash
docker run --rm -v mon-premier-volume:/data -v $(pwd):/backup alpine tar czf /backup/sauvegarde-volume.tar.gz -C /data .
```

Vérifier que le fichier de sauvegarde existe :

**Windows (PowerShell) :**
```powershell
dir sauvegarde-volume.tar.gz
```

**Mac / Linux :**
```bash
ls -lh sauvegarde-volume.tar.gz
```

### Restaurer dans un nouveau volume

```bash
docker volume create volume-restaure
```

**Windows (PowerShell) :**
```powershell
docker run --rm -v volume-restaure:/data -v ${PWD}:/backup alpine tar xzf /backup/sauvegarde-volume.tar.gz -C /data
```

**Mac / Linux :**
```bash
docker run --rm -v volume-restaure:/data -v $(pwd):/backup alpine tar xzf /backup/sauvegarde-volume.tar.gz -C /data
```

---

## Nettoyage

```bash
# Supprimer les conteneurs
docker rm -f ecrivain lecteur bind-test nouveau-conteneur test-ephemere 2>nul

# Supprimer les volumes
docker volume rm mon-premier-volume partage volume-restaure

# Supprimer les dossiers de test
```

**Windows (PowerShell) :**
```powershell
Remove-Item -Recurse -Force C:\docker-test
```

**Mac / Linux :**
```bash
rm -rf ~/docker-test
```

---

## Récapitulatif -- Quand utiliser quoi ?

| Situation | Type de volume | Commande |
|-----------|---------------|----------|
| Base de données (MySQL, SQLite) | Volume nommé | `-v mon-volume:/var/lib/mysql` |
| Code source en développement | Bind Mount | `-v $(pwd):/app` |
| Partager des fichiers entre conteneurs | Volume nommé | Même `-v mon-volume:/data` sur chaque conteneur |
| Fichiers temporaires sensibles | tmpfs | `--tmpfs /tmp` |
| Garder les logs | Volume nommé | `-v logs-volume:/var/log` |

---

## Les erreurs courantes

**Erreur : le dossier est vide dans le conteneur**
- Cause : le chemin du bind mount est incorrect
- Solution : vérifier que le dossier existe sur votre machine avant de lancer le conteneur

**Erreur : Permission denied**
- Cause : le conteneur tourne avec un utilisateur différent
- Solution : ajouter `:z` ou `:Z` à la fin du mount sur Linux (SELinux)

**Erreur : le volume n'est pas supprimé avec `docker rm`**
- C'est normal ! Un volume survit à la suppression du conteneur.
- Pour supprimer aussi le volume : `docker rm -v mon-conteneur`
- Pour tout nettoyer : `docker volume prune`

---

Suite : [Lab fil rouge -- Module 05](../lab-fil-rouge/README.md)
