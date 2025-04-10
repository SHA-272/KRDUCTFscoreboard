from flask import Flask, render_template, jsonify
import requests, os
import json

app = Flask(__name__)

API_KEY = os.getenv("CTFD_API_KEY")
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
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except KeyError:
        print("Unexpected response format: 'data' key not found")
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
    page = 1
    first_bloods = {}

    while True:
        submissions = fetch_from_api(f"{API_SUBMISSIONS_URL}?page={page}")
        if submissions is None:
            return jsonify({"error": "Failed to fetch submissions"}), 500

        for submission in sorted(submissions, key=lambda x: x["date"]):
            if submission["type"] == "correct":
                chal_id = submission["challenge"]["id"]
                if chal_id not in first_bloods:
                    first_bloods[chal_id] = submission

        pagination = submissions.get("meta", {}).get("pagination", {})
        if not pagination.get("next"):
            break
        page = pagination["next"]

    return jsonify(list(first_bloods.values()))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
