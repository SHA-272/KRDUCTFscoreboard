from flask import Flask, render_template, jsonify
import requests, os

app = Flask(__name__)

API_KEY = os.getenv(
    "CTFD_API_KEY",
    "ctfd_bacb1a23f432dc26bad66a3e6189b732c2c099610e5aa75d2d66b66b1b9798a6",
)
API_URL = os.getenv("CTFD_URL", "http://localhost:8000")

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


def fetch_all_submissions():
    page = 1
    all_submissions = []

    while True:
        response = requests.get(f"{API_SUBMISSIONS_URL}?page={page}", headers=headers)
        if not response.ok:
            return None

        json_data = response.json()
        all_submissions.extend(json_data.get("data", []))

        pagination = json_data.get("meta", {}).get("pagination", {})
        if pagination.get("next"):
            page = pagination["next"]
        else:
            break

    return all_submissions


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
    submissions = fetch_all_submissions()
    if submissions is None:
        return jsonify({"error": "Failed to fetch submissions"}), 500

    first_bloods = {}

    for submission in sorted(submissions, key=lambda x: x["date"]):
        if submission["type"] == "correct":
            chal_id = submission["challenge"]["id"]
            if chal_id not in first_bloods:
                first_bloods[chal_id] = submission

    return jsonify(list(first_bloods.values()))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
