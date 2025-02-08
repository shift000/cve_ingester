from flask import Flask, jsonify, request
from database import db, init_db
from models import CVEEntry
from sqlalchemy import inspect
import logging


logging.basicConfig(filename='cve_api.log', level=logging.INFO)

app = Flask(__name__)
init_db(app)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "running", "version": "1.0"})

@app.route("/add", methods=["POST"])
def add_cve():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        required_fields = ["id", "vendor", "product", "version", "description"]

        print("!==>")
        print(data, required_fields)
        print("<==!")
        # Prüfen, ob alle Felder vorhanden sind
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_cve = CVEEntry(
            id=data["id"],
            vendor=data["vendor"],
            product=data["product"],
            version=data["version"],
            description=data["description"]
        )

        db.session.add(new_cve)
        db.session.commit()

        return jsonify({"message": "CVE added successfully", "cve": new_cve.to_dict()}), 201
    except Exception as e:
        print(f"Fehler beim Hinzufügen der CVE: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["GET"])
def search():
    try:
        vendor = request.args.get("vendor")
        product = request.args.get("product")
        version = request.args.get("version")
        description = request.args.get("description")

        query = CVEEntry.query
        if vendor:
            query = query.filter(CVEEntry.vendor.ilike(f"%{vendor}%"))
        if product:
            query = query.filter(CVEEntry.product.ilike(f"%{product}%"))
        if version:
            query = query.filter(CVEEntry.version.ilike(f"%{version}%"))
        if description:
            query = query.filter(CVEEntry.description.ilike(f"%{description}%"))

        results = query.all()
        return jsonify([cve.to_dict() for cve in results])
    except Exception as e:
        print(f"Fehler beim Hinzufügen der CVE: {e}")
        return jsonify({"status": "failed", "route": "search", "error": str(e), "query": str(query), "version": "1.0"}), 500
    

@app.route("/delete/<cve_id>", methods=["DELETE"])
def delete_cve(cve_id):
    try:
        cve = CVEEntry.query.filter_by(id=cve_id).first()
    
        if not cve:
            return jsonify({"error": "CVE not found"}), 404
    
        db.session.delete(cve)
        db.session.commit()
    
        return jsonify({"message": f"CVE {cve_id} deleted successfully"}), 200
    except Exception as e:
        print(f"Fehler beim Löschen der CVE: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/update/<cve_id>", methods=["PUT"])
def update_cve(cve_id):
    try:
        cve = CVEEntry.query.filter_by(id=cve_id).first()

        if not cve:
            return jsonify({"error": "CVE not found"}), 404

        data = request.get_json()

        cve.vendor = data.get("vendor", cve.vendor)
        cve.product = data.get("product", cve.product)
        cve.version = data.get("version", cve.version)
        cve.description = data.get("description", cve.description)

        db.session.commit()

        return jsonify({"message": "CVE updated successfully", "cve": cve.to_dict()}), 200
    except Exception as e:
        print(f"Fehler beim Updaten der CVE: {e}")
        return jsonify({"error": str(e)}), 500

# Eine Route zum Testen der Tabellenabfrage
@app.route("/tables", methods=["GET"])
def tables():
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            return jsonify({"tables": tables})
    except Exception as e:
        print(f"Fehler beim Abrufen der Tables: {e}")
        return jsonify({"error": str(e)}), 500
    
# Route zum Abrufen der Tabellen und ihrer Spalten
@app.route("/tables_columns", methods=["GET"])
def tables_columns():
    try:
        with app.app_context():
            # Inspektor-Objekt zum Abrufen der Tabellen und ihrer Spalten
            inspector = inspect(db.engine)
        
            # Alle Tabellennamen abrufen
            tables = inspector.get_table_names()
        
            # Erstelle eine leere Liste, um Tabellen und Spalten zu speichern
            tables_columns = {}
        
            # Durchlaufe alle Tabellen und hole deren Spalten
            for table in tables:
                columns = [column["name"] for column in inspector.get_columns(table)]
                tables_columns[table] = columns
                
            return jsonify(tables_columns)
    except Exception as e:
        print(f"Fehler beim Abrufen der Tabellenspalten: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
