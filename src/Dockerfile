# Use the Python 3.11.8 image based on Alpine Linux 3.19
FROM python:3.11.8-alpine3.19

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file from the parent directory to the working directory
COPY ../requirements.txt .

# Install Python dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the application source code from the parent directory's src folder to the working directory
COPY ./../src/. .

# Expose port 4000 to allow external connections
EXPOSE 4000

# Define the command to run the application when the container starts
CMD ["python", "app.py"]

# commands for building flask-app container:
# docker build -t flask-app .
# docker run -d -p 4000:4000 flask-app
