# Verwenden Sie das Python Alpine-Image als Basisimage
FROM python:alpine

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Anforderungen in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren Sie die Anforderungen
RUN pip install -r requirements.txt

# Kopieren Sie den Rest des Codes in das Arbeitsverzeichnis
COPY . .

# Öffnen Sie den Port, auf dem Ihr Flask-Server läuft (z. B. 8000)
EXPOSE 8000

# Befehl zum Ausführen Ihres Flask-Servers innerhalb des Containers
CMD ["python", "microservice/app.py"]

# docker build -t flask-app .
# docker run -d -p 8000:8000 flask-app
