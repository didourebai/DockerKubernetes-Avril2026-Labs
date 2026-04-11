# syntax=docker/dockerfile:1
# Module 04 : BuildKit cache mount

FROM python:3.12-slim AS builder
WORKDIR /install
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/deps -r requirements.txt

FROM python:3.12-slim AS final
ARG VERSION=3.0.0
ARG BUILD_DATE=unknown
LABEL maintainer="it-support@institution.ca" version="${VERSION}"
WORKDIR /app
COPY --from=builder /deps /usr/local
COPY app.py .
COPY templates/ templates/
COPY static/ static/
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser
ENV APP_ENV=production APP_VERSION=${VERSION} PORT=5000
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
