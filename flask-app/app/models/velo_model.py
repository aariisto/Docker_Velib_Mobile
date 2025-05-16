from ..extensions import db
from sqlalchemy import Column, Integer, String


class Velo(db.Model):
    """Modèle pour la table velo"""
    
    __tablename__ = 'velo'
    
    id_velo = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<Velo {self.id_velo}: {self.type}>"
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour les réponses API"""
        return {
            'id_velo': self.id_velo,
            'type': self.type
        }