Aus diesem Verzeichnis (dort, wo die Dockerfile sich befindet) das Container Image mit diesem Befehl bauen:

```
docker build -t dhbw-couch:1 .
```

Testen mit:

```
docker run -d -p 5984:5984 --name couchdb dhbw-couch:1
```

*Bitte beachten:* Wo immer Sie dieses Container Image verwenden, müssen Sie den Verweis auf meinen Docker Account ("haraldu/") entfernen! 

Unbedingt testen, ob der Build erfolgreich war, d.h wenn das neue Image gestartet ist, eine Abfrage durchführen:

```
curl -d  '{"selector": {"month": "5", "day": "23"}, "fields": ["first","name","prof","year","month","day"], "sort": [{"year":"asc"}]}' -H "Content-Type: application/json" -X POST 'http://localhost:5984/birthday_db/_find' -u 'admin:student'
```

Ergebnis:

```
{"docs":[
{"first":"Vinton Gray","name":"Cerf","prof":"Computer Scientist","year":"1943","month":"5","day":"23"}
],
"bookmark": "g2wAAAACaAJkAA5zdGFydGtleV9kb2NpZG0AAAAgMTc1NDVhMThmODkwZmZkYmVmODNhZjFiYjcwMDNkMTBoAmQACHN0YXJ0a2V5bAAAAAFtAAAABDE5NDNqag",
"warning": "The number of documents examined is high in proportion to the number of results returned. Consider adding a more specific index to improve this."}
```



