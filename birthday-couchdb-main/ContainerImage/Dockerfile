FROM couchdb:latest
COPY ./data/ /opt/couchdb/data
COPY ./config/ /opt/couchdb/etc/local.d

# docker build -t dhbw-couch:1 .
# docker run -d -p 5984:5984 --name couchdb dhbw-couch:1
# curl -d  '{"selector": {"month": "5", "day": "23"}, "fields": ["first","name","prof","year","month","day"], "sort": [{"year":"asc"}]}' -H "Content-Type: application/json" -X POST 'http://localhost:5984/birthday_db/_find' -u 'admin:student'