"""
Service d'authentification pour gérer l'inscription et la connexion des utilisateurs
"""
import bcrypt
from sqlalchemy.exc import IntegrityError
from typing import Tuple, Optional, Dict, Any
from ..models.user_model import User
from ..extensions import db
from .token_service import TokenService

class AuthService:
    """
    Service gérant l'authentification des utilisateurs
    """
    
    @staticmethod
    def register(username: str, email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str, int]:
        """
        Enregistre un nouvel utilisateur dans la base de données.
        
        Args:
            username (str): Nom d'utilisateur
            email (str): Adresse email
            password (str): Mot de passe en clair
            
        Returns:
            tuple: (user_dict, message, status_code)
        """
        try:
            # Vérifier si l'email existe déjà
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return None, "Un utilisateur avec cet email existe déjà", 409
            
            # Hasher le mot de passe
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Créer le nouvel utilisateur
            new_user = User(
                username=username,
                email=email,
                password=hashed_password.decode('utf-8')  # Stocker le hash en string
            )
            
            # Enregistrer dans la base de données
            db.session.add(new_user)
            db.session.commit()
            
            # Préparer les données de réponse
            user_data = {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email
            }
            
            return user_data, "Compte créé avec succès", 201
            
        except IntegrityError:
            db.session.rollback()
            return None, "Une erreur est survenue lors de l'inscription", 500
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur inattendue: {str(e)}", 500
    
    @staticmethod
    def login(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str, int]:
        """
        Authentifie un utilisateur.
        
        Args:
            email (str): Adresse email
            password (str): Mot de passe en clair
            
        Returns:
            tuple: (user_dict, message, status_code)
        """
        try:
            # Chercher l'utilisateur par email
            user = User.query.filter_by(email=email).first()
            
            # Vérifier si l'utilisateur existe
            if not user:
                return None, "Email ou mot de passe incorrect", 401
            
            # Vérifier le mot de passe
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return None, "Email ou mot de passe incorrect", 401
            
            # Générer le token
            token = TokenService.generate_token(user.id)
            
            # Préparer les données de réponse
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token
            }
            
            return user_data, "Connexion réussie", 200
                
        except Exception as e:
            return None, f"Erreur lors de la connexion: {str(e)}", 500 