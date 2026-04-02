import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :
@app.route("/contact")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"  

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/atelier")
def atelier():
    # Coordonnées de Hyères (83)
    lat, lon = 43.12, 6.12
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunshine_duration&timezone=Europe%2FBerlin"
    
    try:
        response = requests.get(url)
        data = response.json()

        # Récupération de la durée d'ensoleillement (en secondes) pour aujourd'hui
        sunshine_seconds = data.get("daily", {}).get("sunshine_duration", [0])[0]
        
        # Conversion en heures : 3600 secondes = 1 heure
        sun_hours = round(sunshine_seconds / 3600, 1)
        # Calcul du reste de la journée (24h - soleil) pour le graphique donut
        other_hours = round(24 - sun_hours, 1)
        
        return render_template("atelier.html", sun=sun_hours, other=other_hours)
    except Exception as e:
        return f"Erreur lors de la récupération des données : {e}"




# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001, debug=True)
