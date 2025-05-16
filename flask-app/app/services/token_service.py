"""
Service de gestion des tokens JWT
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Tuple
from flask import current_app

class TokenService:
    """Service pour gérer les tokens JWT"""
    
    @staticmethod
    def generate_token(user_id: int) -> str:
        """
        Génère un token JWT pour un utilisateur
        """
        # Utilisation de la configuration de l'application
        secret_key = current_app.config['JWT_SECRET_KEY']
        expiration = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expiration),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_token(token: str, user_id: Optional[int] = None) -> Tuple[bool, Optional[dict]]:
        """
        Vérifie la validité d'un token JWT
        
        Args:
            token: Le token JWT à vérifier
            user_id: ID utilisateur à comparer avec celui stocké dans le token (optionnel)
            
        Returns:
            Tuple[bool, Optional[dict]]: (is_valid, payload ou erreur)
        """
        try:
            # Utilisation de la configuration de l'application
            secret_key = current_app.config['JWT_SECRET_KEY']
            
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=['HS256']
            )
            
            # Vérifier si l'ID utilisateur correspond à celui du token
            if user_id is not None and payload.get('user_id') != user_id:
                return False, {'error': 'ID utilisateur ne correspond pas à celui du token'}
                
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {'error': 'Token expiré'}
        except jwt.InvalidTokenError:
            return False, {'error': 'Token invalide'}