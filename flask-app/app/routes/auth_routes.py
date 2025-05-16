"""
Routes d'authentification pour l'API
"""
from flask import Blueprint, request, jsonify

from ..services.auth_service import AuthService
from ..services.token_service import TokenService

# Créer un blueprint pour les routes d'authentification
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint pour l'inscription d'un nouvel utilisateur
    ---
    Requiert un JSON avec username, email et password
    """
    # Récupérer les données JSON de la requête
    data = request.get_json()
    
    # Vérifier que les données requises sont présentes
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({
            'success': False,
            'message': 'Données manquantes. username, email et password sont requis.'
        }), 400
    
    # Appeler le service d'authentification pour l'inscription
    user, message, status_code = AuthService.register(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    # Construire la réponse selon le résultat
    if user:
        return jsonify({
            'success': True,
            'message': message,
            'data': user
        }), status_code
    else:
        return jsonify({
            'success': False,
            'message': message
        }), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint pour la connexion d'un utilisateur
    ---
    Requiert un JSON avec email et password
    """
    # Récupérer les données JSON de la requête
    data = request.get_json()
    
    # Vérifier que les données requises sont présentes
    if not all(k in data for k in ('email', 'password')):
        return jsonify({
            'success': False,
            'message': 'Données manquantes. email et password sont requis.'
        }), 400
    
    # Appeler le service d'authentification pour la connexion
    user, message, status_code = AuthService.login(
        email=data['email'],
        password=data['password']
    )
    
    # Construire la réponse selon le résultat
    if user:
        return jsonify({
            'success': True,
            'message': message,
            'data': user
        }), status_code
    else:
        return jsonify({
            'success': False,
            'message': message
        }), status_code

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Endpoint pour vérifier la validité d'un token JWT
    ---
    Requiert un JWT token dans le corps JSON avec la clé 'token'
    """
    # Récupérer les données JSON de la requête
    data = request.get_json() or {}
    
    # Extraire le token uniquement du corps JSON
    token = data.get('token')
    
    if not token:
        return jsonify({
            'success': False,
            'message': 'Token manquant. Veuillez fournir un token JWT dans le corps de la requête.'
        }), 400
        
    # Vérifier la validité du token
    is_valid, payload = TokenService.verify_token(token)
    
    if is_valid:
        return jsonify({
            'success': True,
            'message': 'Token valide',
            'user_id': payload.get('user_id')
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': payload.get('error', 'Token invalide')
        }), 401