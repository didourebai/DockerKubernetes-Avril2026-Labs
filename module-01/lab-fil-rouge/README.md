# Module 01 — Lab fil rouge : Découverte du IT-Support Portal

> **Niveau :** Débutant  
> **Durée estimée :** 15 minutes  
> **Prérequis :** Lab basique du module 01 terminé

---

## Contexte

Vous faites le support technique dans une institution scolaire.  
Les professeurs vous demandent souvent l'état de l'infrastructure : "Est-ce que le serveur web fonctionne ? La base de données est-elle active ?"

Votre objectif : déployer un **portail web de surveillance** interne appelé **IT-Support Portal**.

Dans ce premier module, vous allez simplement **découvrir** le portail en le lançant depuis une image déjà prête.

---

## Architecture du portail (version finale)

```
Navigateur
    │
    ▼
┌─────────────┐
│   Nginx     │  ← Sert les pages web (HTML/CSS)
│  (port 80)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Python    │  ← Fournit les données (API)
│   Flask     │
│  (port 5000)│
└─────────────┘
```

---

## Étape 1 — Ouvrir un terminal dans le bon dossier

**Windows (PowerShell) :**
```powershell
cd C:\chemin\vers\labs\module-01\lab-fil-rouge
```

**Mac (Terminal) :**
```bash
cd ~/chemin/vers/labs/module-01/lab-fil-rouge
```

Vérifiez que le fichier `demo.py` est présent :
```bash
ls
# Vous devez voir : demo.py  README.md
```

---

## Étape 2 — Lancer le portail de démonstration

Copiez-collez cette commande **exactement** (une seule ligne) :

**Windows (PowerShell) :**
```powershell
docker run -d -p 8080:5000 --name it-portal-demo -e APP_ENV=demonstration -v ${PWD}/demo.py:/app/demo.py python:3.12-slim python3 /app/demo.py
```

**Mac / Linux (Terminal) :**
```bash
docker run -d -p 8080:5000 --name it-portal-demo -e APP_ENV=demonstration -v $(pwd)/demo.py:/app/demo.py python:3.12-slim python3 /app/demo.py
```

**Explication des options :**
- `-d` : en arrière-plan
- `-p 8080:5000` : port 8080 de votre machine → port 5000 du conteneur
- `--name it-portal-demo` : nom du conteneur (notez les **deux tirets** `--`)
- `-e APP_ENV=demonstration` : variable d'environnement
- `-v .../demo.py:/app/demo.py` : monter le fichier Python dans le conteneur
- `python:3.12-slim` : image de base Python

Ouvrez votre navigateur : **http://localhost:8080**

---

## Étape 3 — Voir les logs du portail

```bash
docker logs it-portal-demo
```

Rafraîchissez la page dans votre navigateur, puis relancez la commande — de nouvelles lignes apparaissent.

---

## Étape 4 — Explorer l'intérieur du conteneur

```bash
docker exec -it it-portal-demo sh
```

Vous êtes maintenant **à l'intérieur** du conteneur. Essayez :

```sh
ls /app          # Voir le fichier demo.py monté
python3 --version  # Vérifier Python
hostname         # Le nom du conteneur (une suite de lettres/chiffres)
exit             # Revenir à votre terminal
```

> 💡 **Important :** Tout ce que vous faites à l'intérieur du conteneur disparaît à son arrêt. Le conteneur est isolé de votre machine.

---

## Étape 5 — Arrêter et nettoyer

```bash
docker stop it-portal-demo
docker rm it-portal-demo
```

---

## Ce que vous avez appris

- `--name` s'écrit avec **deux tirets** (common mistake : `-name` avec un seul tiret)
- `-v` monte un fichier de votre machine dans le conteneur
- Un conteneur **isole** une application de votre système
- On peut **entrer dedans** pour déboguer avec `docker exec`

---

## Dans le prochain module

Vous allez découvrir comment le portail est **construit** : le Dockerfile, les images, et comment Docker fonctionne en profondeur.

---

➡️ **Retour :** [Lab basique](../lab-basique/README.md) | **Suivant :** [Module 02](../../module-02/lab-basique/README.md)
