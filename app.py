from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Конфигурация API
API_KEY = os.getenv("CTFD_API_KEY")
API_URL = os.getenv("CTFD_URL", "http://localhost:8000")

HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}

ENDPOINTS = {
    "scoreboard": f"{API_URL}/api/v1/scoreboard",
    "start_time": f"{API_URL}/api/v1/configs/start",
    "end_time": f"{API_URL}/api/v1/configs/end",
    "submissions": f"{API_URL}/api/v1/submissions",
}


def fetch_from_api(url):
    """Запрашивает данные с API и возвращает содержимое поля 'data'."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("data")
    except requests.RequestException:
        return None


def fetch_paginated_data(url):
    """Извлекает все данные с пагинацией по указанному URL."""
    page = 1
    all_data = []

    while True:
        try:
            response = requests.get(f"{url}?page={page}", headers=HEADERS)
            response.raise_for_status()
            json_data = response.json()
            all_data.extend(json_data.get("data", []))

            pagination = json_data.get("meta", {}).get("pagination", {})
            page = pagination.get("next")
            if not page:
                break
        except requests.RequestException:
            return None

    return all_data


@app.route("/api/scoreboard")
def get_scoreboard():
    """Получить таблицу результатов."""
    data = fetch_from_api(ENDPOINTS["scoreboard"])
    return (
        jsonify(data)
        if data
        else (jsonify({"error": "Failed to fetch scoreboard"}), 500)
    )


@app.route("/api/start")
def get_start_time():
    """Получить время начала CTF."""
    data = fetch_from_api(ENDPOINTS["start_time"])
    return (
        jsonify(data["value"])
        if data
        else (jsonify({"error": "Failed to fetch start time"}), 500)
    )


@app.route("/api/end")
def get_end_time():
    """Получить время окончания CTF."""
    data = fetch_from_api(ENDPOINTS["end_time"])
    return (
        jsonify(data["value"])
        if data
        else (jsonify({"error": "Failed to fetch end time"}), 500)
    )


@app.route("/api/get_firstbloods")
def get_firstbloods():
    """Получить первые успешные отправки (First Bloods) по задачам."""
    submissions = fetch_paginated_data(ENDPOINTS["submissions"])
    if submissions is None:
        return jsonify({"error": "Failed to fetch submissions"}), 500

    first_bloods = {}
    sorted_subs = sorted(submissions, key=lambda x: x["date"])

    for sub in sorted_subs:
        if sub.get("type") == "correct":
            challenge_id = sub["challenge"]["id"]
            if challenge_id not in first_bloods:
                first_bloods[challenge_id] = sub

    return jsonify(list(first_bloods.values()))


@app.route("/")
def index():
    """Главная страница."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
