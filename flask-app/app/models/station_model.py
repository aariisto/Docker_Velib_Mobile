from ..extensions import db
from sqlalchemy import Column, BigInteger, String, Float


class Station(db.Model):
    """Modèle pour la table stations"""
    
    __tablename__ = 'stations'
    
    station_id = Column(BigInteger, primary_key=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    station = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Station {self.station_id}: {self.station}>"
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour les réponses API"""
        return {
            'station_id': self.station_id,
            'lat': self.lat,
            'lon': self.lon,
            'station': self.station
        }