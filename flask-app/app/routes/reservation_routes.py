from flask import Blueprint, request, jsonify
from ..decorators import token_required
from app.services.reservation_service import ReservationService
import logging

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/', methods=['POST'])
@token_required
def post_reservation(*args, **kwargs):
    """
    Crée une nouvelle réservation
    La validation du token et de l'utilisateur est gérée par le décorateur token_required
    """
    try:
        # Récupération de l'ID utilisateur du token
        user_id = kwargs.get('user_id')
        
        # Vérification des données de la requête
        if not request.is_json:
            return jsonify({
                "success": False,
                "message": "Format JSON requis"
            }), 400
        
        # Récupération des données de la requête
        data = request.json
        
        # S'assurer que le client_id correspond à l'utilisateur authentifié
        data['client_id'] = user_id  # Force l'ID client à celui du token pour la sécurité
        
        # Appel au service pour créer la réservation
        success, message, result, status = ReservationService.create_reservation(data)
        
        if not success:
            return jsonify({
                "success": False,
                "message": message,
                "error": result
            }), status
        
        # Réponse en cas de succès
        return jsonify({
            "success": True,
            "message": message,
            "data": result
        }), status
        
    except Exception as e:
        # Logging de l'erreur
        logging.error(f"Erreur lors de la création d'une réservation: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Une erreur inattendue s'est produite",
            "error": str(e)
        }), 500
    
@reservation_bp.route('/', methods=['GET'])
@token_required
def get_reservations(*args, **kwargs):
    try:
        # Vérification que user_id est présent et valide
        user_id = kwargs.get('user_id')
        if not user_id or not isinstance(user_id, int):
            return jsonify({"success": False, "message": "ID utilisateur invalide ou manquant"}), 400
        
        # Appel au service avec gestion complète des retours
        success, message, data, status = ReservationService.get_order(user_id)

        if not success:
            return jsonify({
                "success": False,
                "message": message,
                "error": data
            }), status

        # Réponse en cas de succès
        return jsonify({
            "success": True,
            "message": message,
            "data": data
        }), status
        
    except Exception as e:
        # Logging de l'erreur
        logging.error(f"Erreur lors de la récupération des réservations: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Une erreur inattendue s'est produite",
            "error": str(e)
        }), 500