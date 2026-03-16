from tinydb import TinyDB
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
db = TinyDB('podatki.json')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/naloga1", methods=["POST"])
def naloga1():
    email = request.form['email']
    name = request.form['name']
    country = request.form['country'].upper()
    password = request.form['password']

    url = f"https://api.nationalize.io/?name={name}"
    response = requests.get(url)
    data = response.json()
    countries = [c['country_id'] for c in data['country']]

    if country in countries:
        db.append({
            "email": email,
            "name": name,
            "country": country,
            "password": password
        })
    else:
        return jsonify({"status": "error", "message": "ERROR: Ime ne ustreza izbrani državi."}), 400
    return render_template("naloga1.html")

app.run(debug=True)