from ..extensions import db
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.sql import func


class Reservation(db.Model):
    """Modèle pour la table reservations"""
    
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    confirmationID = Column(String(255), nullable=False)
    id_velo = Column(Integer, ForeignKey('velo.id_velo', ondelete='CASCADE'), nullable=False)
    client_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    create_time = Column(DateTime, default=func.now())
    station_id = Column(BigInteger, ForeignKey('stations.station_id', ondelete='CASCADE'), nullable=True)
    
    def __repr__(self):
        return f"<Reservation {self.id}: {self.confirmationID}>"
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour les réponses API"""
        return {
            'id': self.id,
            'confirmationID': self.confirmationID,
            'id_velo': self.id_velo,
            'client_id': self.client_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'station_id': self.station_id
        }