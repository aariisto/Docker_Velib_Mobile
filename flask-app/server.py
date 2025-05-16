"""
Point d'entrée principal pour le serveur Flask avec architecture modulaire
"""
import os
import pymysql
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Installer PyMySQL comme MySQLdb pour Flask-SQLAlchemy
pymysql.install_as_MySQLdb()

# Charger les variables d'environnement
load_dotenv()

# ==================================================================================
# TODO: PAS OUBLIER DE CHANGER LE LIEN DE CONNEXION MYSQL DANS LE FICHIER .env
#       ou dans app/config.py selon votre configuration
# ==================================================================================

def create_app():
    """Crée et configure l'application Flask"""
    # Créer l'instance Flask
    app = Flask(__name__)
    
    # Configurer l'application depuis config.py
    from app.config import Config
    app.config.from_object(Config)
    
    # Activer CORS
    CORS(app)
    
    # Initialiser les extensions
    from app.extensions import db
    db.init_app(app)
    
    # Enregistrer les blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.hello_routes import hello_bp
    from app.routes.search_routes import search_bp
    from app.routes.reservation_routes import reservation_bp
    from app.routes.station_routes import station_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(hello_bp, url_prefix='/api/hello')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(reservation_bp, url_prefix='/api/reservation')
    app.register_blueprint(station_bp, url_prefix='/api/station')

    # Route racine
    @app.route('/')
    def index():
        return "API Flask en cours d'exécution. Consultez la documentation pour les endpoints disponibles."
    
    return app

if __name__ == '__main__':
    # Créer l'application
    app = create_app()
    
    # Démarrer le serveur
    port = int(os.environ.get('PORT', 5001))
    print(f"Démarrage du serveur sur le port {port}...")
    print("N'OUBLIEZ PAS DE VÉRIFIER LA CONNEXION MYSQL DANS LES PARAMÈTRES DE CONFIGURATION!")
    app.run(host='0.0.0.0', port=port, debug=True)