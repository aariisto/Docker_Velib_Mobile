from datetime import datetime
from app.extensions import db


class Recherche(db.Model):
    """
    Modèle pour stocker les recherches effectuées par les utilisateurs
    """
    __tablename__ = 'recherches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recherche = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    resultat = db.Column(db.Boolean)  # TINYINT(1) est équivalent à BOOLEAN dans SQLAlchemy
    station_id = db.Column(db.BigInteger, db.ForeignKey('stations.station_id', ondelete='CASCADE'))

    # Relations avec les autres modèles
    user = db.relationship('User', backref=db.backref('recherches', lazy=True))
    station = db.relationship('Station', backref=db.backref('recherches', lazy=True))

    def __repr__(self):
        return f'<Recherche {self.id} par utilisateur {self.client_id}>'
    
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
            'station_id': self.station_id
        }