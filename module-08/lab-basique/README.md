# Module 08 — Lab basique : Helm

> **Niveau :** Débutant | **Durée estimée :** 30 minutes

## 🎯 Objectifs
Comprendre Helm, installer un chart existant, créer votre propre chart.

---

## Étape 1 — Installer et vérifier Helm

```bash
helm version
```

Si Helm n'est pas installé : https://helm.sh/docs/intro/install/

---

## Étape 2 — Ajouter un dépôt de charts

```bash
# Ajouter le dépôt officiel
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami

# Mettre à jour les dépôts
helm repo update

# Lister les dépôts
helm repo list
```

---

## Étape 3 — Chercher et inspecter un chart

```bash
# Chercher un chart Nginx
helm search repo nginx

# Voir les informations du chart Nginx Bitnami
helm show chart bitnami/nginx

# Voir les valeurs configurables
helm show values bitnami/nginx | head -50
```

---

## Étape 4 — Installer un chart

```bash
# Installer Nginx avec le nom "mon-nginx"
helm install mon-nginx bitnami/nginx \
  --set service.type=NodePort \
  --set service.nodePorts.http=30090

# Voir les releases installées
helm list

# Voir l'état de la release
helm status mon-nginx
```

Ouvrez **http://localhost:30090** ✅

---

## Étape 5 — Mettre à jour une release

```bash
# Mettre à jour la configuration
helm upgrade mon-nginx bitnami/nginx \
  --set service.type=NodePort \
  --set service.nodePorts.http=30090 \
  --set replicaCount=2

# Voir l'historique
helm history mon-nginx
```

---

## Étape 6 — Rollback

```bash
# Revenir à la version 1
helm rollback mon-nginx 1

# Vérifier
helm history mon-nginx
```

---

## Étape 7 — Désinstaller

```bash
helm uninstall mon-nginx
helm list   # Vide
```

---

## Étape 8 — Créer votre propre chart

```bash
helm create mon-chart
ls mon-chart/
```

La structure créée :
```
mon-chart/
├── Chart.yaml          ← Métadonnées
├── values.yaml         ← Valeurs par défaut (configurables)
├── templates/          ← Manifestes Kubernetes avec variables
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
└── charts/             ← Dépendances
```

```bash
# Valider le chart
helm lint mon-chart

# Voir le YAML généré (sans déployer)
helm template mon-chart

# Installer
helm install test-chart mon-chart

helm list
helm uninstall test-chart
rm -rf mon-chart
```

---

## ✅ Récapitulatif

| Commande | Action |
|----------|--------|
| `helm install <nom> <chart>` | Installer |
| `helm upgrade <nom> <chart>` | Mettre à jour |
| `helm rollback <nom> <version>` | Revenir en arrière |
| `helm uninstall <nom>` | Désinstaller |
| `helm list` | Lister les releases |
| `helm history <nom>` | Historique |
| `helm create <nom>` | Créer un chart vide |
| `helm lint <chart>` | Valider |
| `helm template <chart>` | Voir le YAML généré |

---

➡️ **Suivant :** [Lab fil rouge — Portail déployé avec Helm](../lab-fil-rouge/README.md)
