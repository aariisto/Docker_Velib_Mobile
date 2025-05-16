from ..extensions import db
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.sql import func


class ReservationVue(db.Model):
    """Modèle pour la vue reservations_vue qui joint les tables reservations, stations et velo"""
    
    __tablename__ = 'reservations_vue'
    
    # Colonnes de la table reservations
    id = Column(Integer, primary_key=True)
    confirmationID = Column(String(255), nullable=False)
    id_velo = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    create_time = Column(DateTime)
    station_id = Column(BigInteger)
    
    # Colonnes de la table stations
    lat = Column(db.Float)
    lon = Column(db.Float)
    station = Column(String(255))
    
    # Colonnes de la table velo
    type = Column(String(50))
    
    def __repr__(self):
        return f"<ReservationVue {self.id}: {self.confirmationID} - {self.station}>"
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour les réponses API"""
        return {
            'id': self.id,
            'confirmationID': self.confirmationID,
            'id_velo': self.id_velo,
            'client_id': self.client_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'station_id': self.station_id,
            'lat': self.lat,
            'lon': self.lon,
            'station': self.station,
            'type_velo': self.type
        }
