# Verwenden Sie ein offizielles Python-Laufzeitbild
FROM python:3.8

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie die benötigten Pakete
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den aktuellen Ordnerinhalt in den Container unter /app
COPY . .

# Führen Sie den Befehl aus, um den Server zu starten
CMD ["gunicorn", "mein_hrm.wsgi:application", "--bind", "0.0.0.0:8000"]
