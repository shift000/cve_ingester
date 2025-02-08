# Basis-Image mit Python
FROM python:3.10

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Anforderungen kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY . .

# Flask-App starten
CMD ["python", "app/main.py"]
