from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Funktion für den Daten-Endpoint
@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    # Extrahiere die Monats- und Tagesparameter aus der URL-Anfrage
    month = request.args.get('month')
    day = request.args.get('day')

    # Erstelle das Mango-Query JSON-Objekt für CouchDB
    mango_query = {
        "selector": {"month": str(int(month) - 1), "day": day},
        "fields": ["name", "profession", "year", "month", "day"],
        "sort": [{"year": "asc"}]
    }

    # Führe die Mango-Query durch
    try:
        response = requests.post('http://admin:student@localhost:5984/birthday_db/_find', json=mango_query, timeout=2)
        data = response.json()
        
        # Überprüfe, ob die Abfrage einen Treffer ergibt
        if data.get('docs'):
            return jsonify(data['docs']), 200
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
    return 'Healthy', 200

if __name__ == '__main__':
    app.run(debug=True)
