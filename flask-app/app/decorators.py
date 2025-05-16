"""
Décorateurs pour l'application
"""
from functools import wraps
from flask import request, jsonify
from .services.token_service import TokenService

def token_required(f):
    """
    Décorateur pour protéger les routes qui nécessitent une authentification
    Vérifie la présence et la validité du token JWT
    Vérifie OBLIGATOIREMENT que l'ID utilisateur fourni dans la requête correspond à celui du token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        request_user_id = None
        
        # Chercher le token dans les headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Token invalide'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token manquant'
            }), 401
        
        # Décodage simple du token pour récupérer le user_id qu'il contient
        is_valid_token, token_payload = TokenService.verify_token(token)
        if not is_valid_token:
            return jsonify({
                'success': False,
                'message': token_payload.get('error', 'Token invalide')
            }), 401
            
        token_user_id = token_payload.get('user_id')
        
        # Récupérer l'ID utilisateur depuis les paramètres de requête ou le corps
        if request.method == 'GET':
            request_user_id = request.args.get('user_id')
        else:
            if request.is_json:
                request_user_id = request.json.get('user_id')

        # Si aucun ID utilisateur n'est fourni dans la requête, renvoyer une erreur
        if not request_user_id:
            return jsonify({
                'success': False,
                'message': "L'ID utilisateur est obligatoire"
            }), 400
        
        # Convertir en entier si nécessaire
        if isinstance(request_user_id, str) and request_user_id.isdigit():
            request_user_id = int(request_user_id)
        
        # Vérifier que l'ID utilisateur de la requête correspond à celui du token
        if token_user_id != request_user_id:
            return jsonify({
                'success': False,
                'message': "Accès non autorisé pour cet utilisateur T"
            }), 403
            
        # Ajouter l'ID de l'utilisateur aux arguments de la fonction
        kwargs['user_id'] = token_user_id
        return f(*args, **kwargs)
        
    return decorated