"""
Package contenant les modèles de données
"""

# Importer tous les modèles ici pour s'assurer qu'ils sont chargés
# lorsque l'application démarre
from .user_model import User
from .reservation_model import Reservation
from .station_model import Station
from .velo_model import Velo
from .recherche_model import Recherche

# Exporter tous les modèles pour un import plus facile
__all__ = ['User', 'Reservation', 'Station', 'Velo', 'Recherche']