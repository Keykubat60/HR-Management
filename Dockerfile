# Verwenden Sie ein offizielles Python-Laufzeitbild
FROM python:3.8

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie die benötigten Pakete
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den aktuellen Ordnerinhalt in den Container unter /app
COPY . .

# Führen Sie die Befehle aus
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Starten Sie die Anwendung
CMD ["gunicorn", "mein_hrm.wsgi:application", "--bind", "0.0.0.0:8000"]
