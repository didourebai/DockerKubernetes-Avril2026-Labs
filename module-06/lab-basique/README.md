# Module 06 — Lab basique : Docker Swarm

> **Niveau :** Débutant | **Durée estimée :** 25 minutes  
> **Note :** Docker Swarm fonctionne sur Docker Desktop — un seul nœud suffit pour ce lab.

## 🎯 Objectifs
Comprendre Docker Swarm : initialiser un cluster, déployer un service, le scaler.


> **Note Windows PowerShell :**
> - `| grep X`  ->  `| findstr X`
> - `$(date +%Y-%m-%d)`  ->  `$(Get-Date -Format "yyyy-MM-dd")`
> - `$(pwd)`  ->  `${PWD}`
> - `commande1 && commande2`  ->  deux lignes separees

---

## Étape 1 — Initialiser un cluster Swarm

```bash
docker swarm init
```

**Résultat attendu :** Un message "Swarm initialized" avec une commande `docker swarm join`.

```bash
# Voir l'état du cluster
docker node ls
```

Vous êtes le seul nœud — rôle **Leader** et **Manager**.

---

## Étape 2 — Déployer un premier service

Dans Swarm, on ne fait plus `docker run`, on crée des **services** :

```bash
docker service create \
  --name mon-web \
  --replicas 2 \
  --publish 8080:80 \
  nginx:alpine
```

**Explication :**
- `--replicas 2` : 2 copies du conteneur
- `--publish 8080:80` : port accessible depuis l'extérieur

```bash
# Voir le service
docker service ls

# Voir les conteneurs (tâches) du service
docker service ps mon-web
```

Ouvrez **http://localhost:8080** ✅

---

## Étape 3 — Scaler le service

```bash
# Passer à 4 répliques
docker service scale mon-web=4

# Vérifier
docker service ps mon-web
```

Swarm démarre automatiquement 2 conteneurs supplémentaires.

---

## Étape 4 — Simuler une panne

```bash
# Trouver l'ID d'un conteneur du service
docker ps | findstr mon-web

# Supprimer un conteneur (simuler une panne)
docker rm -f <ID_DU_CONTENEUR>

# Observer : Swarm le redémarre automatiquement !
docker service ps mon-web
```

> 💡 C'est l'**auto-réparation** (self-healing) de Swarm. Il maintient toujours le nombre de répliques demandé.

---

## Étape 5 — Mettre à jour le service

```bash
# Mettre à jour l'image (rolling update)
docker service update \
  --image nginx:1.27-alpine \
  --update-parallelism 1 \
  --update-delay 5s \
  mon-web
```

Pendant la mise à jour, le service reste disponible — les conteneurs sont mis à jour un par un.

---

## Étape 6 — Supprimer le service et quitter Swarm

```bash
docker service rm mon-web
docker swarm leave --force
```

---

## ✅ Récapitulatif

| Commande | Action |
|----------|--------|
| `docker swarm init` | Créer un cluster |
| `docker service create` | Déployer un service |
| `docker service ls` | Lister les services |
| `docker service ps <nom>` | Voir les tâches |
| `docker service scale <nom>=N` | Changer le nombre de répliques |
| `docker service update` | Mettre à jour |
| `docker service rm` | Supprimer un service |
| `docker swarm leave --force` | Quitter le cluster |

---

➡️ **Suivant :** [Lab fil rouge — Portail en haute disponibilité Swarm](../lab-fil-rouge/README.md)
