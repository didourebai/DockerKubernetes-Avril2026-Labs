# Module 07 — Lab basique : Kubernetes avec kind

> **Niveau :** Débutant | **Durée estimée :** 40 minutes  
> **Prérequis :** Docker Desktop avec Kubernetes activé, ou kind installé

## 🎯 Objectifs
Créer un cluster local, déployer un Pod, un Deployment et un Service.

---

## Étape 1 — Vérifier kubectl et le cluster

```bash
kubectl version --client
kubectl get nodes
kubectl cluster-info
```

Si vous utilisez Docker Desktop : activez Kubernetes dans **Settings → Kubernetes → Enable Kubernetes**.

---

## Étape 2 — Votre premier Pod

Créez le fichier `pod-nginx.yaml` :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mon-premier-pod
  labels:
    app: web
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
```

```bash
# Créer le Pod
kubectl apply -f pod-nginx.yaml

# Voir le Pod
kubectl get pods

# Voir les détails
kubectl describe pod mon-premier-pod

# Accéder au Pod depuis votre machine
kubectl port-forward pod/mon-premier-pod 8080:80
# Ouvrir http://localhost:8080 (Ctrl+C pour arrêter)
```

---

## Étape 3 — Un Deployment (gère plusieurs Pods)

Créez `deployment-nginx.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3          # 3 copies du Pod
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "32Mi"
            cpu: "50m"
          limits:
            memory: "64Mi"
            cpu: "100m"
```

```bash
kubectl apply -f deployment-nginx.yaml
kubectl get deployments
kubectl get pods
```

---

## Étape 4 — Un Service (expose le Deployment)

Créez `service-nginx.yaml` :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

```bash
kubectl apply -f service-nginx.yaml
kubectl get services
```

Ouvrez **http://localhost:30080** ✅

---

## Étape 5 — Scaler le Deployment

```bash
# Passer à 5 répliques
kubectl scale deployment web-deployment --replicas=5
kubectl get pods

# Revenir à 2
kubectl scale deployment web-deployment --replicas=2
```

---

## Étape 6 — Simuler une panne

```bash
# Lister les pods
kubectl get pods

# Supprimer un pod
kubectl delete pod <NOM_DU_POD>

# Kubernetes en recrée un immédiatement !
kubectl get pods
```

---

## Étape 7 — Mettre à jour l'image (Rolling Update)

```bash
kubectl set image deployment/web-deployment nginx=nginx:1.27-alpine

# Suivre le déploiement
kubectl rollout status deployment/web-deployment

# Voir l'historique
kubectl rollout history deployment/web-deployment

# Annuler si problème
kubectl rollout undo deployment/web-deployment
```

---

## Étape 8 — ConfigMap et Secret

```bash
# Créer un ConfigMap
kubectl create configmap app-config \
  --from-literal=APP_ENV=production \
  --from-literal=APP_VERSION=1.0.0

kubectl get configmap app-config
kubectl describe configmap app-config

# Créer un Secret
kubectl create secret generic app-secret \
  --from-literal=DB_PASSWORD=MonMotDePasse123

kubectl get secrets
```

---

## Étape 9 — Nettoyage

```bash
kubectl delete -f deployment-nginx.yaml
kubectl delete -f service-nginx.yaml
kubectl delete -f pod-nginx.yaml
kubectl delete configmap app-config
kubectl delete secret app-secret
```

---

## ✅ Récapitulatif commandes kubectl

| Commande | Action |
|----------|--------|
| `kubectl apply -f fichier.yaml` | Créer/mettre à jour une ressource |
| `kubectl get pods/deployments/services` | Lister les ressources |
| `kubectl describe <ressource> <nom>` | Détails d'une ressource |
| `kubectl delete -f fichier.yaml` | Supprimer |
| `kubectl scale deployment` | Changer le nombre de Pods |
| `kubectl rollout status/undo` | Suivre/annuler un déploiement |
| `kubectl port-forward` | Accès temporaire depuis votre machine |
| `kubectl logs <pod>` | Voir les logs |
| `kubectl exec -it <pod> -- sh` | Entrer dans un Pod |

---

➡️ **Suivant :** [Lab fil rouge — Portail sur Kubernetes](../lab-fil-rouge/README.md)
