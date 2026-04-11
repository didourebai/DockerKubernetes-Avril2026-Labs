# Dockerfile — IT-Support Portal v2.0
# Module 03 : Build multi-stage, utilisateur non-root, healthcheck

# ============================================================
# ÉTAPE 1 : Installation des dépendances Python
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /install

# Copier uniquement requirements.txt pour optimiser le cache
# Si requirements.txt ne change pas, cette couche est réutilisée
COPY requirements.txt .

# Installer dans un préfixe séparé (sera copié dans l'image finale)
RUN pip install --no-cache-dir --prefix=/deps -r requirements.txt


# ============================================================
# ÉTAPE 2 : Image finale légère
# ============================================================
FROM python:3.12-slim AS final

# Métadonnées
ARG VERSION=2.0.0
ARG BUILD_DATE=unknown
LABEL maintainer="it-support@institution.ca"
LABEL version="${VERSION}"
LABEL build-date="${BUILD_DATE}"
LABEL description="IT-Support Portal - Portail de surveillance IT"

# Dossier de travail
WORKDIR /app

# Copier les dépendances depuis l'étape builder
COPY --from=builder /deps /usr/local

# Copier le code source
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Créer et utiliser un utilisateur non-root (bonne pratique de sécurité)
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Variables d'environnement par défaut
ENV APP_ENV=production
ENV APP_VERSION=${VERSION}
ENV PORT=5000

# Port exposé
EXPOSE 5000

# Vérification de santé automatique
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Démarrage avec gunicorn (serveur WSGI pour la production)
# 2 workers pour gérer plusieurs requêtes simultanées
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
