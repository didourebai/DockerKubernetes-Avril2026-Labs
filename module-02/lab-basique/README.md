# Module 02 — Lab basique : Images Docker et CLI

> **Niveau :** Débutant  
> **Durée estimée :** 25 minutes  
> **Prérequis :** Module 01 terminé

---

## 🎯 Objectifs

- Comprendre la différence image / conteneur
- Utiliser Docker Hub pour trouver des images
- Maîtriser les commandes Docker CLI essentielles
- Entrer dans un conteneur et l'inspecter

---

## Étape 1 — Chercher une image sur Docker Hub

Docker Hub est le registre public d'images Docker. Cherchez depuis le terminal :

```bash
docker search nginx
```

Vous verrez plusieurs résultats. La colonne **OFFICIAL** indique les images maintenues officiellement.

---

## Étape 2 — Télécharger une image sans l'exécuter

```bash
docker pull nginx:1.27-alpine
```

> 💡 `:1.27-alpine` est le **tag** (version). `alpine` indique une image très légère basée sur Alpine Linux.

Vérifiez que l'image est bien téléchargée :

```bash
docker images
```

Comparez la taille de `nginx:latest` et `nginx:1.27-alpine` — la version alpine est beaucoup plus petite.

---

## Étape 3 — Inspecter une image

```bash
docker inspect nginx:1.27-alpine
```

Cherchez dans la sortie :
- `"Os"` : système d'exploitation
- `"Architecture"` : processeur cible
- `"ExposedPorts"` : ports déclarés

---

## Étape 4 — Voir l'historique des couches d'une image

```bash
docker history nginx:1.27-alpine
```

Chaque ligne est une **couche** de l'image. La colonne `SIZE` montre la taille ajoutée par chaque instruction.

---

## Étape 5 — Lancer un conteneur avec différentes options

```bash
# Option 1 : mode interactif (vous entrez dans le conteneur)
docker run -it --rm nginx:1.27-alpine sh

# Dans le conteneur, explorez :
ls /etc/nginx/       # Configuration Nginx
cat /etc/nginx/nginx.conf   # Fichier de configuration
nginx -v             # Version de Nginx
exit                 # Quitter
```

> 💡 `--rm` supprime automatiquement le conteneur quand vous quittez.

```bash
# Option 2 : mode détaché avec nom
docker run -d -p 8080:80 --name nginx-test nginx:1.27-alpine

# Tester
curl http://localhost:8080
# ou ouvrir http://localhost:8080 dans votre navigateur
```

---

## Étape 6 — Exécuter une commande dans un conteneur actif

```bash
# Voir les processus dans le conteneur
docker exec nginx-test ps aux

# Voir les fichiers de configuration
docker exec nginx-test ls /etc/nginx/conf.d/

# Entrer en mode interactif
docker exec -it nginx-test sh
```

---

## Étape 7 — Voir les statistiques d'utilisation

```bash
docker stats nginx-test
```

Appuyez sur `Ctrl+C` pour quitter. Vous voyez en temps réel : CPU, mémoire, réseau.

---

## Étape 8 — Copier des fichiers vers/depuis un conteneur

```bash
# Créer un fichier HTML de test
echo "<h1>Bonjour depuis mon lab!</h1>" > test.html

# Copier dans le conteneur
docker cp test.html nginx-test:/usr/share/nginx/html/test.html

# Vérifier dans le navigateur
# http://localhost:8080/test.html
```

---

## Étape 9 — Nettoyer

```bash
docker stop nginx-test
docker rm nginx-test
docker rmi nginx:1.27-alpine   # Supprimer l'image (optionnel)
```

---

## ✅ Récapitulatif des commandes

| Commande | Action |
|----------|--------|
| `docker search <terme>` | Chercher sur Docker Hub |
| `docker pull <image>:<tag>` | Télécharger une image |
| `docker images` | Lister les images locales |
| `docker inspect <image>` | Détails d'une image |
| `docker history <image>` | Couches d'une image |
| `docker run -it --rm` | Mode interactif temporaire |
| `docker exec -it <conteneur> sh` | Entrer dans un conteneur actif |
| `docker stats <conteneur>` | Statistiques en temps réel |
| `docker cp <fichier> <conteneur>:<chemin>` | Copier un fichier |
| `docker rmi <image>` | Supprimer une image |

---

➡️ **Suivant :** [Lab fil rouge — Containerisation du portail](../lab-fil-rouge/README.md)
