# Lab Stockage Kubernetes -- PersistentVolume et PersistentVolumeClaim

> **Niveau :** Débutant
> **Durée estimée :** 25 minutes
> **Prérequis :** Lab ConfigMap terminé

---

## Le problème sans stockage persistant

Un Pod Kubernetes est éphémère comme un conteneur Docker.
Quand il redémarre, ses données disparaissent.

**Démonstration :**

```bash
# Créer un Pod qui écrit un fichier
kubectl run pod-ephemere --image=alpine --restart=Never \
  -- sh -c "echo 'Données importantes' > /tmp/données.txt && sleep 30"

kubectl exec pod-ephemere -- cat /tmp/données.txt
# Données importantes

# Supprimer et recréer le Pod
kubectl delete pod pod-ephemere
kubectl run pod-ephemere --image=alpine --restart=Never \
  -- sh -c "cat /tmp/données.txt && sleep 30"

kubectl logs pod-ephemere
# Erreur : fichier introuvable
```

Nettoyage :
```bash
kubectl delete pod pod-ephemere
```

---

## Les objets de stockage Kubernetes

```
Administrateur IT                 Développeur / Application
-----------------                 -------------------------
PersistentVolume (PV)   <----     PersistentVolumeClaim (PVC)
"J'offre 1 Go de stockage"        "J'ai besoin de 500 Mo"

Kubernetes fait le lien automatiquement entre le PV et le PVC.

StorageClass : permet la création automatique de PV à la demande
(utilisée dans Docker Desktop et les clouds)
```

---

## Étape 1 -- Créer un PersistentVolumeClaim

Avec Docker Desktop, on n'a pas besoin de créer les PV manuellement.
La **StorageClass par défaut** les crée automatiquement.

Examinez `pvc-portail.yaml` :

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-données-portail
spec:
  accessModes:
    - ReadWriteOnce      # Un seul Pod peut écrire à la fois
  resources:
    requests:
      storage: 100Mi     # 100 mégaoctets demandés
```

```bash
kubectl apply -f pvc-portail.yaml
kubectl get pvc
```

**Résultat attendu :**
```
NAME                   STATUS   VOLUME     CAPACITY   ACCESS MODES
pvc-données-portail    Bound    pvc-xxx    100Mi      RWO
```

> `STATUS: Bound` signifie que Kubernetes a trouvé (ou créé) un volume
> correspondant et l'a associé au PVC.

---

## Étape 2 -- Utiliser le PVC dans un Pod

Examinez `pod-avec-pvc.yaml` :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-stockage-test
spec:
  containers:
  - name: app
    image: alpine
    command: ["sh", "-c", "sleep 3600"]
    volumeMounts:
    - name: données          # Nom du volume (défini ci-dessous)
      mountPath: /app/data   # Dossier dans le Pod
  volumes:
  - name: données
    persistentVolumeClaim:
      claimName: pvc-données-portail   # Le PVC créé à l'étape 1
```

```bash
kubectl apply -f pod-avec-pvc.yaml
kubectl get pods
```

Écrire des données dans le volume :
```bash
kubectl exec pod-stockage-test -- sh -c "echo 'Serveur-Web-01: actif' > /app/data/serveurs.txt"
kubectl exec pod-stockage-test -- sh -c "echo 'NAS-01: actif' >> /app/data/serveurs.txt"
kubectl exec pod-stockage-test -- cat /app/data/serveurs.txt
```

---

## Étape 3 -- Vérifier la persistance

Supprimer le Pod (PAS le PVC) :

```bash
kubectl delete pod pod-stockage-test
kubectl get pvc
# Le PVC est toujours là !
```

Recréer un nouveau Pod avec le MÊME PVC :

```bash
kubectl apply -f pod-avec-pvc.yaml
kubectl exec pod-stockage-test -- cat /app/data/serveurs.txt
# Serveur-Web-01: actif
# NAS-01: actif
# Les données sont intactes !
```

---

## Étape 4 -- Déploiement avec stockage persistant

Dans la réalité, on utilise un Deployment (pas un Pod direct).
Examinez `deployment-avec-pvc.yaml` :

```bash
kubectl apply -f deployment-avec-pvc.yaml
kubectl get pods
kubectl get pvc
```

Écrire des données depuis le Pod du Deployment :

```bash
# Trouver le nom du Pod
kubectl get pods -l app=portail-stockage

# Écrire dans le volume
kubectl exec deploy/portail-stockage -- sh -c "echo 'Données du déploiement' > /app/data/deploy.txt"
```

Simuler un crash du Pod :

```bash
# Supprimer le Pod (Kubernetes en recrée un automatiquement)
kubectl delete pod -l app=portail-stockage

# Attendre le nouveau Pod
kubectl get pods -w
# Ctrl+C quand STATUS=Running

# Vérifier que les données sont toujours là
kubectl exec deploy/portail-stockage -- cat /app/data/deploy.txt
# Données du déploiement
```

---

## Étape 5 -- Les modes d'accès

| Mode | Signification | Cas d'usage |
|------|--------------|-------------|
| ReadWriteOnce (RWO) | Un seul noeud peut lire et écrire | Base de données |
| ReadOnlyMany (ROX) | Plusieurs noeuds peuvent lire | Fichiers statiques partagés |
| ReadWriteMany (RWX) | Plusieurs noeuds peuvent lire et écrire | Stockage partagé NFS |

> Sur Docker Desktop en local : seul RWO est supporté nativement.
> RWX nécessite un stockage réseau (NFS, Azure Files, EFS...)

---

## Nettoyage

```bash
kubectl delete deployment portail-stockage
kubectl delete pod pod-stockage-test
kubectl delete pvc pvc-données-portail
```

> **Important :** Supprimer le PVC ne supprime pas les données
> immédiatement sur certains clouds. Vérifiez la politique
> de rétention (Reclaim Policy) de votre StorageClass.

```bash
# Voir la politique de rétention
kubectl get storageclass
```

---

## Récapitulatif

| Objet | Rôle | Qui le crée |
|-------|------|-------------|
| StorageClass | Définit le type de stockage disponible | Administrateur |
| PersistentVolume (PV) | Espace de stockage réel | Administrateur (ou auto) |
| PersistentVolumeClaim (PVC) | Demande de stockage | Développeur |
| volumeMount | Monte le PVC dans un conteneur | Dans le manifest Pod/Deployment |

---

Suite : [Lab déploiement -- Rolling Update et Rollback](../lab-deploiement/README.md)
