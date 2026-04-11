"""
IT-Support Portal - Application Python Flask
Portail web interne pour la gestion de l'infrastructure IT
"""

from flask import Flask, render_template, jsonify
import platform
import socket
import datetime
import os

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Page principale
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Page d'accueil du portail."""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# API : informations système
# ---------------------------------------------------------------------------

@app.route("/api/status")
def status():
    """Retourne l'état du système sous forme JSON."""
    info = {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "environment": os.environ.get("APP_ENV", "développement"),
        "version": os.environ.get("APP_VERSION", "1.0.0"),
    }
    return jsonify(info)


@app.route("/api/services")
def services():
    """Liste des services IT surveillés."""
    services_list = [
        {"nom": "Serveur Web",      "statut": "actif",   "icone": "🌐"},
        {"nom": "Base de données",  "statut": "actif",   "icone": "🗄️"},
        {"nom": "Serveur de fichiers (NAS)", "statut": "actif", "icone": "💾"},
        {"nom": "VPN",              "statut": "inactif", "icone": "🔒"},
        {"nom": "Serveur de sauvegardes", "statut": "actif", "icone": "📦"},
    ]
    return jsonify(services_list)


@app.route("/health")
def health():
    """Point de contrôle de santé (utilisé par Kubernetes)."""
    return jsonify({"statut": "ok"}), 200


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("APP_ENV", "développement") == "développement"
    app.run(host="0.0.0.0", port=port, debug=debug)
