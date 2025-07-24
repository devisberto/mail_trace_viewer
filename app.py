"""
Email Trace App - Web application to analyze email headers and display routing and reputation information.

Copyright (C) 2025 Devis Berto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask import Flask, render_template, request, jsonify, Response
from parser import extract_hops
import json
import requests
import os

app = Flask(__name__)

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def enrich_with_country_coords_reputation(hops):
    enriched = []
    for hop in hops:
        ip = hop.get('ip')
        country = ""
        lat = lon = None
        reputation = "Unknown"

        if ip:
            try:
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if geo.ok:
                    info = geo.json()
                    country = info.get('country', '')
                    lat = info.get('lat')
                    lon = info.get('lon')
            except requests.RequestException:
                pass

            if ABUSEIPDB_API_KEY:
                try:
                    abuse = requests.get(
                        f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90",
                        headers={"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"})
                    if abuse.ok:
                        abuse_data = abuse.json()
                        reputation = "Bad" if abuse_data['data']['abuseConfidenceScore'] > 25 else "Good"
                except requests.RequestException:
                    pass

        hop['country'] = country
        hop['lat'] = lat
        hop['lon'] = lon
        hop['reputation'] = reputation
        enriched.append(hop)
    return enriched

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/parse", methods=["POST"])
def parse():
    headers = request.form.get("headers", "")
    hops = extract_hops(headers)
    enriched_hops = enrich_with_country_coords_reputation(hops)
    return jsonify(enriched_hops)

@app.route("/export", methods=["POST"])
def export():
    headers = request.form.get("headers", "")
    hops = extract_hops(headers)
    enriched_hops = enrich_with_country_coords_reputation(hops)
    output = json.dumps(enriched_hops, indent=2)
    return Response(
        output,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=email_trace.json"}
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
