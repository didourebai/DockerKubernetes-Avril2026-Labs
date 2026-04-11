"""
IT-Support Portal v4.0 — Avec historique SQLite
"""
from flask import Flask, render_template, jsonify
import platform, socket, datetime, os, sqlite3

app = Flask(__name__)
DB_PATH = "/app/data/portail.db"

def init_db():
    """Initialise la base de données SQLite."""
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS connexions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horodatage TEXT NOT NULL,
            hostname TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_connexion():
    """Enregistre une connexion dans la base."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO connexions (horodatage, hostname) VALUES (?, ?)",
                     (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      socket.gethostname()))
        conn.commit()
        conn.close()
    except Exception:
        pass

@app.route("/")
def index():
    log_connexion()
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "environment": os.environ.get("APP_ENV", "développement"),
        "version": os.environ.get("APP_VERSION", "4.0.0"),
    })

@app.route("/api/services")
def services():
    return jsonify([
        {"nom": "Serveur Web (Nginx)",      "statut": "actif",   "icone": "🌐"},
        {"nom": "Application (Flask)",       "statut": "actif",   "icone": "🐍"},
        {"nom": "Base de données (SQLite)",  "statut": "actif",   "icone": "🗄️"},
        {"nom": "Serveur de fichiers (NAS)", "statut": "actif",   "icone": "💾"},
        {"nom": "VPN",                       "statut": "inactif", "icone": "🔒"},
    ])

@app.route("/api/historique")
def historique():
    """Retourne les 10 dernières connexions."""
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT horodatage, hostname FROM connexions ORDER BY id DESC LIMIT 10"
        ).fetchall()
        conn.close()
        return jsonify([{"horodatage": r[0], "hostname": r[1]} for r in rows])
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"statut": "ok"}), 200

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
