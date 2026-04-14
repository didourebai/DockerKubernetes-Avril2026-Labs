# Module 08 — Lab fil rouge : IT-Support Portal v7 — Déploiement Helm

> **Niveau :** Débutant | **Durée estimée :** 35 minutes

## 🎯 Objectif

Déployer et gérer le IT-Support Portal entièrement avec Helm :
- Installation en une commande
- Mise à jour de version
- Rollback en cas de problème


> **IMPORTANT avant de commencer :**
> L'image `it-portal:v7` doit etre construite localement AVANT de deployer avec Helm.
> Si vous sautez cette etape, les Pods restent en `ErrImageNeverPull`.

---

## Etape 0 -- Construire l'image (OBLIGATOIRE)

**Windows (PowerShell) :**
```powershell
cd labs\module-08\lab-fil-rouge
docker build -t it-portal:v7 -f app\Dockerfile app\
docker images | findstr it-portal
```

**Mac / Linux :**
```bash
cd labs/module-08/lab-fil-rouge
docker build -t it-portal:v7 -f app/Dockerfile app/
docker images | grep it-portal
```

**Resultat attendu :**
```
it-portal   v7   abc123...   1 minute ago   ~150MB
```

---

## Architecture v7

```
Helm Chart: it-support-portal
│
├── Deployment: app (Flask)    ← configurable via values.yaml
├── Deployment: nginx          ← configurable via values.yaml
├── Service: nginx (NodePort)
├── Service: app (ClusterIP)
├── ConfigMap: app-config
├── Secret: app-secret
└── PersistentVolumeClaim
```

---

## Étape 1 — Construire l'image

```bash
cd labs/module-08/lab-fil-rouge
docker build -t it-portal:v7 -f app/Dockerfile app/
```

---

## Étape 2 — Explorer le chart Helm

```bash
ls chart/
```

```
chart/
├── Chart.yaml            ← Nom, version, description
├── values.yaml           ← Valeurs par défaut
└── templates/
    ├── namespace.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── pvc.yaml
    ├── deployment-app.yaml
    ├── deployment-nginx.yaml
    ├── service-app.yaml
    └── service-nginx.yaml
```

Ouvrez `chart/values.yaml` et lisez les paramètres configurables.

---

## Étape 3 — Valider le chart

```bash
helm lint chart/
```

---

## Étape 4 — Voir le YAML qui sera généré

```bash
helm template portail chart/ | head -80
```

> 💡 Helm remplace les `{{ .Values.xxx }}` par les valeurs de `values.yaml`. Vous voyez le YAML final sans rien déployer.

---

## Étape 5 — Installer le portail

```bash
helm install portail-it chart/ \
  --namespace it-support \
  --create-namespace \
  --set app.version=7.0.0 \
  --set nginx.nodePort=30080
```

Vérifier :
```bash
helm list -n it-support
kubectl -n it-support get pods
```

Ouvrez **http://localhost:30080** ✅

---

## Étape 6 — Mettre à jour la version

```bash
helm upgrade portail-it chart/ \
  --namespace it-support \
  --set app.version=7.1.0 \
  --set app.replicas=4
```

```bash
# Vérifier la mise à jour
helm history portail-it -n it-support
kubectl -n it-support get pods
```

Le portail reste accessible pendant la mise à jour.

---

## Étape 7 — Simuler un problème et faire un rollback

```bash
# Déployer une "mauvaise" version
helm upgrade portail-it chart/ \
  --namespace it-support \
  --set app.image=it-portal:inexistante

# Les pods échouent à démarrer
kubectl -n it-support get pods

# Rollback immédiat vers la version précédente
helm rollback portail-it -n it-support

# Tout est revenu à la normale
kubectl -n it-support get pods
```

---

## Étape 8 — Personnaliser avec un fichier de valeurs

Créez `mes-valeurs.yaml` :

```yaml
app:
  version: "7.2.0"
  replicas: 2
  env: "production"

nginx:
  replicas: 2
  nodePort: 30080
```

```bash
helm upgrade portail-it chart/ \
  -n it-support \
  -f mes-valeurs.yaml
```

---

## Étape 9 — Désinstaller proprement

```bash
helm uninstall portail-it -n it-support
kubectl delete namespace it-support
```

---

## 🎉 Félicitations — Vous avez complété la formation !

Voici le parcours complet du IT-Support Portal :

| Version | Module | Technologie |
|---------|--------|-------------|
| v1.0 | 01 | Découverte |
| v2.0 | 02 | Dockerfile |
| v3.0 | 03 | Multi-stage, sécurité |
| v4.0 | 04 | BuildKit optimisé |
| v5.0 | 05 | Docker Compose + Nginx + SQLite |
| v6.0 | 06 | Docker Swarm (haute disponibilité) |
| v6.0 | 07 | Kubernetes |
| **v7.0** | **08** | **Helm — déploiement géré** |

Vous savez maintenant conteneuriser, orchestrer et gérer une application web complète !

---

➡️ **Retour au [README principal](../../README.md)**
