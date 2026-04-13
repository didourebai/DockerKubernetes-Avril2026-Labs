"""
Application web minimaliste pour les exercices de build Docker.
Pas besoin de comprendre ce code -- il sert uniquement de base pour les labs.
"""
from flask import Flask
import datetime

app = Flask(__name__)

@app.route("/")
def bonjour():
    heure = datetime.datetime.now().strftime('%H:%M:%S')
    return (
        "<html><body style='font-family:sans-serif;padding:40px;background:#f0f2f5'>"
        "<h1>Lab Docker - Optimisation des builds</h1>"
        "<p>Serveur demarre a : <strong>" + heure + "</strong></p>"
        "<p>Cette page sert a tester les builds Docker.</p>"
        "</body></html>"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
