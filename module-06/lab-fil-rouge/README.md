# Module 06 — Lab fil rouge : IT-Support Portal v5 — Déploiement Swarm

> **Niveau :** Débutant | **Durée estimée :** 30 minutes

## 🎯 Objectif

Déployer le IT-Support Portal en **haute disponibilité** avec Docker Swarm.  
Le portail restera accessible même si un conteneur tombe.


> **Note Windows PowerShell :**
> - `| grep X`  ->  `| findstr X`
> - `$(date +%Y-%m-%d)`  ->  `$(Get-Date -Format "yyyy-MM-dd")`
> - `$(pwd)`  ->  `${PWD}`
> - `commande1 && commande2`  ->  deux lignes separees

---

## Architecture v5

```
Internet
    │
    ▼
Docker Swarm (1 nœud en lab, N nœuds en prod)
    │
    ├── nginx        (2 répliques) ← Load balancing automatique
    └── app Flask    (3 répliques) ← Haute disponibilité
              │
              └── Volume partagé (portail-data)
```

---

## Étape 1 — Initialiser Swarm

```bash
docker swarm init
```

---

## Étape 2 — Construire et tagger l'image

Swarm a besoin que l'image soit disponible — on la construit localement :

```bash
cd labs/module-06/lab-fil-rouge

docker build \
  -t it-portal:v5 \
  -f app/Dockerfile app/
```

---

## Étape 3 — Déployer la stack

Avec Swarm, on déploie une **stack** (ensemble de services) depuis un fichier `docker-stack.yml` :

```bash
docker stack deploy -c docker-stack.yml portail-it
```

---

## Étape 4 — Vérifier le déploiement

```bash
# Voir toutes les stacks
docker stack ls

# Voir les services de notre stack
docker stack services portail-it

# Voir les tâches (conteneurs) de chaque service
docker stack ps portail-it
```

Ouvrez **http://localhost:8080** ✅

---

## Étape 5 — Tester la haute disponibilité

```bash
# Trouver un conteneur de l'application
docker ps | findstr portail-it_app

# Supprimer un conteneur (simuler une panne)
docker rm -f <ID>

# Swarm le redémarre automatiquement
docker stack ps portail-it
```

Le portail reste accessible pendant toute la durée ! Swarm recrée le conteneur manquant.

---

## Étape 6 — Mettre à jour sans interruption

```bash
# Simuler une nouvelle version en changeant une variable
docker service update \
  --env-add APP_VERSION=5.1.0 \
  portail-it_app
```

Swarm met à jour les conteneurs un par un — le service ne s'interrompt pas.

---

## Étape 7 — Supprimer la stack et quitter Swarm

```bash
docker stack rm portail-it
docker swarm leave --force
```

---

## 📝 Évolution du portail

| Version | Module | Nouveautés |
|---------|--------|-----------|
| v4.0 | 05 | Docker Compose, Nginx, SQLite |
| **v5.0** | **06** | **Swarm, haute disponibilité, load balancing** |

---

➡️ **Suivant :** [Module 07 — Kubernetes](../../module-07/lab-basique/README.md)
