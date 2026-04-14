# Lab ConfigMap et Secret -- Gérer la configuration dans Kubernetes

> **Niveau :** Débutant
> **Durée estimée :** 25 minutes
> **Prérequis :** Kubernetes activé dans Docker Desktop, kubectl fonctionnel

---

## Pourquoi ConfigMap et Secret ?

Dans Docker, on passait les variables avec `-e APP_ENV=production`.
Dans Kubernetes, on les centralise dans des objets dédiés :

- **ConfigMap** : pour les valeurs non sensibles (URLs, noms, paramètres)
- **Secret** : pour les valeurs sensibles (mots de passe, tokens, clés)

> Les deux s'injectent dans les Pods exactement de la même façon.
> La différence est que les Secrets sont (légèrement) protégés.

---

## Étape 1 -- Créer un ConfigMap

### Méthode 1 : depuis la ligne de commande

```bash
kubectl create configmap config-ecole --from-literal=APP_ENV=production --from-literal=APP_VERSION=1.0.0 --from-literal=NOM_ECOLE=ÉTS
```

Voir le ConfigMap créé :
```bash
kubectl get configmap config-ecole
kubectl describe configmap config-ecole
```

### Méthode 2 : depuis un fichier YAML

Examinez le fichier `configmap.yaml` fourni dans ce dossier :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-portail
data:
  APP_ENV: "production"
  APP_VERSION: "2.0.0"
  NOM_INSTITUTION: "ÉTS Formation"
  PORT: "5000"
```

```bash
kubectl apply -f configmap.yaml
kubectl get configmaps
```

**Résultat attendu :**
```
NAME              DATA   AGE
config-ecole      3      1m
config-portail    4      5s
```

---

## Étape 2 -- Créer un Secret

```bash
kubectl create secret generic secret-portail --from-literal=MOT_DE_PASSE_DB=MonMotDePasse123 --from-literal=CLE_API=abc123xyz
```

Voir le Secret :
```bash
kubectl get secret secret-portail
kubectl describe secret secret-portail
```

> Remarquez que les valeurs n'apparaissent PAS dans describe.
> Kubernetes les masque automatiquement.

Pour voir la valeur encodée (base64) :

**Windows (PowerShell) :**
```powershell
kubectl get secret secret-portail -o jsonpath="{.data.MOT_DE_PASSE_DB}"
```

**Mac / Linux :**
```bash
kubectl get secret secret-portail -o jsonpath="{.data.MOT_DE_PASSE_DB}" | base64 --decode
```

---

## Étape 3 -- Utiliser ConfigMap dans un Pod

Examinez `pod-avec-config.yaml` :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-config-test
spec:
  containers:
  - name: app
    image: alpine
    command: ["sh", "-c", "echo APP_ENV=$APP_ENV && echo VERSION=$APP_VERSION && sleep 3600"]
    envFrom:
    - configMapRef:
        name: config-portail   # Injecte TOUTES les variables du ConfigMap
```

```bash
kubectl apply -f pod-avec-config.yaml
kubectl get pods
kubectl logs pod-config-test
```

**Résultat attendu dans les logs :**
```
APP_ENV=production
VERSION=2.0.0
```

---

## Étape 4 -- Injecter seulement certaines variables

Examinez `pod-selection-vars.yaml` :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-vars-select
spec:
  containers:
  - name: app
    image: alpine
    command: ["sh", "-c", "env && sleep 3600"]
    env:
    - name: ENVIRONNEMENT       # Nom de la variable dans le Pod
      valueFrom:
        configMapKeyRef:
          name: config-portail  # Nom du ConfigMap
          key: APP_ENV          # Clé à récupérer
    - name: MDP                 # Variable renommée
      valueFrom:
        secretKeyRef:
          name: secret-portail
          key: MOT_DE_PASSE_DB
```

```bash
kubectl apply -f pod-selection-vars.yaml
kubectl logs pod-vars-select | grep -E "ENVIRONNEMENT|MDP"
```

**Windows (PowerShell) :**
```powershell
kubectl logs pod-vars-select | findstr "ENVIRONNEMENT MDP"
```

---

## Étape 5 -- Monter un ConfigMap comme fichier

On peut aussi injecter un ConfigMap comme un fichier dans le Pod.
Utile pour les fichiers de configuration (nginx.conf, etc.)

Examinez `configmap-fichier.yaml` et `pod-avec-fichier.yaml`.

```bash
kubectl apply -f configmap-fichier.yaml
kubectl apply -f pod-avec-fichier.yaml

# Vérifier que le fichier est monté
kubectl exec pod-fichier-test -- cat /etc/config/parametres.conf
```

---

## Étape 6 -- Modifier un ConfigMap et observer

```bash
# Modifier le ConfigMap
kubectl edit configmap config-portail
```

Changez `APP_VERSION: "2.0.0"` en `APP_VERSION: "2.1.0"` et sauvegardez.

```bash
# Les Pods existants NE voient PAS le changement automatiquement
kubectl logs pod-config-test | grep VERSION
# Affiche encore 2.0.0

# Il faut redémarrer le Pod pour qu'il prenne la nouvelle valeur
kubectl delete pod pod-config-test
kubectl apply -f pod-avec-config.yaml
kubectl logs pod-config-test | grep VERSION
# Affiche maintenant 2.1.0
```

> **Point important :** Un changement de ConfigMap ne redémarre pas
> les Pods automatiquement. Il faut forcer un redémarrage.

---

## Nettoyage

```bash
kubectl delete pod pod-config-test pod-vars-select pod-fichier-test
kubectl delete configmap config-ecole config-portail configmap-nginx
kubectl delete secret secret-portail
```

---

## Récapitulatif

| Objet | Contenu | Exemple d'usage |
|-------|---------|----------------|
| ConfigMap | Variables non sensibles | URL de service, nom d'env, version |
| Secret | Variables sensibles | Mot de passe, token API, certificat |
| envFrom | Injecter tout le ConfigMap | Toutes les variables d'un coup |
| env + valueFrom | Injecter une seule clé | Renommer ou sélectionner |
| volumeMount | Monter comme fichier | Fichier de configuration nginx |

---

Suite : [Lab stockage -- PersistentVolume](../lab-stockage/README.md)
