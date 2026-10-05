import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather():
    place = request.args.get("location", "").strip()
    if not place:
        return jsonify({"error": "Please enter a location"}), 400

    r = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": place, "appid": API_KEY, "units": "metric"},
        timeout=10,
    )

    if r.status_code == 401:
        return jsonify({"error": "Invalid API key (new keys can take up to 2 hours to activate)"}), 401
    if r.status_code == 404:
        return jsonify({"error": f"Could not find '{place}'. Try a city name."}), 404
    if not r.ok:
        return jsonify({"error": "Weather service error"}), 502

    d = r.json()
    return jsonify({
        "place": d["name"],
        "region": "",
        "country": d["sys"].get("country", ""),
        "temperature": round(d["main"]["temp"], 1),
        "temp_unit": "°C",
        "wind": d["wind"]["speed"],
        "wind_unit": "m/s",
    })

if __name__ == "__main__":
    app.run(debug=True)