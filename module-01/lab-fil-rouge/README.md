# Module 01 — Lab fil rouge : Découverte du IT-Support Portal

> **Niveau :** Débutant  
> **Durée estimée :** 15 minutes  
> **Prérequis :** Lab basique du module 01 terminé

---

## 🎯 Contexte

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

## Étape 1 — Lancer le portail depuis une image existante

Pour cette démonstration, nous utilisons l'image officielle Python pour simuler le portail.

```bash
docker run -d \
  -p 8080:5000 \
  --name it-portal-demo \
  -e APP_ENV=demonstration \
  -e APP_VERSION=1.0.0 \
  python:3.12-slim \
  python3 -c "
import http.server, socketserver, json

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = '''<html><body style=\"font-family:sans-serif;padding:40px;background:#f0f2f5\">
        <h1>🖥️ IT-Support Portal</h1>
        <p>✅ Le conteneur fonctionne !</p>
        <p>Dans les prochains modules, ce portail sera complet.</p>
        </body></html>'''
        self.wfile.write(html.encode())
    def log_message(self, *args): pass

with socketserver.TCPServer(('', 5000), Handler) as httpd:
    httpd.serve_forever()
"
```

Ouvrez : **http://localhost:8080**

---

## Étape 2 — Inspecter le conteneur en cours d'exécution

```bash
# Voir les détails du conteneur
docker inspect it-portal-demo
```

C'est beaucoup d'informations ! Cherchez la section `"Env"` pour voir les variables d'environnement.

---

## Étape 3 — Voir les logs du portail

```bash
docker logs it-portal-demo
```

Les logs montrent chaque requête reçue par le serveur.

Rafraîchissez la page dans votre navigateur puis relancez `docker logs` : vous verrez de nouvelles lignes.

---

## Étape 4 — Explorer l'intérieur du conteneur

```bash
docker exec -it it-portal-demo sh
```

Vous êtes maintenant **à l'intérieur** du conteneur. Essayez :

```sh
ls /          # Voir les dossiers du système
python3 --version  # Vérifier Python
hostname      # Voir le nom du conteneur
exit          # Revenir à votre terminal
```

> 💡 **Important :** Tout ce que vous faites à l'intérieur du conteneur disparaît à son arrêt. Le conteneur est isolé de votre machine.

---

## Étape 5 — Arrêter et nettoyer

```bash
docker stop it-portal-demo
docker rm it-portal-demo
```

---

## 📝 Ce que vous avez appris

- Un conteneur **isole** une application de votre système
- On peut lui passer des **variables d'environnement** (`-e`)
- On peut voir ses **logs** en temps réel
- On peut **entrer dedans** pour déboguer avec `docker exec`

---

## 🔮 Dans le prochain module

Vous allez découvrir comment le portail est **construit** : le Dockerfile, les images, et comment Docker fonctionne en profondeur.

---

➡️ **Retour :** [Lab basique](../lab-basique/README.md) | **Suivant :** [Module 02](../../module-02/lab-basique/README.md)
