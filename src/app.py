from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import os
import json

app = Flask(__name__)
app.json.sort_keys = False

if os.getenv('PROD') and os.getenv('KUBERNETES'):
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config_docker.json')
elif os.getenv('PROD'):
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), './config_docker.json')
else:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), './../cfg/config.json')


# Laden der Konfigurationsdatei
def load_config():
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
    return config


def get_couchdb_credentials():
    config = load_config()
    couchdb_config = config.get('couchdb', {})
    return couchdb_config.get('username'), couchdb_config.get('password')


def get_couchdb_url_and_database():
    config = load_config()
    couchdb_config = config.get('couchdb', {})
    return couchdb_config.get('url'), couchdb_config.get('database_name')


# Funktion für den Daten-Endpoint
@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    month = int(request.args.get('month')) - 1
    day = request.args.get('day')

    # Erstelle das Mango-Query JSON-Objekt für CouchDB
    headers = {'Content-Type': 'application/json'}
    request_data = {
        "selector": {
            "month": str(month),
            "day": str(day)
        },
        "fields": ["first", "name", "prof", "year", "month", "day"],
        "sort": [{"year": "asc"}]
    }

    try:
        username, password = get_couchdb_credentials()
        url, database_name = get_couchdb_url_and_database()

        response = requests.post(f"{url}/{database_name}/_find", json=request_data, headers=headers,
                                 auth=(username, password), timeout=2)

        data = response.json()

        # Überprüfe, ob die Abfrage einen Treffer ergibt
        if data.get('docs'):
            # Extrahiere die relevanten Daten aus dem JSON
            extracted_data = [
                {'name': doc['first'] + ' ' + doc['name'],
                 'profession': doc['prof'],
                 'born': doc['day'] + '.' + str(int(doc['month']) + 1) + '.' + doc['year']
                 } for doc in data['docs']]
            return jsonify(extracted_data), 200
        else:
            return '', 204
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            return 'Invalid Credentials', 401
        else:
            return 'Internal Server Error', 500
    except requests.Timeout:
        return 'Timeout', 408
    except Exception as e:
        return str(e), 500


# Funktion für den Health-Endpoint
@app.route('/health', methods=['GET'])
def health():
    message = {'Status': 'Healthy - Hooray'}
    return make_response(jsonify(message), 200)


def create_swagger_ui(app):
    SWAGGER_URL = '/swagger'  # URL für den Zugriff auf die Swagger-Oberfläche
    SWAGGER_API = '/static/swagger.yaml'

    # Konfiguration der Swagger-Oberfläche
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        SWAGGER_API,
        config={
            'app_name': "Birthday API"
        }
    )

    # Registrieren Sie die Swagger-Oberfläche in Ihrer Flask-Anwendung
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


create_swagger_ui(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
