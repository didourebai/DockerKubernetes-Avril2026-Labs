# Guide pour les formateurs

## Structure d'un lab

Chaque lab suit le même modèle :
- `README.md` : instructions étape par étape en français
- Fichiers de code prêts à l'emploi (Dockerfile, YAML, etc.)
- Résultat attendu indiqué clairement à chaque étape

## Convention de nommage des images

| Module | Tag image | Commande build |
|--------|-----------|----------------|
| 02 | `it-portal:v1` | `docker build -t it-portal:v1 .` |
| 03 | `it-portal:v2` | `docker buildx build -t it-portal:v2 .` |
| 04 | `it-portal:v3` | `docker buildx build -t it-portal:v3 .` |
| 05 | Compose build | `docker-compose build` |
| 06 | `it-portal:v5` | `docker build -t it-portal:v5 app/` |
| 07 | `it-portal:v6` | `docker build -t it-portal:v6 app/` |
| 08 | `it-portal:v7` | `docker build -t it-portal:v7 app/` |

## Environnement testé

- Docker Desktop 4.30+ (Windows 11 / macOS 14+)
- Kubernetes 1.28+ (intégré à Docker Desktop)
- Helm 3.14+
