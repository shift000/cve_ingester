#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:39:50 2025

@author: shift
"""

import requests

BASE_URL = "http://localhost:5000"  # Passe die URL an, falls dein API-Server woanders läuft

def add_cve(cve_id, vendor, product, version, description):
    """Sendet eine neue CVE an die API."""
    url = f"{BASE_URL}/add"
    data = {
        "id": cve_id,
        "vendor": vendor,
        "product": product,
        "version": version,
        "description": description
    }
    response = requests.post(url, json=data)
    return response.json()

def search_cve(vendor=None, product=None, version=None, description=None):
    """Sucht nach CVEs basierend auf den angegebenen Filtern."""
    url = f"{BASE_URL}/search"
    params = {
        "vendor": vendor,
        "product": product,
        "version": version,
        "description": description
    }
    response = requests.get(url, params=params)
    return response.json()

def delete_cve(cve_id):
    """Löscht eine CVE basierend auf der ID."""
    url = f"{BASE_URL}/delete/{cve_id}"
    response = requests.delete(url)
    return response.json()

def update_cve(cve_id, updated_data):
    """Aktualisiert eine bestehende CVE."""
    url = f"{BASE_URL}/update/{cve_id}"
    response = requests.put(url, json=updated_data)
    return response.json()

def get_tables_col():
    """Aktualisiert eine bestehende CVE."""
    url = f"{BASE_URL}/tables_columns"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    # 1️⃣ Beispiel: Neue CVE hinzufügen
    print("1:[➕] Neue CVE hinzufügen:")
    result = add_cve(
        cve_id="CVE-2025-0001",
        vendor="TestVendor",
        product="TestProduct",
        version="2.3",
        description="Testbeschreibung"
    )
    if "error" in result.keys():
        print("Error while creating new cve entry, maybe already existing?")
    else:
        print(result)
    
    print("\n2:[Tabellen COLS")
    print(get_tables_col())

    # 2️⃣ Beispiel: Nach CVEs suchen
    print("\n3:[🔍] Nach CVEs suchen:")
    results = search_cve(vendor="TestVendor")
    print(results)

    # 3️⃣ Beispiel: CVE aktualisieren
    print("\n4:[✏️] CVE aktualisieren:")
    updated_info = {"description": "Neue Beschreibung", "version": "9.0a"}
    result = update_cve("CVE-2025-0001", updated_info)
    print(result)
    
    # 2️⃣ Beispiel: Nach CVEs suchen
    print("\n5:[🔍] Nach CVEs suchen:")
    results = search_cve(vendor="TestVendor")
    print(results)

    # 4️⃣ Beispiel: CVE löschen
    print("\n6:[🗑️] CVE löschen:")
    result = delete_cve("CVE-2025-0001")
    print(result)
    
    # 2️⃣ Beispiel: Nach CVEs suchen
    print("\n7:[🔍] Nach CVEs suchen:")
    results = search_cve(vendor="TestVendor")
    print(results)
