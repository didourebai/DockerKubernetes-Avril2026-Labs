# Module 07 — Lab fil rouge : IT-Support Portal v6 — Déploiement Kubernetes

> **Niveau :** Débutant | **Durée estimée :** 40 minutes

## 🎯 Objectif

Migrer le IT-Support Portal de Docker Compose vers Kubernetes.  
Utiliser des Deployments, Services, ConfigMaps et Secrets K8s.


> **IMPORTANT avant de commencer :**
> L'image `it-portal:v6` doit etre construite localement AVANT de deployer sur Kubernetes.
> Kubernetes cherche cette image sur votre machine (`imagePullPolicy: Never`).
> Si vous sautez cette etape, vous obtenez l'erreur `ErrImageNeverPull`.

---

## Etape 0 -- Construire l'image (OBLIGATOIRE)

**Windows (PowerShell) :**
```powershell
cd labs\module-07\lab-fil-rouge
docker build -t it-portal:v6 -f app\Dockerfile app\
docker images | findstr it-portal
```

**Mac / Linux :**
```bash
cd labs/module-07/lab-fil-rouge
docker build -t it-portal:v6 -f app/Dockerfile app/
docker images | grep it-portal
```

**Resultat attendu :**
```
it-portal   v6   abc123...   1 minute ago   ~150MB
```

> Sans ce resultat, n'allez pas plus loin -- les Pods ne demarreront pas.

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

## Étape 1 — Construire l'image (OBLIGATOIRE avant tout kubectl)

> **Important :** Kubernetes ne peut pas télécharger cette image depuis Internet.
> Elle doit exister localement dans Docker Desktop avant de déployer.
> Si vous sautez cette étape, les Pods resteront bloqués en `ErrImagePull`.

**Windows (PowerShell) :**
```powershell
cd labs\module-07\lab-fil-rouge
docker build -t it-portal:v6 -f app/Dockerfile app/
```

**Mac / Linux :**
```bash
cd labs/module-07/lab-fil-rouge
docker build -t it-portal:v6 -f app/Dockerfile app/
```

**Verifier que l'image existe avant de continuer :**

**Windows (PowerShell) :**
```powershell
docker images | findstr it-portal
```

**Mac / Linux :**
```bash
docker images | grep it-portal
```

**Resultat attendu :**
```
it-portal   v6   abc123...   2 minutes ago   180MB
```

> Si l'image n'apparait pas, le build a echoue. Relancez la commande docker build.

---

**Diagnostic si les Pods ne demarrent pas :**

Si apres avoir deploye vous voyez cette erreur :
```
error: deployment "it-portal-app" exceeded its progress deadline
```

Cela signifie que l'image n'a pas ete trouvee. Verifiez avec :
```bash
kubectl -n it-support describe pod -l app=it-portal-app
```

Puis rebuildez l'image et relancez :
```bash
docker build -t it-portal:v6 -f app/Dockerfile app/
kubectl -n it-support rollout restart deployment/it-portal-app
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

**Acceder au portail :**

```bash
kubectl port-forward service/it-portal-nginx-svc 8080:80 -n it-support
```

Ouvrez **http://localhost:8080** dans votre navigateur.
`Ctrl+C` pour arreter le port-forward.

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
