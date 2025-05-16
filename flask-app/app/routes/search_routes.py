"""
Routes pour la gestion des recherches
"""
from flask import Blueprint, request, jsonify
from ..services.search_service import SearchService
from ..decorators import token_required
from flask import Blueprint, session, jsonify
from app.services.reservation_service import ReservationService

# Créer un blueprint pour les routes de recherche
search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['POST'])
@token_required
def search_station(*args, **kwargs):
    """
    Endpoint pour rechercher une station
    ---
    Requiert un JSON avec search
    Requiert un token JWT valide
    """
    try:
        # Récupérer l'ID utilisateur depuis le token JWT
        token_user_id = kwargs.get('user_id')

        # Récupérer les données JSON de la requête
        data = request.get_json()
        if not data or 'search' not in data:
            return jsonify({
                'error': "Paramètre 'search' manquant",
                'error_code': 'MISSING_PARAMETER',
                'token': True
            }), 400

        search_term = data['search']

        # Rechercher la station via l'API externe
        success, message, response_data, status_code = SearchService.search_station(search_term)
        if not success:
            return jsonify(response_data), status_code

       
        if response_data.get('should_save', False):
            result = 1 
        else:
            result = 0
            
        station_id = response_data.get('station_id')
            
        success, db_message, db_data, db_status = SearchService.save_search(
            token_user_id,
            search_term,
            station_id,
            result
        )

        if not success:
            return jsonify(db_data), db_status

        if response_data.get('should_save') != True:
            # Si la recherche n'a pas abouti
            return jsonify({
                'message': "Station / Adresse non trouvée",
                'error_code': 'NOT_FOUND'
            }), 404
        else:
            return jsonify({
                'lat': response_data.get('lat'),
                'lon': response_data.get('lon'),
                'message': message
            }), 200

    except Exception as e:
        return jsonify({
            'error': f"Erreur inattendue: {str(e)}",
            'error_code': 'UNKNOWN_ERROR',
            'token': True
        }), 500


@search_bp.route('/delete', methods=['POST'])
@token_required
def delete_search(*args, **kwargs):
    """
    Endpoint pour supprimer une recherche par son ID
    ---
    Requiert un JSON avec id_search ET user_id
    Requiert un token JWT valide
    Le user_id dans la requête doit correspondre à celui du token (OBLIGATOIRE)
    """
    try:
        # Récupérer l'ID utilisateur depuis le token JWT
        token_user_id = kwargs.get('user_id')
        
        # Récupérer les données JSON de la requête
        data = request.get_json()
        
        # Vérifier que les paramètres obligatoires sont présents
        required_params = ['id_search', 'user_id']
        missing_params = [param for param in required_params if param not in data]
        
        if missing_params:
            return jsonify({
                'error': f"Paramètre(s) manquant(s): {', '.join(missing_params)}",
                'error_code': 'MISSING_PARAMETER',
                'token': False
            }), 400
        
        id_search = data['id_search']

            
        # Appeler le service de recherche pour la suppression avec l'ID utilisateur
        success, message, response_data, status_code = SearchService.delete_search(id_search, token_user_id)
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'user_id': token_user_id  # Retourner l'ID utilisateur pour confirmer
            }), status_code
        else:
            return jsonify(response_data), status_code
            
    except Exception as e:
        return jsonify({
            'error': f"Erreur inattendue: {str(e)}",
            'error_code': 'UNKNOWN_ERROR',
            'token': False
        }), 500
    
@search_bp.route('/', methods=['GET'])
@token_required
def get_user_searches(*args, **kwargs):
     """
     Endpoint pour récupérer les recherches de l'utilisateur authentifié
     Requiert un token JWT valide
     """
     try:
         user_id = kwargs.get('user_id')  # fourni par le décorateur token_required
 
         # Appel au service pour récupérer les recherches
         success, message, data, status_code = SearchService.get_searches_by_user(user_id)
         
         if success:
             return jsonify({
                 'success': True,
                 'message': message,
                 'data': data
             }), status_code
         else:
             return jsonify({
                 'success': False,
                 'message': message
             }), status_code
 
     except Exception as e:
         return jsonify({
             'error': f"Erreur serveur: {str(e)}",
             'error_code': 'SERVER_ERROR'
         }), 500
     
     