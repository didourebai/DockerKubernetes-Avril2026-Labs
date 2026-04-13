# Module 05 — Lab basique : Réseau Docker et Docker Compose

> **Niveau :** Débutant  
> **Durée estimée :** 35 minutes


> **Note Windows PowerShell :**
> - `cat > fichier << 'EOF' ... EOF`  ->  `@" ... "@ | Out-File fichier -Encoding utf8`
> - `rm -rf dossier`  ->  `Remove-Item -Recurse -Force dossier`
> - `| grep X`  ->  `| findstr X`
> - `commande1 && commande2`  ->  deux lignes separees

---

## 🎯 Objectifs

- Créer un réseau Docker pour faire communiquer des conteneurs
- Écrire un fichier `docker-compose.yml`
- Lancer plusieurs services avec une seule commande
- Gérer les variables d'environnement avec un fichier `.env`

---

## Partie A — Réseau Docker

### Étape 1 — Créer un réseau bridge

```bash
# Créer un réseau isolé
docker network create --driver bridge reseau-institution

# Lister les réseaux
docker network ls
```

### Étape 2 — Lancer deux conteneurs sur le même réseau

```bash
# Lancer un serveur web
docker run -d --network reseau-institution --name serveur-web nginx:alpine

# Lancer un conteneur "client"
docker run -d --network reseau-institution --name client-test nginx:alpine sleep 3600
```

### Étape 3 — Tester la communication entre conteneurs

```bash
# Depuis le client, pinguer le serveur web par son NOM
docker exec client-test ping -c 3 serveur-web

# Faire une requête HTTP au serveur web
docker exec client-test wget -qO- http://serveur-web
```

> 💡 Les conteneurs sur le même réseau peuvent se joindre **par leur nom** — pas besoin d'adresse IP !

### Étape 4 — Nettoyer

```bash
docker stop serveur-web client-test
docker rm serveur-web client-test
docker network rm reseau-institution
```

---

## Partie B — Docker Compose

### Étape 5 — Votre premier docker-compose.yml

Créez un dossier et le fichier suivant :

```bash
mkdir compose-test
cd compose-test
```

Créez `docker-compose.yml` :

```yaml
# docker-compose.yml — Exemple simple : Nginx + outil de monitoring
version: "3.9"

services:

  # Service 1 : Serveur web
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    networks:
      - reseau-app

  # Service 2 : Vérification de santé (whoami retourne l'identité du conteneur)
  whoami:
    image: containous/whoami
    networks:
      - reseau-app

networks:
  reseau-app:
    driver: bridge
```

Créez la page HTML :

```bash
mkdir html
echo "<h1>🖥️ Serveur Web — Formation Docker</h1>" > html/index.html
```

### Étape 6 — Lancer tous les services

```bash
# Démarrer tous les services en arrière-plan
docker-compose up -d

# Voir les services actifs
docker-compose ps

# Voir les logs de tous les services
docker-compose logs

# Voir les logs d'un service spécifique en temps réel
docker-compose logs -f web
```

Testez dans votre navigateur :
- **http://localhost:8080** → Votre page Nginx

### Étape 7 — Variables d'environnement avec .env

Créez un fichier `.env` :

```bash
**Mac / Linux :**
```bash
cat > .env << 'EOF'
APP_NAME=Formation-Docker
APP_VERSION=1.0.0
NGINX_PORT=8080
EOF
```

**Windows (PowerShell) :**
```powershell
@"
APP_NAME=Formation-Docker
APP_VERSION=1.0.0
NGINX_PORT=8080
"@ | Out-File -FilePath .env -Encoding utf8
```
```

Modifiez `docker-compose.yml` pour utiliser ces variables :

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "${NGINX_PORT}:80"
    environment:
      - APP_NAME=${APP_NAME}
      - APP_VERSION=${APP_VERSION}
```

Relancez :
```bash
docker-compose down
docker-compose up -d
```

### Étape 8 — Commandes utiles Compose

```bash
# Arrêter sans supprimer
docker-compose stop

# Redémarrer
docker-compose start

# Arrêter ET supprimer les conteneurs et réseaux
docker-compose down

# Arrêter ET supprimer + les volumes
docker-compose down -v

# Reconstruire les images
docker-compose build

# Voir l'utilisation des ressources
docker-compose top
```

### Étape 9 — Nettoyer

```bash
docker-compose down
cd ..
Remove-Item -Recurse -Force compose-test
```

---

## ✅ Récapitulatif

| Commande | Action |
|----------|--------|
| `docker-compose up -d` | Démarrer tous les services |
| `docker-compose down` | Arrêter et supprimer |
| `docker-compose ps` | État des services |
| `docker-compose logs -f` | Logs en temps réel |
| `docker-compose build` | Reconstruire les images |
| `docker-compose stop/start` | Pause/reprise |
| `docker-compose exec <service> sh` | Entrer dans un service |

---

➡️ **Suivant :** [Lab fil rouge — Portail avec base de données](../lab-fil-rouge/README.md)
