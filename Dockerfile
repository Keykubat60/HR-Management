# Verwenden Sie ein offizielles Python-Laufzeitbild
FROM python:3.8

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie die benötigten Pakete
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den aktuellen Ordnerinhalt in den Container unter /app
COPY . .

# Kopieren Sie das Einstiegspunkt-Skript und machen Sie es ausführbar
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
