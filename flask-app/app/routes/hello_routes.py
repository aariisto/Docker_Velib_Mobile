"""
Route simple pour tester l'API
"""
from flask import Blueprint, jsonify

# Créer un blueprint pour la route de test
hello_bp = Blueprint('hello', __name__)

@hello_bp.route('/', methods=['GET'])
def hello():
    """
    Endpoint simple pour tester que l'API fonctionne
    """
    return jsonify({
        'message': 'Hello World!',
        'status': 'API fonctionne correctement'
    }) 