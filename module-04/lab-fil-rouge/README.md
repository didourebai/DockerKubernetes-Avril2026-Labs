# Module 04 — Lab fil rouge : IT-Support Portal v3 — Build optimisé

> **Niveau :** Débutant | **Durée estimée :** 20 minutes

## 🎯 Objectif
Améliorer le build avec cache BuildKit, Build Checks et Docker Scout.

## Étape 1 — Valider le Dockerfile avant de builder

```bash
cd labs/module-04/lab-fil-rouge
docker buildx build --check .
```

## Étape 2 — Builder avec cache BuildKit

```bash
docker buildx build --build-arg VERSION=3.0.0 --build-arg BUILD_DATE=$(date +%Y-%m-%d) -t it-portal:v3 .
```

Modifiez un texte dans `app.py` et rebuilder — l'étape `pip install` est instantanée grâce au cache.

## Étape 3 — Analyser la sécurité

```bash
docker login
docker scout quickview it-portal:v3
docker scout recommendations it-portal:v3
```

## Étape 4 — Lancer et tester

```bash
docker run -d -p 8080:5000 --name it-portal-v3 -e APP_ENV=production -e APP_VERSION=3.0.0 it-portal:v3
```

Ouvrez **http://localhost:8080** — version affichée : **3.0.0**

## Étape 5 — Comparer toutes les versions

```bash
docker images | grep it-portal
```

| Version | Module | Nouveautés |
|---------|--------|-----------|
| v1.0 | 02 | Dockerfile simple |
| v2.0 | 03 | Multi-stage, non-root, healthcheck |
| **v3.0** | **04** | **Cache BuildKit, Build Checks, Scout** |

## 🧹 Nettoyage

```bash
docker stop it-portal-v3 && docker rm it-portal-v3
```

---
➡️ **Suivant :** [Module 05](../../module-05/lab-basique/README.md)
