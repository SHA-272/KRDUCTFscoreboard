from flask import Flask, render_template, jsonify
import requests, os, json

app = Flask(__name__)

API_KEY = os.environ.get(
    "CTFD_API_KEY",
    "ctfd_2c71a65dc478092a47cdebf982b250337ba33b3f15505001fd0dbec10f62b89e",
)
API_URL = os.environ.get("CTFD_URL", "https://krductf.ru")
API_SCOREBOARD_URL = f"""{API_URL}/api/v1/scoreboard"""
API_START_TIME_URL = f"""{API_URL}/api/v1/configs/start"""
API_END_TIME_URL = f"""{API_URL}/api/v1/configs/end"""

headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}


@app.route("/api/scoreboard")
def get_scoreboard():
    response = requests.get(API_SCOREBOARD_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        return jsonify(data)
    return jsonify({"error": "Failed to fetch scoreboard"}), 500


@app.route("/api/start")
def get_start_time():
    response = requests.get(API_START_TIME_URL, headers=headers)
    if response.status_code == 200:
        value = response.json()["data"]["value"]
        return jsonify(value)
    return jsonify({"error": "Failed to fetch start time"}), 500


@app.route("/api/end")
def get_end_time():
    response = requests.get(API_END_TIME_URL, headers=headers)
    if response.status_code == 200:
        value = response.json()["data"]["value"]
        return jsonify(value)
    return jsonify({"error": "Failed to fetch end time"}), 500


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
