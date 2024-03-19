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
Im lokalen Betrieb ist die API-Dokumentation im Browser unter http://127.0.0.1:5000/swagger/ erreichbar. Im Betrieb mit Docker und Kubernetes ist sie jedoch unter http://localhost:4000/swagger/ zu finden.

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
   `docker-compose build`<br><br>
2. Die Container werden ausgeführt über:<br>
   `docker-compose up`<br><br>
3. Das Deployment kann beispielsweise mit 'curl' getestet werden:<br>
   `curl -d '{"selector": {"month": "5", "day":"23"}, "fields":["first","name","prof","year","month","day"], "sort": [{"year":"asc"}]}' -H "Content-Type: application/json" -X POST 'http://localhost:5984/birthday_db/_find' -u 'admin:student'`<br><br>

>Achtung: Bevor der Befehl docker-compose build verwendet werden kann, muss ein Image der Datenbank selbst bereits vorhanden sein, auf das dann von docker-compose.yaml zugegriffen wird.

### Kubernetes-Betrieb

#### Kubernetes initialisieren<br>
1. Der Minikube-Cluster wird im Hauptverzeichnis "/verteilteSysteme/" gestartet mit:<br>
   `minikube start`<br><br>
2. Setze die Umgebungsvariablen des Minikube Clusters mit:<br>
   `eval $(minikube docker-env)`<br><br>
3. Das Docker-Image für den julian-microservice wird mithilfe von Minikube gebaut mit:<br>
   `minikube image build -t julian-microservice:latest . -f src/Dockerfile`<br><br>
4. Wechsle in das Verzeichnis '/kubernetes/'<br>
   `cd kubernetes`<br><br>
5. Erstelle die ConfigMap mit:<br>
   `kubectl create -f configMap.yaml`<br><br>
6. Wende das Deployment an mit:<br>
   `kubectl apply -f deployment.yaml`<br><br>
7. Wende den Service an mit:<br>
   `kubectl apply -f service.yaml`<br><br>
8. Liste aller Pods im Minikube-Cluster ausgeben mit:<br>
   `kubectl get pods`<br><br>
9. Pod-Namen des Microservice-Pods kopieren<br>
<img src="../imgs/get_pods.png" style="width: 600px" alt="pod-list"><br><br>
10. Führe das port-forwarding für den Zugriff von außen mit dem Port 4000:4000 in einem neuen Terminal-Fenster durch mit:<br>
   `kubectl port-forward <POD-NAME> 4000:4000`<br><br>
11. Greife auf die Swagger-UI zu im Browser:<br>
   `localhost:4000/swagger`<br><br>

*Bei Bedarf*: Starte das minikube-Dashboard für Monitoring-Zwecke<br>
   `minikube dashboard`<br><br>
