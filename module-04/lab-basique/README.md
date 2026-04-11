# Module 04 — Lab basique : Optimisation des builds Docker

> **Niveau :** Débutant  
> **Durée estimée :** 25 minutes

---

## 🎯 Objectifs

- Utiliser BuildKit pour des builds plus rapides
- Comprendre et exploiter le cache
- Utiliser `docker init` pour générer un Dockerfile automatiquement
- Analyser la sécurité d'une image avec Docker Scout

---

## Étape 1 — Activer BuildKit

BuildKit est le moteur de build moderne de Docker. Il est activé par défaut depuis Docker Desktop 4.x, mais vous pouvez le forcer :

```bash
# Vérifier la version de Docker
docker --version

# Activer BuildKit pour une commande
DOCKER_BUILDKIT=1 docker build -t test .

# Ou utiliser la commande moderne (recommandée)
docker buildx build -t test .
```

---

## Étape 2 — Mesurer la différence de vitesse

Créez un `Dockerfile` de test :

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir flask gunicorn
COPY . .
CMD ["python", "app.py"]
```

Créez un `requirements.txt` minimaliste :
```
flask==3.0.3
gunicorn==22.0.0
```

**Premier build (sans cache) :**
```bash
docker build --no-cache -t speed-test:v1 .
```

**Deuxième build (avec cache) :**
```bash
docker build -t speed-test:v1 .
```

Comparez les temps. Le deuxième est **beaucoup plus rapide** grâce au cache.

---

## Étape 3 — L'ordre des instructions compte !

Comparez ces deux Dockerfiles :

**Mauvais ordre (invalidation du cache à chaque changement de code) :**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .                           # ← Tout est copié ici
RUN pip install -r requirements.txt  # ← Réinstallé à chaque build !
CMD ["python", "app.py"]
```

**Bon ordre (cache intelligent) :**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .            # ← Seulement les dépendances
RUN pip install -r requirements.txt  # ← Mis en cache si requirements.txt n'a pas changé
COPY . .                           # ← Code copié en dernier
CMD ["python", "app.py"]
```

> 💡 **Règle :** Placez ce qui change **rarement** en premier, ce qui change **souvent** en dernier.

---

## Étape 4 — docker init (génération automatique)

`docker init` génère automatiquement un Dockerfile adapté à votre projet :

```bash
mkdir test-init
cd test-init

# Créer un fichier Python simple
echo "print('Hello Docker!')" > main.py

# Laisser Docker détecter et générer le Dockerfile
docker init
```

Suivez les questions interactives. Docker va détecter que c'est un projet Python et générer :
- Un `Dockerfile` optimisé
- Un `docker-compose.yml`
- Un `.dockerignore`

Examinez les fichiers générés — comparez avec ce que vous avez écrit manuellement.

---

## Étape 5 — Analyser la sécurité avec Docker Scout

Docker Scout détecte les vulnérabilités dans vos images :

```bash
# Analyser une image (nécessite un compte Docker Hub)
docker scout quickview it-portal:v2

# Voir les vulnérabilités détaillées
docker scout cves it-portal:v2

# Obtenir des recommandations
docker scout recommendations it-portal:v2
```

> 💡 Si vous n'avez pas de compte Docker Hub, vous pouvez analyser une image publique :
> ```bash
> docker scout quickview nginx:latest
> ```

---

## Étape 6 — Build Check : valider la qualité du Dockerfile

```bash
# Vérifier le Dockerfile avant de construire
docker buildx build --check .
```

Cette commande détecte les problèmes courants :
- Utilisation de `FROM ubuntu:latest` sans version fixe
- `ADD` au lieu de `COPY`
- Exécution en `root`
- `RUN apt-get update` sans `apt-get install` dans la même couche

---

## 🧹 Nettoyage

```bash
docker rmi speed-test:v1
cd ..
rm -rf test-init
```

---

## ✅ Récapitulatif

| Outil / Commande | Utilité |
|------------------|---------|
| `docker buildx build` | Build moderne avec BuildKit |
| `docker init` | Génération automatique du Dockerfile |
| `docker scout quickview` | Résumé de sécurité |
| `docker scout cves` | Vulnérabilités détaillées |
| `docker buildx build --check` | Validation du Dockerfile |
| `--no-cache` | Forcer un build complet |

---

➡️ **Suivant :** [Lab fil rouge — Portail v3 avec BuildKit](../lab-fil-rouge/README.md)
