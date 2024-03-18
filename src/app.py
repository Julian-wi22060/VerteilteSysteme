from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import os

app = Flask(__name__)
app.json.sort_keys = False


def config_path():
    if os.environ.get('IS_PROD') is not None:
        print(f'Running in production/docker mode: {os.environ.get("IS_PROD")}')
        return 'config_docker.cfg'

    elif os.getenv('KUBERNETES'):
        configfile = os.path.join(os.path.dirname(_file), 'config_micro.json')
        print(f'Running in kubernetes mode: {os.environ.get("KUBERNETES")}')
        return '../kubernetes/deployment.yaml'

    print('Running in development mode: True')
    return '../cfg/config.cfg'


# Laden der Konfigurationsdatei
config_path = config_path()
app.config.from_pyfile(config_path)

# Port-Forwarding des CouchDB-Containers
app.config['DB_NAME'] = 'http://localhost:5984/birthday_db'


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
    auth = (app.config['COUCHDB_USER'], app.config['COUCHDB_PASSWORD'])

    db_url = app.config['DB_URL'] + '/_find'

    try:
        response = requests.post(db_url, json=request_data, headers=headers, auth=auth, timeout=2)
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
