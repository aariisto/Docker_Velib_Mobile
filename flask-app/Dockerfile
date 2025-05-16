# Utiliser l'image officielle Python
FROM python:3.9

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances en premier pour optimiser le cache de Docker
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet
COPY . .

# Exposer le port 5001 (port configuré dans server.py)
EXPOSE 5001

# Lancer directement l'application Flask sans attendre MySQL
CMD ["python", "server.py"]
