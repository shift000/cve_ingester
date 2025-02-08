import json
from database import db, init_db
from models import CVEEntry
from flask import Flask

app = Flask(__name__)
init_db(app)

"""def insert_cve_data(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    
    with app.app_context():
        for entry in data:
            cve = CVEEntry(
                id=entry["id"],
                vendor=entry["vendor"],
                product=entry["product"],
                description=entry["description"],
                cvss_score=entry.get("cvss_score", 0)
            )
            db.session.add(cve)
        db.session.commit()

if __name__ == "__main__":
    insert_cve_data("cve_list.json")"""
