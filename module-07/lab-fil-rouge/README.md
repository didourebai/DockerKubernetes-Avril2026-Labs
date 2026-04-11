# Module 07 — Lab fil rouge : IT-Support Portal v6 — Déploiement Kubernetes

> **Niveau :** Débutant | **Durée estimée :** 40 minutes

## 🎯 Objectif

Migrer le IT-Support Portal de Docker Compose vers Kubernetes.  
Utiliser des Deployments, Services, ConfigMaps et Secrets K8s.

---

## Architecture v6

```
Navigateur
    │
    ▼
Service K8s (NodePort 30080)
    │
    ▼
Deployment: nginx  (2 Pods)   ← Proxy inverse
    │
    ▼
Service K8s (ClusterIP)
    │
    ▼
Deployment: app    (3 Pods)   ← Flask Python
    │
    ▼
PersistentVolumeClaim         ← Données SQLite persistantes
```

---

## Étape 1 — Préparer l'image

```bash
cd labs/module-07/lab-fil-rouge

# Construire l'image v6
docker build -t it-portal:v6 -f app/Dockerfile app/
```

---

## Étape 2 — Créer le namespace

Kubernetes utilise des **namespaces** pour isoler les ressources :

```bash
kubectl apply -f k8s/namespace.yaml
kubectl get namespaces
```

---

## Étape 3 — Déployer la configuration (ConfigMap + Secret)

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

kubectl -n it-support get configmaps
kubectl -n it-support get secrets
```

---

## Étape 4 — Déployer le stockage persistant

```bash
kubectl apply -f k8s/pvc.yaml
kubectl -n it-support get pvc
```

---

## Étape 5 — Déployer l'application Flask

```bash
kubectl apply -f k8s/deployment-app.yaml
kubectl -n it-support get pods
kubectl -n it-support rollout status deployment/it-portal-app
```

---

## Étape 6 — Déployer Nginx

```bash
kubectl apply -f k8s/configmap-nginx.yaml
kubectl apply -f k8s/deployment-nginx.yaml
kubectl apply -f k8s/service-nginx.yaml
```

---

## Étape 7 — Accéder au portail

```bash
kubectl -n it-support get services
```

Ouvrez **http://localhost:30080** ✅

---

## Étape 8 — Tester la résilience

```bash
# Voir les pods
kubectl -n it-support get pods

# Supprimer un pod app
kubectl -n it-support delete pod <NOM_DU_POD_APP>

# K8s le recrée immédiatement
kubectl -n it-support get pods
```

---

## Étape 9 — Voir les logs

```bash
# Logs de l'application
kubectl -n it-support logs -l app=it-portal-app --tail=20

# Suivre en temps réel
kubectl -n it-support logs -l app=it-portal-app -f
```

---

## Étape 10 — Mettre à jour la version

```bash
# Changer la version dans le ConfigMap
kubectl -n it-support edit configmap it-portal-config

# Ou forcer un redémarrage des pods
kubectl -n it-support rollout restart deployment/it-portal-app
```

---

## Étape 11 — Nettoyage

```bash
kubectl delete namespace it-support
```

---

## 📝 Évolution du portail

| Version | Module | Orchestrateur |
|---------|--------|--------------|
| v4.0 | 05 | Docker Compose |
| v5.0 | 06 | Docker Swarm |
| **v6.0** | **07** | **Kubernetes** |

---

➡️ **Retour :** [Lab basique](../lab-basique/README.md) | **Suivant :** [Module 08 — Helm](../../module-08/lab-basique/README.md)
