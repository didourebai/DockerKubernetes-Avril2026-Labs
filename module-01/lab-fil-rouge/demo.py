import http.server
import socketserver
import os

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = b"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>IT-Support Portal</title></head>
<body style="font-family:sans-serif;padding:40px;background:#f0f2f5">
  <h1>IT-Support Portal</h1>
  <p>Le conteneur fonctionne !</p>
  <p>Dans les prochains modules, ce portail sera complet.</p>
</body>
</html>"""
        self.wfile.write(html)

    def log_message(self, *args):
        pass

with socketserver.TCPServer(('', 5000), Handler) as httpd:
    httpd.serve_forever()
