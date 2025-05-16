from sqlalchemy.exc import SQLAlchemyError
from typing import Tuple, Any, List, Dict
from ..extensions import db
import logging
from ..models.reservation_model import Reservation
from ..models.user_model import User
from ..models.velo_model import Velo
from ..models.station_model import Station
from ..models.reservation_vue_model import ReservationVue

class ReservationService:
    """Service pour gérer les réservations"""

    @staticmethod
    def get_order(client_id: int) -> Tuple[bool, str, List[Dict[str, Any]], int]:
        """
        Récupère les réservations d'un client avec toutes les informations associées (station, velo)

        Args:
            client_id (int): ID du client

        Returns:
            Tuple[bool, str, List[Dict[str, Any]], int]: (succès, message, données, code_statut)
        """
        try:
            # Validation de l'ID client
            if not client_id or not isinstance(client_id, int):
                return False, "ID client invalide", {"error": "L'ID client doit être un entier valide"}, 400
                
            # Utilisation du modèle ORM de la vue pour récupérer les réservations avec les détails complets
            reservations = ReservationVue.query.filter_by(client_id=client_id).order_by(ReservationVue.create_time.desc()).all()
            
            # Conversion en dictionnaire
            reservations_list = [reservation.to_dict() for reservation in reservations]
            
            message = "Réservations récupérées avec succès"
            if not reservations_list:
                message = "Aucune réservation trouvée pour cet utilisateur"
                
            # Retour standardisé avec message
            return True, message, reservations_list, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Erreur SQL lors de la récupération des réservations : {str(e)}"
            logging.error(error_msg)
            return False, "Erreur de base de données", {"error": str(e)}, 500

        except Exception as e:
            db.session.rollback()
            error_msg = f"Erreur inattendue lors de la récupération des réservations : {str(e)}"
            logging.error(error_msg)
            return False, "Erreur inattendue", {"error": str(e)}, 500

    @staticmethod
    def create_reservation(reservation_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any], int]:
        """
        Crée une nouvelle réservation

        Args:
            reservation_data (Dict[str, Any]): Données de la réservation
                {
                  "confirmationID": str,
                  "id_velo": int,
                  "station_id": int,
                  "client_id": int
                }

        Returns:
            Tuple[bool, str, Dict[str, Any]], int]: (succès, message, données, code_statut)
        """
        try:
            # Validation des données
            required_fields = ['confirmationID', 'id_velo', 'client_id', 'station_id']
            for field in required_fields:
                if field not in reservation_data:
                    return False, f"Le champ '{field}' est obligatoire", {"error": "Données incomplètes"}, 400
            
            # Création de la réservation
            new_reservation = Reservation(
                confirmationID=reservation_data['confirmationID'],
                id_velo=reservation_data['id_velo'],
                client_id=reservation_data['client_id'],
                station_id=reservation_data['station_id']
            )
            
            # Enregistrement de la réservation
            db.session.add(new_reservation)
            db.session.commit()
            
            return True, "Réservation créée avec succès", new_reservation.to_dict(), 201
            
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Erreur SQL lors de la création de la réservation : {str(e)}"
            logging.error(error_msg)
            return False, "Erreur de base de données", {"error": str(e)}, 500
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Erreur inattendue lors de la création de la réservation : {str(e)}"
            logging.error(error_msg)
            return False, "Erreur inattendue", {"error": str(e)}, 500
