# Module 01 — Lab basique : Premiers pas avec les conteneurs

> **Niveau :** Débutant  
> **Durée estimée :** 20 minutes  
> **Prérequis :** Docker Desktop installé et démarré

---

## 🎯 Objectifs

- Lancer votre premier conteneur
- Comprendre la différence entre une image et un conteneur
- Utiliser les commandes Docker de base

---

## Étape 1 — Vérifier que Docker fonctionne

Ouvrez un terminal (PowerShell sur Windows, Terminal sur Mac) et tapez :

```bash
docker --version
```

**Résultat attendu :**
```
Docker version 24.x.x, build ...
```

Si vous voyez un message d'erreur, assurez-vous que Docker Desktop est bien démarré (icône dans la barre des tâches).

---

## Étape 2 — Lancer votre premier conteneur

```bash
docker run hello-world
```

Docker va :
1. Chercher l'image `hello-world` sur votre machine (elle n'y est pas encore)
2. La télécharger automatiquement depuis Docker Hub
3. Créer un conteneur et l'exécuter

**Résultat attendu :** Un message "Hello from Docker!" s'affiche.

> 💡 **Ce qui vient de se passer :** Docker a téléchargé une *image* (un modèle), créé un *conteneur* à partir de cette image, l'a exécuté, puis le conteneur s'est arrêté tout seul.

---

## Étape 3 — Lancer un serveur web Nginx

```bash
docker run -d -p 8080:80 --name mon-serveur-web nginx
```

**Explication des options :**
- `-d` : exécuter en arrière-plan (mode détaché)
- `-p 8080:80` : connecter le port 8080 de votre machine au port 80 du conteneur
- `--name mon-serveur-web` : donner un nom lisible au conteneur
- `nginx` : le nom de l'image à utiliser

Ouvrez votre navigateur et allez sur : **http://localhost:8080**

**Résultat attendu :** La page d'accueil de Nginx s'affiche.

---

## Étape 4 — Voir les conteneurs en cours d'exécution

```bash
docker ps
```

**Résultat attendu :**
```
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS                  NAMES
abc123...      nginx   ...       ...       Up ...   0.0.0.0:8080->80/tcp   mon-serveur-web
```

Pour voir **tous** les conteneurs (y compris les arrêtés) :

```bash
docker ps -a
```

---

## Étape 5 — Arrêter et supprimer le conteneur

```bash
# Arrêter le conteneur
docker stop mon-serveur-web

# Supprimer le conteneur
docker rm mon-serveur-web
```

Vérifiez qu'il n'est plus là :
```bash
docker ps -a
```

---

## Étape 6 — Lister les images téléchargées

```bash
docker images
```

Vous devriez voir `hello-world` et `nginx` dans la liste.

---

## ✅ Récapitulatif des commandes apprises

| Commande | Action |
|----------|--------|
| `docker run <image>` | Télécharger et démarrer un conteneur |
| `docker run -d` | Démarrer en arrière-plan |
| `docker run -p hôte:conteneur` | Exposer un port |
| `docker ps` | Voir les conteneurs actifs |
| `docker ps -a` | Voir tous les conteneurs |
| `docker stop <nom>` | Arrêter un conteneur |
| `docker rm <nom>` | Supprimer un conteneur |
| `docker images` | Lister les images locales |

---

## 🧹 Nettoyage

```bash
docker rm $(docker ps -aq)   # Supprimer tous les conteneurs arrêtés
```

---

➡️ **Suivant :** [Lab fil rouge — Découverte du IT-Support Portal](../lab-fil-rouge/README.md)
