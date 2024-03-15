from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import requests
from urllib.parse import urljoin
import os

app = Flask(__name__)

'''
# Laden der Konfigurationsdatei
config_path = os.path.join(os.path.dirname(__file__), '..', 'cfg', 'config.cfg')
app.config.from_pyfile(config_path)
'''

# Port-Forwarding des CouchDB-Containers
app.config['DB_NAME'] = 'http://localhost:5984/birthday_db'

# Funktion für den Daten-Endpoint
@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    month = request.args.get('month')
    day = request.args.get('day')

    # Erstelle das Mango-Query JSON-Objekt für CouchDB
    mango_query = {
        "selector": {"month": str(int(month) - 1), "day": day},
        "fields": ["name", "prof", "year", "month", "day"],
        "sort": [{"year": "asc"}]
    }

    # Konstruieren Sie die URL zur CouchDB unter Verwendung der Konfiguration aus der dev.cfg-Datei
    db_url = urljoin(app.config['DB_NAME'], '_find')

    try:
        response = requests.post(db_url, json=mango_query, timeout=2)
        data = response.json()

        # Überprüfe, ob die Abfrage einen Treffer ergibt
        if data.get('docs'):
            # Extrahiere die relevanten Daten aus dem JSON
            extracted_data = [{'name': doc['name'], 'profession': doc['prof'], 'year': doc['year'], 'month': doc['month'], 'day': doc['day']} for doc in data['docs']]
            return jsonify(extracted_data), 200
        else:
            return '', 204
    except requests.Timeout:
        return 'Timeout', 500
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            return 'Invalid Credentials', 401
        else:
            return 'Internal Server Error', 500
    except Exception as e:
        return str(e), 500

# Funktion für den Health-Endpoint
@app.route('/health', methods=['GET'])
def health():
    try:
        response = requests.get('http://localhost:5984/_up', timeout=2)
        if response.status_code == 200:
            return 'Healthy - Hooray', 200
        else:
            return 'CouchDB Health Check Failed', 500
    except requests.Timeout:
        return 'Timeout', 500
    except Exception as e:
        return str(e), 500

def create_swagger_ui(app):
    SWAGGER_URL = '/swagger'  # URL für den Zugriff auf die Swagger-Oberfläche
    API_URL = '/static/swagger.yaml'   # URL zur API-Konfiguration

    # Konfiguration der Swagger-Oberfläche
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,   # Swagger URL
        API_URL,       # URL zur API-Konfiguration
        config={       # Optionale Konfigurationseinstellungen
            'app_name': "Birthday API"
        }
    )

    # Registrieren Sie die Swagger-Oberfläche in Ihrer Flask-Anwendung
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

create_swagger_ui(app)

if __name__ == '__main__':
    app.run(port=8000, debug=True)