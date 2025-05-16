# Utiliser une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installation des outils nécessaires
RUN apt-get update && apt-get install -y wget netcat-traditional

# Installation de wait-for-it pour attendre que Flask soit prêt
RUN wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Créer un script d'attente pour MySQL
COPY requirements.txt /app/
RUN echo '#!/bin/bash\n\
echo "Waiting for MySQL to be ready..."\n\
wait-for-it.sh mysql:3306 --timeout=180\n\
echo "Waiting for MySQL to initialize (15 seconds)..."\n\
sleep 15\n\
echo "Waiting for Flask API to be ready..."\n\
wait-for-it.sh flask-app:5001 --timeout=120\n\
echo "Starting data insertion script..."\n\
python insersion.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier les scripts Python dans le conteneur
COPY . /app/

# Exécuter le script de démarrage
CMD ["/app/start.sh"]
