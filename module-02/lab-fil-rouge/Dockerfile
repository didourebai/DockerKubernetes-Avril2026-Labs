# Dockerfile — IT-Support Portal v1.0
# Module 02 : Premier Dockerfile, version simple

# Image de base : Python 3.12 version légère
FROM python:3.12-slim

# Dossier de travail à l'intérieur du conteneur
WORKDIR /app

# Copier et installer les dépendances Python
# (on copie requirements.txt en premier pour bénéficier du cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Indiquer que l'application écoute sur le port 5000
EXPOSE 5000

# Variables d'environnement par défaut
ENV APP_ENV=développement
ENV APP_VERSION=1.0.0

# Commande exécutée au démarrage du conteneur
CMD ["python", "app.py"]
