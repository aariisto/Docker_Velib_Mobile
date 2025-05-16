"""
Modèle pour les utilisateurs.
"""
from datetime import datetime
from ..extensions import db

class User(db.Model):
    """
    Modèle représentant un utilisateur dans la base de données.
    Correspond à la table 'users'.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """Représentation de l'objet pour le debugging"""
        return f'<User {self.username} ({self.email})>'
        
    def to_dict(self):
        """Convertit l'objet User en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 