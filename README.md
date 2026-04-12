# DockerKubernetes-Avril2026-Labs

> Ce guide vous accompagne pas à pas dans la découverte de Docker et Kubernetes, en partant des bases jusqu'à des déploiements complets.  


---

## À propos de ces laboratoires

Chaque module contient **deux laboratoires** :

| Type | Description |
|------|-------------|
| 🔧 **Lab basique** | Exercices indépendants pour maîtriser les commandes du module |
| 🏗️ **Lab fil rouge** | Construction progressive du **IT-Support Portal** — un portail web interne d'institution |

### Le cas d'utilisation fil rouge : IT-Support Portal

Un portail web interne qui permet aux professeurs de consulter l'état de l'infrastructure IT (serveurs, VMs, services).  
Il est composé d'un **site web HTML** servi par **Nginx** et d'une **API Python (Flask)** qui retourne des informations système.

À chaque module, le portail évolue et gagne en robustesse, jusqu'à être déployé sur Kubernetes avec Helm.

---

## Structure du dépôt

```
labs/
├── app/                        ← Code source du IT-Support Portal (référence)
├── module-01/                  ← Concepts des conteneurs
├── module-02/                  ← Docker : architecture et composants
├── module-03/                  ← Construire votre première image Docker
├── module-04/                  ← Optimisation des builds Docker
├── module-05/                  ← Réseau et Docker Compose
├── module-06/                  ← Docker Swarm
├── module-07/                  ← Kubernetes
└── module-08/                  ← Helm
```

Chaque module contient :
```
module-XX/
├── lab-basique/README.md       ← Exercices de base sur les commandes
└── lab-fil-rouge/              ← Fichiers du portail (code + configs)
    └── README.md               ← Instructions étape par étape
```

---

## Prérequis

- **Docker Desktop** installé (Windows ou Mac) — [Télécharger ici](https://www.docker.com/products/docker-desktop/)
- Un terminal (PowerShell sur Windows, Terminal sur Mac)
- Aucune connaissance en développement requise

---

## Progression du IT-Support Portal

| Version | Module | Technologie introduite |
|---------|--------|----------------------|
| v1.0 | 01 | Découverte (conteneur existant) |
| v2.0 | 02 | Premier Dockerfile Python/Flask |
| v3.0 | 03 | Multi-stage build, utilisateur non-root |
| v4.0 | 04 | BuildKit, cache optimisé |
| v5.0 | 05 | Nginx + SQLite + Docker Compose |
| v6.0 | 06 | Docker Swarm, haute disponibilité |
| v6.0 | 07 | Kubernetes (Deployments, Services, PVC) |
| v7.0 | 08 | Helm — déploiement géré et rollback |

---

## Comment utiliser ces labs

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/didourebai/DockerKubernetes-Avril2026-Labs.git
   cd DockerKubernetes-Avril2026-Labs
   ```
2. Naviguez dans le module correspondant au cours du jour
3. Lisez le `README.md` du lab et suivez les étapes

---

*Formation Avril 2026 — Fondements des conteneurs Docker et Kubernetes*
