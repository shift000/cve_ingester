Alles bereinigen mit
**sudo docker compose down -v**

danach starten mit
**sudo docker compose up --build**

Struktur ist
- Dockerfile
- docker-compose.yml
- requirements.txt
- ingester-client.py
- /app
  - database.py
  - insert_data.py
  - main.py
  - models.py
