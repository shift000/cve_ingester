from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cve_user:cve_password@db:5432/cve_db"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database/cve_db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Erstellt die Tabelle, falls sie nicht existiert
        print("✅ Datenbank und Tabelle `cve_entry` erfolgreich erstellt.")
        
        # Prüfe, ob Tabellen existieren
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📌 Existierende Tabellen: {tables}")