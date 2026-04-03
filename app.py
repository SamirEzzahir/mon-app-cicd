# app.py — Application Flask simple

from flask import Flask, jsonify
import os

app = Flask(__name__)

# Variable de version (on la changera pour le bonus v1→v2)
VERSION = os.getenv('APP_VERSION', '1.0')


@app.route('/')
def home():
    return f'''
    <html>
    <head><title>Mon App CI/CD</title></head>
    <body style="font-family:Arial; margin:40px; background:#0D1117; color:white">
        <h1>🚀 Mon Application CI/CD</h1>
        <p>Version : <strong>{VERSION}</strong></p>
        <p>Déployée automatiquement via Jenkins + Docker !</p>
        <p style="color:#56D364">✅ Pipeline exécuté avec succès</p>
    </body>
    </html>
    '''


@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'version': VERSION
    })


@app.route('/info')
def info():
    return jsonify({
        'app': 'mon-app-cicd',
        'version': VERSION,
        'description': 'TP CI/CD Pipeline'
    })


# ⚠️ OPTIONNEL (utile seulement en local, pas nécessaire avec Gunicorn)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
