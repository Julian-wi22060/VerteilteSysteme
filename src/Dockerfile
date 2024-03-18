# Verwenden Sie das Python Alpine-Image als Basisimage
FROM  python:3.11.8-alpine3.19

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Anforderungen in das Arbeitsverzeichnis
COPY ../requirements.txt .

# Installieren Sie die Anforderungen
RUN pip install -r requirements.txt

# Kopieren Sie den Rest des Codes in das Arbeitsverzeichnis
COPY ./../src/. .

# Öffnen Sie den Port, auf dem Ihr Flask-Server läuft (z. B. 8000)
EXPOSE 4000

# Befehl zum Ausführen Ihres Flask-Servers innerhalb des Containers
CMD ["python", "app.py"]

# docker build -t flask-app .
# docker run -d -p 8000:8000 flask-app
