from flask import Flask, render_template, jsonify
import requests, os, json

app = Flask(__name__)

API_KEY = os.environ.get("CTFD_API_KEY")
API_URL = os.environ.get("CTFD_API_URL")

headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}


@app.route("/api/scoreboard")
def get_scoreboard():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        # scoreboard = json.loads(open("users.json").read())
        scoreboard = response.json()["data"]
        return jsonify(scoreboard)
    return jsonify({"error": "Failed to fetch data"}), 500


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
