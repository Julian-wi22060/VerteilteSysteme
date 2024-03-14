import requests

def query_couchdb(database, selector, fields=None, sort=None, auth=None):
    url = f'{database}/_find'
    headers = {'Content-Type': 'application/json'}
    data = {'selector': selector}
    if fields:
        data['fields'] = fields
    if sort:
        data['sort'] = sort
    response = requests.post(url, json=data, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    return None
