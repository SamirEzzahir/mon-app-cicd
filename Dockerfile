# Dockerfile
# Étape 1 : image de base Python légère (slim = sans les extras inutiles)
FROM python:3.11-slim

# Étape 2 : définir le répertoire de travail dans le conteneur

WORKDIR /app
# Étape 3 : copier SEULEMENT requirements.txt en premier
# (optimisation : Docker met en cache cette couche si requirements.txt nechange pas)

COPY requirements.txt .
# Étape 4 : installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : copier le code de l'application
COPY app.py .

# Étape 6 : exposer le port 5000 (documentation + convention)
EXPOSE 5000

# Étape 7 : commande de démarrage avec gunicorn (production-ready)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]