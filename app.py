import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Konfiguration
COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984')
COUCHDB_DB_NAME = os.environ.get('COUCHDB_DB_NAME', 'birthday_db')


# REST API-Endpoint für Datenabfrage
@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    try:
        # Extrahiere Monat und Tag aus den Query-Parametern
        month = int(request.args.get('month'))
        day = int(request.args.get('day'))

        # Erzeuge Mango Query für CouchDB
        mango_query = {
            "selector": {
                "month": month - 1,  # CouchDB verwendet 0-basierte Monate
                "day": day
            }
        }

        # Sende POST Request an CouchDB _find Endpoint
        response = requests.post(f'{COUCHDB_URL}/{COUCHDB_DB_NAME}/_find', json=mango_query)

        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # JSON-Daten aus der CouchDB-Antwort extrahieren
            data = response.json().get('docs', [])

            if data:
                # Wenn Treffer vorhanden sind
                return jsonify(data), 200
            else:
                # Wenn keine Treffer gefunden wurden
                return jsonify({'message': 'Keine Daten gefunden.'}), 404

        else:
            # Bei einem Fehler in der Anfrage
            return jsonify({'error': f'Fehler beim Zugriff auf die CouchDB: {response.status_code}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Health Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8001)
