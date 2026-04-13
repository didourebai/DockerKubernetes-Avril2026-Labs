# Module 03 — Lab fil rouge : Build multi-étape du IT-Support Portal

> **Niveau :** Débutant  
> **Durée estimée :** 25 minutes


> **Note Windows PowerShell :**
> - `| grep X`  ->  `| findstr X`
> - `$(date +%Y-%m-%d)`  ->  `$(Get-Date -Format "yyyy-MM-dd")`
> - `$(pwd)`  ->  `${PWD}`
> - `commande1 && commande2`  ->  deux lignes separees

---

## 🎯 Objectif

Améliorer le Dockerfile du portail avec :
- Un **build en deux étapes** (multi-stage)
- L'utilisateur **non-root** (sécurité)
- Le fichier **.dockerignore**
- Des **métadonnées** sur l'image

---

## Contexte : pourquoi deux étapes ?

Dans le module 02, notre Dockerfile était simple mais l'image finale contenait des outils inutiles en production (pip, etc.).

Un **build multi-stage** sépare :
1. **Étape de build** : on installe tout ce qu'il faut pour compiler/préparer
2. **Étape d'exécution** : image finale légère, juste ce qu'il faut pour tourner

---

## Étape 1 — Créer le .dockerignore

```bash
cd labs/module-03/lab-fil-rouge
```

Créez le fichier `.dockerignore` :

```
__pycache__
*.pyc
*.pyo
.git
.gitignore
*.md
.DS_Store
.env
```

---

## Étape 2 — Le nouveau Dockerfile multi-stage

Examinez le `Dockerfile` fourni dans ce dossier :

```dockerfile
# ============================================================
# ÉTAPE 1 : Installation des dépendances
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /install

# Copier uniquement le fichier de dépendances (optimise le cache)
COPY requirements.txt .

# Installer dans un dossier séparé
RUN pip install --no-cache-dir --prefix=/deps -r requirements.txt


# ============================================================
# ÉTAPE 2 : Image finale d'exécution
# ============================================================
FROM python:3.12-slim AS final

# Métadonnées de l'image
ARG VERSION=2.0.0
ARG BUILD_DATE
LABEL maintainer="it-support@institution.ca"
LABEL version="${VERSION}"
LABEL description="IT-Support Portal — Portail de surveillance IT"

# Dossier de travail
WORKDIR /app

# Copier les dépendances installées à l'étape 1
COPY --from=builder /deps /usr/local

# Copier le code de l'application
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Créer un utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Variables d'environnement par défaut
ENV APP_ENV=production
ENV APP_VERSION=${VERSION}
ENV PORT=5000

# Port exposé
EXPOSE 5000

# Vérification de santé (utile pour Kubernetes plus tard)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Démarrage avec gunicorn (serveur de production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

---

## Étape 3 — Construire l'image optimisée

```bash
docker build --build-arg VERSION=2.0.0 --build-arg BUILD_DATE=$(Get-Date -Format "yyyy-MM-dd") -t it-portal:v2 .
```

---

## Étape 4 — Comparer les tailles

```bash
docker images | findstr it-portal
```

**Résultat attendu :**
```
it-portal   v2   ...   xxx MB   ← Version optimisée
it-portal   v1   ...   xxx MB   ← Version module 02
```

> 💡 La différence peut être minime ici avec Python, mais sur des applications Java ou Node.js, le gain est souvent de 500 Mo à 1 Go.

---

## Étape 5 — Lancer la version de production

```bash
docker run -d -p 8080:5000 --name it-portal-v2 -e APP_ENV=production -e APP_VERSION=2.0.0 it-portal:v2
```

Ouvrez : **http://localhost:8080**

Vérifiez dans le portail que l'environnement affiche bien **"production"**.

---

## Étape 6 — Vérifier que l'utilisateur est non-root

```bash
docker exec it-portal-v2 whoami
```

**Résultat attendu :** `appuser` (et non `root`)

> 💡 **Sécurité :** Si un attaquant réussit à compromettre l'application, il se retrouve avec les droits limités de `appuser`, pas avec les droits `root`.

---

## Étape 7 — Tester le health check

```bash
docker inspect --format='{{json .State.Health}}' it-portal-v2
```

Le conteneur surveille lui-même sa santé toutes les 30 secondes.

---

## 🧹 Nettoyage

```bash
docker stop it-portal-v2
docker rm it-portal-v2
```

---

## 📝 Évolution du portail

| Version | Module | Nouveautés |
|---------|--------|-----------|
| v1.0 | Module 02 | Dockerfile simple |
| **v2.0** | **Module 03** | **Multi-stage, non-root, healthcheck, gunicorn** |

---

## 🔮 Dans le prochain module

Vous allez apprendre à **optimiser encore plus** les builds avec BuildKit, et à ajouter une **base de données** au portail.

---

➡️ **Retour :** [Lab basique](../lab-basique/README.md) | **Suivant :** [Module 04](../../module-04/lab-basique/README.md)
