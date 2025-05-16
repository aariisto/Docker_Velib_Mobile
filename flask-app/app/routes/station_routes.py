from flask import Blueprint, jsonify, request
import requests

station_bp = Blueprint('station', __name__)

@station_bp.route('/stations', methods=['GET'])
def get_stations():
    # Effectuer une requête GET pour obtenir les informations des stations
    response = requests.get("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json")
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Convertir la réponse JSON en dictionnaire Python
        data = response.json()
        formatted_data = []

        # Filtrer et structurer les données des stations
        for station in data.get('data', {}).get('stations', []):
            # Ajouter la station avec les champs formatés dans la liste finale
            formatted_station = {
                "station_id": station.get('station_id'),
                "stationCode": station.get('stationCode'),
                "name": station.get('name'),
                "lat": station.get('lat'),
                "lon": station.get('lon'),
                "capacity": station.get('capacity')
            }
            formatted_data.append(formatted_station)

        # Retourner les données formatées en JSON
        return jsonify(formatted_data)
    else:
        # Retourner une erreur si la requête a échoué
        return jsonify({"error": f"Erreur lors de la requête: {response.status_code}"}), response.status_code

@station_bp.route('/stations/<int:station_id>', methods=['GET'])
def get_station_info(station_id):
    # Effectuer une requête GET pour obtenir les informations de statut des stations
    response = requests.get("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json")
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Convertir la réponse JSON en dictionnaire Python
        data = response.json()
        
        # Trouver la station avec le station_id donné
        station_info = next((station for station in data['data']['stations'] if station['station_id'] == station_id), None)
        
        # Si la station est trouvée, retourner ses informations
        if station_info:
            return jsonify(station_info)
        else:
            # Retourner une réponse vide si la station n'est pas trouvée
            return jsonify(None)
    else:
        # Retourner une erreur si la requête a échoué
        return jsonify({"error": f"Erreur lors de la requête: {response.status_code}"}), response.status_code