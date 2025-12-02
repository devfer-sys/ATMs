from flask import Blueprint, render_template, request, jsonify
import sqlite3
import math

main = Blueprint('main', __name__)

def get_db():
    conn = sqlite3.connect("app/atm_lapaz_elalto.sqlite")  # ruta correcta
    conn.row_factory = sqlite3.Row
    return conn

# Distancia Haversine
def distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(float(lat2) - float(lat1))
    dLon = math.radians(float(lon2) - float(lon1))
    a = (math.sin(dLat/2)**2 +
         math.cos(math.radians(float(lat1))) *
         math.cos(math.radians(float(lat2))) *
         math.sin(dLon/2)**2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))


@main.route("/")
def home():
    return render_template("home.html")

@main.route("/buscar", methods=["POST"])
def buscar():
    data = request.get_json()
    user_lat = data["lat"]
    user_lon = data["lon"]
    banco = data["banco"]

    conn = get_db()
    cursor = conn.cursor()
    if banco == "todos":
        cursor.execute("SELECT * FROM atms")
    else:
        cursor.execute("SELECT * FROM atms WHERE banco LIKE ?", ('%' + banco + '%',))
    atms = cursor.fetchall()

    resultados = []
    for atm in atms:
        d = distancia(user_lat, user_lon, atm["lat"], atm["lon"])
        resultados.append({
            "osm_id": atm["osm_id"],
            "banco": atm["banco"],
            "lat": atm["lat"],
            "lon": atm["lon"],
            "direccion": atm["direccion"],
            "distancia": round(d, 2)
        })
    resultados = sorted(resultados, key=lambda x: x["distancia"])
    return jsonify(resultados)
