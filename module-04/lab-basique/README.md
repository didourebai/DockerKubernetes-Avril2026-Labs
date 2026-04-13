# Module 04 - Lab basique : Optimisation des builds Docker

> **Niveau :** Debutant
> **Duree estimee :** 25 minutes
> **Prerequis :** Module 03 termine

---

## Objectifs

- Comprendre pourquoi l'ordre des instructions dans un Dockerfile est crucial
- Observer le cache Docker en action
- Utiliser `docker init` pour generer un Dockerfile automatiquement
- Analyser la securite d'une image avec Docker Scout

---

## Ce que contient ce dossier

```
module-04/lab-basique/
  app.py              <- Application web Python (deja prete, pas besoin de la modifier)
  requirements.txt    <- Dependances Python (Flask)
  Dockerfile          <- Dockerfile avec le BON ordre
  Dockerfile.mauvais  <- Dockerfile avec le MAUVAIS ordre (pour comparer)
```

> **Note :** Vous n'avez pas besoin de comprendre le code Python.
> `app.py` est une petite page web qui sert uniquement de cobaye pour les exercices de build.
> Vous n'avez qu'a lancer les commandes Docker.

---

## Etape 1 - Se placer dans le bon dossier

**Windows (PowerShell) :**
```powershell
cd labs\module-04\lab-basique
```

**Mac / Linux :**
```bash
cd labs/module-04/lab-basique
```

Verifiez que les fichiers sont presents :
```bash
ls
```

Vous devez voir : `app.py`  `requirements.txt`  `Dockerfile`  `Dockerfile.mauvais`

---

## Etape 2 - Premier build (sans cache)

Construisez l'image une premiere fois. Docker va tout telecharger depuis zero :

```bash
docker build --no-cache -t lab-build:v1 .
```

L'option `--no-cache` force Docker a ne rien reutiliser.
**Notez le temps affiche a la fin.** (environ 20 a 40 secondes selon votre connexion)

---

## Etape 3 - Deuxieme build (avec cache)

Construisez a nouveau **la meme image**, sans `--no-cache` :

```bash
docker build -t lab-build:v1 .
```

**Resultat attendu :** Vous voyez `---> Using cache` sur chaque etape.
Le build se termine en **moins de 2 secondes**.

> **Explication :** Docker a memorise le resultat de chaque etape.
> Comme rien n'a change, il reutilise tout depuis son cache.

---

## Etape 4 - L'ordre des instructions est important

Modifiez **une seule ligne** dans `app.py` :
changez le texte `Lab Docker` en `Mon Lab Docker` et sauvegardez.

**Rebuild avec le bon Dockerfile :**
```bash
docker build -t lab-build:v1 .
```

Observez : seule la ligne `COPY . .` est re-executee.
Le `pip install` reste en cache car `requirements.txt` n'a pas change.
**Le build est rapide.**

---

**Maintenant testez le mauvais ordre :**

```bash
docker build -f Dockerfile.mauvais --no-cache -t lab-build:mauvais .
```

Modifiez a nouveau `app.py` (changez un autre mot) puis rebuilder :

```bash
docker build -f Dockerfile.mauvais -t lab-build:mauvais .
```

Observez : **le `pip install` se relance entierement** meme si `requirements.txt`
n'a pas change, parce que `COPY . .` arrive avant et invalide tout le cache.

---

**La regle a retenir :**

| Ce qui change...            | Doit etre place...          |
|-----------------------------|-----------------------------|
| Rarement (requirements.txt) | En PREMIER dans Dockerfile  |
| Souvent (le code app.py)    | En DERNIER dans Dockerfile  |

---

## Etape 5 - Tester `docker init`

`docker init` analyse votre projet et genere un Dockerfile automatiquement :

```bash
mkdir test-init
cd test-init
echo "print('Bonjour Docker!')" > main.py
docker init
```

Repondez aux questions (choisir Python, version 3.12, port 8000).
Docker genere automatiquement un `Dockerfile`, un `docker-compose.yml`
et un `.dockerignore`.

Comparez le `Dockerfile` genere avec celui du lab.

```bash
cd ..
```

---

## Etape 6 - Analyser la securite avec Docker Scout

```bash
docker scout quickview lab-build:v1
```

Si vous n'etes pas connecte a Docker Hub :
```bash
docker login
docker scout quickview lab-build:v1
```

---

## Etape 7 - Valider un Dockerfile avant de builder

```bash
docker buildx build --check .
```

Testez aussi le mauvais Dockerfile :
```bash
docker buildx build --check -f Dockerfile.mauvais .
```

---

## Nettoyage

```bash
docker rmi lab-build:v1 lab-build:mauvais
```

---

## Recapitulatif

| Commande                       | Ce qu'elle fait                          |
|--------------------------------|------------------------------------------|
| `docker build --no-cache`      | Build complet, sans reutiliser le cache  |
| `docker build`                 | Build avec cache (rapide si rien change) |
| `docker build -f Dockerfile.X` | Utiliser un Dockerfile specifique        |
| `docker init`                  | Genere automatiquement Dockerfile+Compose|
| `docker scout quickview`       | Analyse de securite de l'image           |
| `docker buildx build --check`  | Valide la qualite du Dockerfile          |

---

Suite : [Lab fil rouge - Portail v3 avec BuildKit](../lab-fil-rouge/README.md)
