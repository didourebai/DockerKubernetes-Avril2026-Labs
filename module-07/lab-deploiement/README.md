# Lab Déploiement -- Rolling Update, Scaling et Rollback

> **Niveau :** Débutant
> **Durée estimée :** 30 minutes
> **Prérequis :** Lab basique module-07 terminé

---

## Objectifs

- Déployer une application avec plusieurs répliques
- Mettre à jour sans interruption de service (Rolling Update)
- Annuler une mise à jour problématique (Rollback)
- Scaler horizontalement (ajouter/retirer des Pods)

---

## Étape 1 -- Déployer l'application version 1

Examinez `deployment-v1.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portail-it
  labels:
    app: portail-it
spec:
  replicas: 3                    # 3 copies du Pod
  selector:
    matchLabels:
      app: portail-it
  template:
    metadata:
      labels:
        app: portail-it
    spec:
      containers:
      - name: app
        image: nginx:1.24-alpine  # Version 1
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "16Mi"
            cpu: "25m"
          limits:
            memory: "32Mi"
            cpu: "50m"
```

```bash
kubectl apply -f deployment-v1.yaml
kubectl get pods
kubectl get deployment portail-it
```

**Résultat attendu :**
```
NAME                          READY   STATUS    RESTARTS
portail-it-xxx-aaa            1/1     Running   0
portail-it-xxx-bbb            1/1     Running   0
portail-it-xxx-ccc            1/1     Running   0
```

---

## Étape 2 -- Exposer le déploiement avec un Service

```bash
kubectl apply -f service-portail.yaml
kubectl get service portail-it-svc
```

**Acceder au portail :**

```bash
kubectl port-forward service/portail-it-svc 8080:80
```

Ouvrez **http://localhost:8080** dans votre navigateur.
`Ctrl+C` pour arreter le port-forward.

---

## Étape 3 -- Scaler (changer le nombre de répliques)

### Ajouter des répliques

```bash
# Passer de 3 à 5 répliques
kubectl scale deployment portail-it --replicas=5
kubectl get pods
```

Kubernetes crée 2 nouveaux Pods automatiquement.

### Réduire les répliques

```bash
# Revenir à 2 répliques
kubectl scale deployment portail-it --replicas=2
kubectl get pods
```

Kubernetes supprime 3 Pods proprement (graceful shutdown).

### Observer en temps réel

```bash
# Dans un deuxième terminal, surveiller les Pods
kubectl get pods -w
# Ctrl+C pour arrêter
```

---

## Étape 4 -- Rolling Update (mise à jour sans interruption)

Un Rolling Update remplace les Pods un par un, en gardant
le service disponible pendant toute la durée de la mise à jour.

### Remettre à 3 répliques avant la mise à jour

```bash
kubectl scale deployment portail-it --replicas=3
```

### Lancer la mise à jour

```bash
# Mettre à jour l'image (simuler passage version 1 -> version 2)
kubectl set image deployment/portail-it app=nginx:1.27-alpine
```

### Observer le Rolling Update en temps réel

```bash
kubectl rollout status deployment/portail-it
```

**Résultat attendu :**
```
Waiting for deployment "portail-it" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "portail-it" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "portail-it" rollout to finish: 1 old replicas are pending termination...
deployment "portail-it" successfully rolled out
```

Kubernetes remplace les Pods un par un -- à aucun moment le
service n'est complètement arrêté.

### Vérifier la nouvelle version

```bash
kubectl describe pod -l app=portail-it | grep Image
# Image: nginx:1.27-alpine
```

---

## Étape 5 -- Voir l'historique des déploiements

```bash
kubectl rollout history deployment/portail-it
```

**Résultat attendu :**
```
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
```

Pour avoir une description de chaque révision :
```bash
kubectl rollout history deployment/portail-it --revision=1
kubectl rollout history deployment/portail-it --revision=2
```

---

## Étape 6 -- Simuler un problème et faire un Rollback

### Déployer une "mauvaise" version

```bash
# Déployer une image qui n'existe pas (simuler une erreur)
kubectl set image deployment/portail-it app=nginx:version-inexistante
```

### Observer le problème

```bash
kubectl get pods
# Les nouveaux Pods sont en ErrImagePull ou ImagePullBackOff
kubectl rollout status deployment/portail-it
# Bloqué...  Ctrl+C pour interrompre
```

```bash
kubectl describe pod -l app=portail-it | grep -A5 "Events:"
```

**Windows (PowerShell) :**
```powershell
kubectl describe pod -l app=portail-it | findstr /A5 "Events:"
```

### Rollback immédiat vers la version précédente

```bash
kubectl rollout undo deployment/portail-it
```

### Vérifier que le service est rétabli

```bash
kubectl rollout status deployment/portail-it
kubectl get pods
# Tous les Pods sont Running avec l'ancienne image
```

### Rollback vers une révision spécifique

```bash
# Voir l'historique
kubectl rollout history deployment/portail-it

# Revenir à la révision 1 (toute première version)
kubectl rollout undo deployment/portail-it --to-revision=1
```

---

## Étape 7 -- Ajouter des annotations pour tracer les changements

```bash
# Mise à jour avec annotation (bonne pratique en production)
kubectl set image deployment/portail-it app=nginx:1.27-alpine
kubectl annotate deployment/portail-it \
  kubernetes.io/change-cause="Mise à jour nginx 1.24 -> 1.27"

kubectl rollout history deployment/portail-it
# REVISION  CHANGE-CAUSE
# 1         <none>
# ...
# 5         Mise à jour nginx 1.24 -> 1.27
```

---

## Étape 8 -- Pause et reprise d'un déploiement

Utile pour faire plusieurs changements avant de les appliquer.

```bash
# Mettre le déploiement en pause
kubectl rollout pause deployment/portail-it

# Faire plusieurs changements
kubectl set image deployment/portail-it app=nginx:1.27-alpine
kubectl set resources deployment/portail-it \
  --limits=memory=64Mi,cpu=100m

# Reprendre -- les changements s'appliquent tous d'un coup
kubectl rollout resume deployment/portail-it
kubectl rollout status deployment/portail-it
```

---

## Nettoyage

```bash
kubectl delete deployment portail-it
kubectl delete service portail-it-svc
```

---

## Récapitulatif

| Commande | Action |
|----------|--------|
| `kubectl scale deployment X --replicas=N` | Changer le nombre de Pods |
| `kubectl set image deployment/X cont=image:tag` | Mettre à jour l'image |
| `kubectl rollout status deployment/X` | Suivre la progression |
| `kubectl rollout history deployment/X` | Voir l'historique |
| `kubectl rollout undo deployment/X` | Rollback version précédente |
| `kubectl rollout undo deployment/X --to-revision=N` | Rollback vers révision N |
| `kubectl rollout pause/resume deployment/X` | Pause / reprise |

---

Suite : [Lab fil rouge -- IT-Support Portal sur Kubernetes](../lab-fil-rouge/README.md)
