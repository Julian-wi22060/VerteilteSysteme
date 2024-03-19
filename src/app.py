from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import os
import json

# Initialize Flask application
app = Flask(__name__)
app.json.sort_keys = False

# Determine configuration file based on environment variables
if os.getenv('DOCKER') and os.getenv('KUBERNETES'):
    print("Running in Kubernetes")
    print(os.getcwd())
    print(os.listdir(os.getcwd()))
    print(os.listdir(os.getcwd() + "/cfg"))
    CONFIG_FILE = 'config_k8s.json'
    '''After countless unsuccessful attempts to mount the config_docker.json in a /cfg directory when using 
    Kubernetes, there is unfortunately no other option but to transfer the config_docker.json to the root directory 
    for the use in Kubernetes... (see empty dir in log output in the Kubernetes pod of the microservice)
    '''
elif os.getenv('DOCKER'):
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), './config_docker.json')
else:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), './../cfg/config.json')


# Load configuration from file
def load_config():
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
    return config


# Get CouchDB credentials from configuration
def get_couchdb_credentials():
    config = load_config()
    couchdb_config = config.get('couchdb', {})
    return couchdb_config.get('username'), couchdb_config.get('password')


# Get CouchDB URL and database name from configuration
def get_couchdb_url_and_database():
    config = load_config()
    couchdb_config = config.get('couchdb', {})
    return couchdb_config.get('url'), couchdb_config.get('database_name')


# Data endpoint function
@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    month = int(request.args.get('month')) - 1
    day = request.args.get('day')

    # Create Mango Query JSON object for CouchDB
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
        # Get CouchDB credentials and URL from configuration
        username, password = get_couchdb_credentials()
        url, database_name = get_couchdb_url_and_database()

        # Make POST request to CouchDB to query data
        response = requests.post(f"{url}/{database_name}/_find", json=request_data, headers=headers,
                                 auth=(username, password), timeout=2)

        # Parse JSON response
        data = response.json()

        # Check if query returns any result
        if data.get('docs'):
            # Extract relevant data from JSON response
            extracted_data = [
                {'name': doc['first'] + ' ' + doc['name'],
                 'profession': doc['prof'],
                 'born': doc['day'] + '.' + str(int(doc['month']) + 1) + '.' + doc['year']
                 } for doc in data['docs']]

            # Return extracted data with status code 200 (OK)
            return jsonify(extracted_data), 200
        else:
            # If no data found, return empty response with status code 204 (No Content)
            return '', 204

    # Handle specific exceptions
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            # If unauthorized, return error message with status code 401 (Unauthorized)
            return 'Invalid Credentials', 401
        else:
            # If other HTTP error, return error message with status code 500 (Internal Server Error)
            return 'Internal Server Error', 500
    except requests.Timeout:
        # If timeout occurs, return error message with status code 408 (Timeout)
        return 'Timeout', 408
    except Exception as e:
        # If any other exception occurs, return error message with status code 500 (Internal Server Error)
        return str(e), 500


# Health endpoint function
@app.route('/health', methods=['GET'])
def health():
    message = {'Status': 'Healthy - Hooray'}
    return make_response(jsonify(message), 200)


# Function to create Swagger UI
def create_swagger_ui(app):
    SWAGGER_URL = '/swagger'  # URL to access Swagger UI
    SWAGGER_API = '/static/swagger.yaml'

    # Configure Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        SWAGGER_API,
        config={
            'app_name': "Birthday API"
        }
    )

    # Register Swagger UI in Flask application
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Call function to create Swagger UI
create_swagger_ui(app)

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
