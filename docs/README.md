# Abgabe Verteilte Systeme 3706017
## Struktur des Projektordners VerteilteSysteme
    |birthday-couchdb-main → Dateien unverändert seit Bereitstellung
    |cfg
    |    |config.cfg
    |    |config_docker.cfg
    |docs
    |    |README.md
    |imgs
    |    |swagger_1.png
    |    |swagger_2.png
    |    |swagger_3.png
    |    |swagger_4.png
    |    |swagger_5.png
    |kubernetes
    |    |deployment.yaml
    |    |microservice_deployment.yaml
    |    |microservice_service.yaml
    |    |service.yaml
    |src
    |    |static
    |    |    |swagger.yaml
    |    |.dockerignore
    |    |app.py
    |    |Dockerfile
    |docker_compose.yml
    |requirements.txt

## Beschreibung

Nachfolgend stehen alle Informationen, um die Birthday-Datenbank und den dazugehörigen Microservice lokal, in Docker-Containern und in einem Kubernetes-Cluster zu starten.

### API-Dokumentation
Im lokalen Betrieb und im Betrieb mit Docker ist die API-Dokumentation unter dem Pfad http://localhost:4000/swagger/ zu finden. Im Kubernetes Betrieb unter http://localhost:"port"/swagger/

### Lokaler Betrieb
1. Im Verzeichnis "/birthday-couchdb-main/ContainerImage/" wird die Geburtstags-Datenbank von Docker bereitgestellt mit:<br>
`docker build -t dhbw-couch:1 .`<br><br>
2. Die Geburtstags-Datenbank wird in einem Docker-Container gestartet mit:<br>
`docker run -d -p 5984:5984 --name couchdb dhbw-couch:1`<br><br>
3. Der Microservice wird im Verzeichnis "/src/" gestartet mit:<br>
`python3 app.py`<br><br>
4. Der Microservice kann beispielsweise mit 'curl' getestet werden:<br>
`curl -d '{"selector": {"month": "5", "day":"23"}, "fields":["first","name","prof","year","month","day"], "sort": [{"year":"asc"}]}' -H "Content-Type: application/json" -X POST 'http://localhost:5984/birthday_db/_find' -u 'admin:student'`<br><br>

### Docker-Betrieb
1. Im Hauptverzeichnis "/verteilteSysteme/" werden die Container simultan bereitgestellt mit:<br>
```docker-compose build```<br><br>
2. Die Container werden ausgeführt über:<br>
`docker-compose up`<br><br>
3. Das Deployment kann beispielsweise mit 'curl' getestet werden:<br>
`curl -d '{"selector": {"month": "5", "day":"23"}, "fields":["first","name","prof","year","month","day"], "sort": [{"year":"asc"}]}' -H "Content-Type: application/json" -X POST 'http://localhost:5984/birthday_db/_find' -u 'admin:student'`<br><br>

**_Achtung:_** Bevor der Befehl docker-compose build verwendet werden darf, muss ein Image der Datenbank selbst bereits vorhanden sein, auf das dann von docker-compose.yaml zugegriffen wird.

### Kubernetes-Betrieb

#### Kubernetes initialisieren<br>
Erstellt den Docker Container zur Verwendung im Kubernetes Cluster.<br>
1. `minikube start`<br><br>
Startet den Minikube Cluster.<br>
2. `eval $(minikube docker-env) `<br><br>
Lädt das Docker Image in das Minikube-Cluster.<br>
3. `minikube image build -t julian-microservice:latest . -f src/Dockerfile`<br><br>
--> Wenn der Fehler: Unable to resolve the current Docker CLI context "default" auftritt:<br>
--> Setzt den Docker Kontext auf "default".<br>
--> `cd kubernetes`<br><br>
4. `kubectl create -f configMap.yaml`
5. `kubectl apply -f deployment.yaml`
6. `kubectl apply -f service.yaml`
7. `kubectl get pods` --> BILD EINFÜGEN
8. `kubectl port-forward PODNAME 4000:4000`
9. `minikube dashboard`
10. `localhost:4000/swagger`

Danach Schritt 3 wiederholen.<br><br>

---> Falls Schritt 3 bis 4 nicht funktioniert hat:<br>
---> Erstellt den Docker Container zur Verwendung im Kubernetes Cluster.<br>
--->`minikube image build -t micronetes -f ./Dockerfile .`<br><br>

Erstellt den Service für den Kubernetes Cluster.<br>
4. `kubectl apply -f kubernetes/service.yaml`<br><br>

Erstellt den Service für die CouchDB im Kubernetes Cluster.<br>
5. `kubectl apply -f kubernetes/couch_service.yaml`<br><br>

Erstellt die ConfigMap für den Kubernetes Cluster.<br>
6. `kubectl create configmap prod-config --from-file=config/kub_prod.yaml`<br><br>

#### Deploying to Kubernetes
Startet den Kubernetes Pod mit dem Service und der Datenbank.<br>
1. `kubectl apply -f kubernetes/kubernetes.yaml`<br><br>
Öffnet den Service im "default" Browser.<br>
2. `minikube service micronetes`<br><br>
Die Swagger Seite ist nun über den Browser erreichbar. Der "port" muss durch den **Port** ersetzt werden<br>
Siehe nachfolgendes Bild.<br>
3. *http://127.0.0.1:"port"/swagger/#/*<br><br>
<img src="../images/hostPort.png"><br>