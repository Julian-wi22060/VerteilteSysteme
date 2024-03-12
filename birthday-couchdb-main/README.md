# Birthday CouchDB

Container Image mit vorkonfigurierter CouchDB mit Birthday DB.

Teil der Portfolioprüfung Verteilte Systeme.

Bau eines eigenen Container Image (z.B. für macOS/ARM) ist [hier](https://git.dhbw-stuttgart.de/harald.uebele/birthday-couchdb/-/tree/main/ContainerImage) beschrieben.

## Start als Docker Container

```
docker run -d -p 5984:5984 --name couchdb haraldu/dhbw-couch:1
```

Das Image liegt in meinem Docker Hub Repository und wird durch diesen Befehl herunter geladen und gestartet.

Zugriff auf die CouchDB GUI Fauxton über die URL:

[http://localhost:5984/_utils](http://localhost:5984/_utils)

(User: admin, Password: student)

## Mango Query mit Monat und Tag

* Die Basis-URL der CouchDB als Container für die lokale Verwendung ist: http://localhost:5984
* Datenbankzugriff ist durch Basic Authentication abgesichert (User: admin, Passwort: student). 
   

Abfrage der birthday_db als cURL-Beispiel:

```
curl -d  '{"selector": {"month": "5", "day": "23"}, "fields": ["first","name","prof","year","month","day"], "sort": [{"year":"asc"}]}' -H "Content-Type: application/json" -X POST 'http://localhost:5984/birthday_db/_find' -u 'admin:student'
```

Erklärung des Befehls:

1. Es wird per HTTP POST ein "Mango"-Query an die URL http://localhost:5984/birthday_db/_find gesendet. Basic Authentication mit *-u 'admin:student'*.

2. Das Query selbst wird als JSON-Objekt (-H "Content-Type: application/json") übergeben (-d):

```
	{
		"selector": {"month": "5", "day": "23"},
		"fields": ["first","name","prof","year","month","day"],
		"sort": [{"year":"asc"}]
	}
```

* "selector" enthält das eigentliche Query, month=5 UND day=23, das wäre also der 23. Juni (5 = Juni!)
* "fields" enthält die "Spalten", die ausgegeben werden (alle relevanten Daten)
* "sort" sortiert die Liste aufsteigend nach dem Geburtsjahr

Ergebnis:

```
{
  "docs": [
    {
      "first": "Vinton Gray",
      "name": "Cerf",
      "prof": "Computer Scientist",
      "year": "1943",
      "month": "5",
      "day": "23"
    }
  ],
  "bookmark": "g2wAAAACaAJkAA5zdGFydGtleV9kb2NpZG0AAA...",
  "warning": "The number of documents examined is high in... ."
}
```
Der relevante Teil ist die Liste "docs". Für diesen Tag gibt es einen Eintrag.

"bookmark" ist nur für CouchDB selbst relevant, "warning" kann in unserem Fall getrost ignoriert werden.

Gibt es für einen Tag gar keine Einträge, z.B. für den 29. Dezember, ist die Liste "docs" einfach leer:

```
{
 "docs": [],
  "bookmark": "nil",
  "warning": …
}
```

## Kubernetes Deployment

Deployment in laufendes Minikube mit diesen Befehlen:

```
kubectl apply -f deployment/deployment.yaml 
kubectl apply -f deployment/service.yaml
```

Basis-URL der Couchdb ist dann

```
http://couchdb:5984
```

bei Zugriff innerhalb des Kubernetes Clusters.

Für den Zugriff von außerhalb die BASIS-URL mit `minikube service list` ermitteln.
