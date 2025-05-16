from ..extensions import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey
from datetime import datetime


class RechercheVue(db.Model):
    """
    Modèle pour la vue SQL recherches_vue qui joint la table recherches avec stations
    """
    __tablename__ = 'recherches_vue'
    
    # Colonnes de la table recherches
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    recherche = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    resultat = Column(Boolean)
    station_id = Column(BigInteger)
    
    # Colonnes de la table stations
    lat = Column(db.Float)
    lon = Column(db.Float)
    station = Column(String(255))
    
    def __repr__(self):
        return f'<RechercheVue {self.id} par utilisateur {self.client_id}>'
    
    def to_dict(self):
        """
        Convertit l'instance en dictionnaire
        """
        return {
            'id': self.id,
            'client_id': self.client_id,
            'recherche': self.recherche,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resultat': self.resultat,
            'station_id': self.station_id,
            'lat': self.lat,
            'lon': self.lon,
            'station': self.station,
            # Champ calculé pour la compatibilité avec l'ancien code
            'resultat_recherche': self._get_resultat_recherche()
        }
    
    def _get_resultat_recherche(self):
        """
        Détermine le texte du résultat de recherche en fonction des données
        """
        if not self.resultat and self.station_id is None:
            return "Pas de resultat de recherche"
        elif self.resultat and self.station_id is None:
            return "Adresse trouvée"
        else:
            return "Station trouvée"
