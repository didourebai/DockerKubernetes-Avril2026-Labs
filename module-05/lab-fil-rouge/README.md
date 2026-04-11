# Module 05 — Lab fil rouge : IT-Support Portal v4 — Multi-conteneurs avec Docker Compose

> **Niveau :** Débutant | **Durée estimée :** 35 minutes

## 🎯 Objectif

Ajouter une **base de données SQLite** au portail et orchestrer tous les services avec `docker-compose.yml`.  
Le portail affichera maintenant un **historique des connexions** stocké en base de données.

---

## Architecture de la v4

```
Navigateur  ──────►  Nginx (port 8080)
                           │
                           ▼
                     Python Flask (port 5000)
                           │
                           ▼
                      SQLite (fichier)
                      (volume persistant)
```

---

## Étape 1 — Placez-vous dans le dossier

```bash
cd labs/module-05/lab-fil-rouge
ls
```

Vous verrez :
```
docker-compose.yml
.env
nginx/
  └── nginx.conf
app/
  ├── Dockerfile
  ├── app.py
  ├── requirements.txt
  ├── templates/
  └── static/
```

---

## Étape 2 — Comprendre le docker-compose.yml

Ouvrez et lisez `docker-compose.yml` :

```yaml
version: "3.9"

services:

  # Service 1 : Proxy inverse Nginx (point d'entrée)
  nginx:
    image: nginx:1.27-alpine
    ports:
      - "${NGINX_PORT:-8080}:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks:
      - reseau-portail
    restart: unless-stopped

  # Service 2 : Application Python Flask
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        VERSION: "${APP_VERSION:-4.0.0}"
    environment:
      - APP_ENV=${APP_ENV:-production}
      - APP_VERSION=${APP_VERSION:-4.0.0}
    volumes:
      - portail-data:/app/data
    networks:
      - reseau-portail
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python3", "-c",
             "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3

networks:
  reseau-portail:
    driver: bridge

volumes:
  portail-data:       # Volume persistant pour la base de données
```

> 💡 **`depends_on`** : Nginx attend que l'application soit démarrée avant de se lancer.  
> 💡 **`volumes: portail-data`** : Les données SQLite survivent aux redémarrages du conteneur.

---

## Étape 3 — Lire le fichier .env

```bash
cat .env
```

```
APP_ENV=production
APP_VERSION=4.0.0
NGINX_PORT=8080
```

Ce fichier configure les variables sans toucher au `docker-compose.yml`.

---

## Étape 4 — Lancer tous les services

```bash
docker-compose up -d
```

Docker va :
1. Construire l'image de l'application Flask
2. Télécharger l'image Nginx
3. Créer le réseau `reseau-portail`
4. Créer le volume `portail-data`
5. Démarrer les deux services

---

## Étape 5 — Vérifier que tout fonctionne

```bash
# Voir l'état des services
docker-compose ps

# Voir les logs en temps réel (Ctrl+C pour quitter)
docker-compose logs -f
```

Ouvrez **http://localhost:8080** dans votre navigateur.

---

## Étape 6 — Tester la persistance des données

```bash
# Voir les logs de l'application
docker-compose logs app

# Redémarrer seulement l'application (pas Nginx)
docker-compose restart app

# Les données en base survivent au redémarrage
```

---

## Étape 7 — Tester la résilience

```bash
# Arrêter seulement l'application
docker-compose stop app

# http://localhost:8080 affiche une erreur Nginx (normal)

# Redémarrer l'application
docker-compose start app

# http://localhost:8080 fonctionne à nouveau
```

---

## Étape 8 — Voir l'intérieur du volume

```bash
# Entrer dans le conteneur de l'application
docker-compose exec app sh

# Dans le conteneur :
ls /app/data/
# Vous voyez la base de données SQLite

exit
```

---

## Étape 9 — Arrêter proprement

```bash
# Arrêter sans supprimer les données
docker-compose down

# Pour tout supprimer y compris les données :
docker-compose down -v
```

---

## 📝 Évolution du portail

| Version | Module | Nouveautés |
|---------|--------|-----------|
| v1.0 | 02 | Dockerfile simple |
| v2.0 | 03 | Multi-stage, non-root |
| v3.0 | 04 | BuildKit optimisé |
| **v4.0** | **05** | **Nginx + Flask + SQLite, Docker Compose** |

---

➡️ **Retour :** [Lab basique](../lab-basique/README.md) | **Suivant :** [Module 06](../../module-06/lab-basique/README.md)
