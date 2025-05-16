from sqlalchemy.exc import SQLAlchemyError
from typing import Tuple, Dict, Any
from ..extensions import db
from ..models.recherche_model import Recherche
from ..models.station_model import Station
from ..models.recherche_vue_model import RechercheVue  # Assuming RechercheVue is defined in recherche_vue_model
import re
import requests
from typing import Optional
import os


class SearchService:
    """Service pour gérer les opérations liées aux recherches"""
    
    @staticmethod
    def delete_search(id_search: int, user_id: int) -> Tuple[bool, str, Dict[str, Any], int]:
        """
        Supprime une recherche par son ID
        
        Args:
            id_search (int): Identifiant de la recherche à supprimer
            user_id (int): Identifiant de l'utilisateur qui fait la demande (obligatoire)
            
        Returns:
            tuple: (success, message, response_data, status_code)
        """
        try:
            # Vérifier la propriété de la recherche en utilisant le modèle ORM
            search_to_delete = Recherche.query.filter_by(id=id_search, client_id=user_id).first()
            
            if not search_to_delete:
                return False, "Vous n'êtes pas autorisé à supprimer cette recherche", {
                    'error': 'Recherche non trouvée ou accès non autorisé',
                    'error_code': 'ACCESS_DENIED',
                    'token': True
                }, 403

            # Supprimer la recherche en utilisant le modèle ORM
            db.session.delete(search_to_delete)
            db.session.commit()
            
            return True, f"Recherche {id_search} supprimée avec succès", {}, 200
            
        except SQLAlchemyError as e:
            # Annuler la transaction en cas d'erreur
            db.session.rollback()
            return False, f"Erreur lors de la suppression de la recherche: {str(e)}", {
                'error': str(e),
                'error_code': 'DATABASE_ERROR',
                'token': False
            }, 500
        except Exception as e:
            db.session.rollback()
            return False, f"Erreur inattendue: {str(e)}", {
                'error': str(e),
                'error_code': 'UNKNOWN_ERROR',
                'token': False
            }, 500

    @staticmethod
    def save_search(user_id: int, search_term: str, station_id: Optional[int], result: int) -> Tuple[bool, str, Dict[str, Any], int]:
        """
        Enregistre une recherche dans la base de données
        
        Args:
            user_id (int): ID de l'utilisateur
            search_term (str): Terme de recherche
            station_id (Optional[int]): ID de la station trouvée
            result (int): Résultat de la recherche (1 = trouvé, 0 = non trouvé)
            
        Returns:
            tuple: (success, message, response_data, status_code)
        """
        try:
            # Nettoyer la recherche
            search_term = re.sub(r'\s+', ' ', search_term.strip())
            
            # Créer une nouvelle instance du modèle Recherche
            new_search = Recherche(
                client_id=user_id,
                recherche=search_term,
                station_id=station_id,
                resultat=bool(result)  # Convertir l'entier en booléen pour le champ resultat
            )
            
            # Ajouter l'objet à la session et effectuer le commit
            db.session.add(new_search)
            db.session.commit()
            
            return True, "Recherche enregistrée avec succès", {}, 200
                
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Erreur lors de l'enregistrement de la recherche: {str(e)}", {
                'error': str(e),
                'error_code': 'DATABASE_ERROR',
                'token': False
            }, 500
            
        except Exception as e:
            db.session.rollback()
            return False, f"Erreur inattendue: {str(e)}", {
                'error': str(e),
                'error_code': 'UNKNOWN_ERROR',
                'token': False
            }, 500

    @staticmethod
    def search_station(search_term: str) -> Tuple[bool, str, Dict[str, Any], int]:
        """
        Recherche une station via l'API Velib, puis Google Maps si non trouvée
        
        Args:
            search_term (str): Terme de recherche
            
        Returns:
            tuple: (success, message, response_data, status_code)
        """
        try:
            # Nettoyer la recherche
            search_term = re.sub(r'\s+', ' ', search_term.strip())
            
            # 1. Recherche dans l'API Velib
            url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
            response = requests.get(url)
            
            if not response.ok:
                return False, "Erreur lors de l'appel à l'API Velib", {
                    'error': "Le serveur n'a pas pu traiter votre demande",
                    'error_code': 'API_ERROR',
                    'token': False
                }, 500
                
            data = response.json()
            stations = data.get("data", {}).get("stations", [])
            
            # Rechercher la station dans Velib
            matched_station = None
            for station in stations:
                if search_term.lower() in station.get("name", "").lower():
                    matched_station = station
                    break
            
            if matched_station:
                return True, "Station trouvée!", {
                    'lat': matched_station.get("lat"),
                    'lon': matched_station.get("lon"),
                    'station_id': matched_station.get("station_id"),
                    'message': "Station trouvée!",
                    'should_save': True
                }, 200
            
            # 2. Si pas trouvé dans Vélib, chercher dans Nominatim
            nominatim_url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(search_term)}&format=json&limit=1"

            try:
                nominatim_response = requests.get(nominatim_url, headers={'User-Agent': 'VelibSearchApp/1.0'})

                if nominatim_response.ok:
                    nominatim_data = nominatim_response.json()
                    if nominatim_data:
                        location = nominatim_data[0]
                        lat = location.get("lat")
                        lon = location.get("lon")

                        if lat and lon:
                            return True, "Localisation trouvée!", {
                                'lat': lat,
                                'lon': lon,
                                'station_id': None,
                                'message': "Localisation trouvée via Nominatim",
                                'should_save': True
                            }, 200

            except Exception as e:
                print(f"Erreur lors de la requête Nominatim : {e}")
                return False, "Erreur de recherche externe", {
                    'lat': None,
                    'lon': None,
                    'station_id': None,
                    'message': "Erreur interne ou réseau avec Nominatim",
                    'should_save': False
                }, 500            

            # 3. Si rien n'est trouvé
            return True, "Aucune station ni adresse n'a été trouvée", {
                'lat': None,
                'lon': None,
                'station_id': None,
                'message': "Aucune station ni adresse n'a été trouvée",
                'should_save': False
            }, 201
            
        except Exception as e:
            return False, f"Erreur inattendue: {str(e)}", {
                'error': str(e),
                'error_code': 'UNKNOWN_ERROR',
                'token': False
            }, 500
        
    @staticmethod
    def get_searches_by_user(user_id: int) -> Tuple[bool, str, Any, int]:
        """
        Récupère toutes les recherches d'un utilisateur donné

        Args:
            user_id (int): ID de l'utilisateur

        Returns:
            tuple: (success, message, data, status_code)
        """
        try:
            # Utilisation du modèle ORM pour récupérer les recherches
            # Note: Comme la vue 'recherches_vue' était utilisée auparavant, nous devons joindre
            # les tables nécessaires pour obtenir les mêmes informations
            searches = RechercheVue.query.filter_by(client_id=user_id).order_by(RechercheVue.created_at.desc()).all()
            
            data = []
            for search in searches:
                search_item = search.to_dict()
                
                # Déterminer la valeur de resultat_recherche en fonction de resultat et station_id
                if not search_item.get('resultat') and search_item.get('station_id') is None:
                    search_item['resultat_recherche'] = "Pas de resultat de recherche"
                elif search_item.get('resultat') and search_item.get('station_id') is None:
                    search_item['resultat_recherche'] = "Adresse trouvée"
                else:
                    search_item['resultat_recherche'] = "Station trouvée"
                    
                data.append(search_item)
            
            return True, "Recherches récupérées avec succès", data, 200

        except SQLAlchemyError as e:
            print(f"[ERROR] SQLAlchemy: {str(e)}")
            return False, "Erreur base de données", {'error': str(e)}, 500

        except Exception as e:
            print(f"[ERROR] Exception: {str(e)}")
            return False, "Erreur inconnue", {'error': str(e)}, 500

