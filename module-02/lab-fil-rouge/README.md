# Module 02 — Lab fil rouge : Containerisation du IT-Support Portal

> **Niveau :** Débutant  
> **Durée estimée :** 20 minutes

---

## 🎯 Objectif

Écrire votre **premier Dockerfile** pour containeriser le IT-Support Portal.  
À la fin, le portail tournera dans un conteneur Docker sur votre machine.

---

## Étape 1 — Récupérer le code source

Placez-vous dans le dossier du lab :

```bash
cd labs/module-02/lab-fil-rouge
```

Le dossier contient déjà les fichiers du portail. Vérifiez :

```bash
ls
```

**Vous devriez voir :**
```
Dockerfile
app.py
requirements.txt
templates/
static/
```

---

## Étape 2 — Lire le code de l'application

Ouvrez `app.py` avec un éditeur de texte (Notepad, VS Code…).

> 💡 **Pas de panique !** Vous n'avez pas besoin de comprendre le code Python en détail. Retenez juste que :
> - C'est une **application web** qui écoute sur le **port 5000**
> - Elle répond à l'adresse `/` (page principale) et `/api/status` (données JSON)

---

## Étape 3 — Comprendre le Dockerfile

Ouvrez le fichier `Dockerfile`. Chaque ligne sera expliquée :

```dockerfile
# --- Étape 1 : Choisir l'image de base ---
FROM python:3.12-slim

# --- Étape 2 : Définir le dossier de travail dans le conteneur ---
WORKDIR /app

# --- Étape 3 : Copier et installer les dépendances Python ---
COPY requirements.txt .
RUN pip install -r requirements.txt

# --- Étape 4 : Copier le reste du code ---
COPY . .

# --- Étape 5 : Indiquer le port utilisé ---
EXPOSE 5000

# --- Étape 6 : Commande de démarrage ---
CMD ["python", "app.py"]
```

> 💡 **Analogie :** Le Dockerfile est comme une **recette de cuisine**. Chaque instruction est une étape. Docker suit ces étapes pour "cuisiner" votre image.

---

## Étape 4 — Construire l'image

```bash
docker build -t it-portal:v1 .
```

**Explication :**
- `docker build` : construire une image
- `-t it-portal:v1` : nommer l'image `it-portal` avec le tag `v1`
- `.` : le Dockerfile se trouve dans le dossier courant

Regardez les lignes qui défilent — chaque ligne correspond à une instruction du Dockerfile.

Vérifiez que l'image est créée :
```bash
docker images | grep it-portal
```

---

## Étape 5 — Lancer le portail

```bash
docker run -d -p 8080:5000 --name it-portal -e APP_ENV=développement -e APP_VERSION=1.0.0 it-portal:v1
```

Ouvrez votre navigateur : **http://localhost:8080**

**Vous devriez voir le IT-Support Portal avec :**
- Le nom d'hôte du conteneur
- La version Python
- L'état des services IT
- L'environnement de déploiement

---

## Étape 6 — Vérifier les logs

```bash
docker logs it-portal
```

Rafraîchissez la page du portail et relancez la commande — les nouvelles requêtes apparaissent dans les logs.

---

## Étape 7 — Tester l'API directement

Ouvrez votre navigateur sur : **http://localhost:8080/api/status**

Vous verrez les données JSON brutes retournées par Python :
```json
{
  "hostname": "abc123def456",
  "os": "Linux",
  "python_version": "3.12.x",
  "timestamp": "2024-01-15 14:30:00",
  "environment": "développement",
  "version": "1.0.0"
}
```

---

## Étape 8 — Arrêter et nettoyer

```bash
docker stop it-portal
docker rm it-portal
```

---

## 📝 Ce que vous avez accompli

✅ Vous avez écrit votre premier Dockerfile  
✅ Vous avez construit une image Docker depuis du code Python  
✅ Vous avez lancé un portail web dans un conteneur  
✅ Vous avez passé des variables d'environnement pour configurer l'application

---

## 🔮 Dans le prochain module

Vous allez apprendre à **optimiser** ce Dockerfile pour que l'image soit plus petite et que les builds soient plus rapides.

---

➡️ **Retour :** [Lab basique](../lab-basique/README.md) | **Suivant :** [Module 03](../../module-03/lab-basique/README.md)
