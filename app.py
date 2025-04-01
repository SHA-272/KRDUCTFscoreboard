from flask import Flask, render_template, jsonify
import requests, os

app = Flask(__name__)

API_KEY = os.getenv("CTFD_API_KEY")
API_URL = os.getenv("CTFD_URL")

API_SCOREBOARD_URL = f"{API_URL}/api/v1/scoreboard"
API_START_TIME_URL = f"{API_URL}/api/v1/configs/start"
API_END_TIME_URL = f"{API_URL}/api/v1/configs/end"
API_SUBMISSIONS_URL = f"{API_URL}/api/v1/submissions"

headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}


def fetch_from_api(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    return None


@app.route("/api/scoreboard")
def get_scoreboard():
    data = fetch_from_api(API_SCOREBOARD_URL)
    if data is not None:
        return jsonify(data)
    return jsonify({"error": "Failed to fetch scoreboard"}), 500


@app.route("/api/start")
def get_start_time():
    data = fetch_from_api(API_START_TIME_URL)
    if data is not None:
        return jsonify(data["value"])
    return jsonify({"error": "Failed to fetch start time"}), 500


@app.route("/api/end")
def get_end_time():
    data = fetch_from_api(API_END_TIME_URL)
    if data is not None:
        return jsonify(data["value"])
    return jsonify({"error": "Failed to fetch end time"}), 500


@app.route("/api/get_firstbloods")
def get_firstbloods():
    data = fetch_from_api(API_SUBMISSIONS_URL)
    correct_submissions = []
    if data is not None:
        for submission in data:
            if submission["type"] == "correct":
                correct_submissions.append(submission)
        return jsonify(correct_submissions)
    return jsonify({"error": "Failed to fetch submissions"}), 500


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
