import requests

# Daten-Endpoint
url_data = 'http://127.0.0.1:5000/api/v1/get_data?month=2&day=21'
response_data = requests.get(url_data)
print(response_data.status_code)
print(response_data.json())

# Health-Endpoint
url_health = 'http://127.0.0.1:5000/health'
response_health = requests.get(url_health)
print(response_health.status_code)
print(response_health.json())