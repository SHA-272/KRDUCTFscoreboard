from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = 'ctfd_2c71a65dc478092a47cdebf982b250337ba33b3f15505001fd0dbec10f62b89e'
API_URL = 'https://krductf.ru/api/v1/scoreboard'

headers = {
    'Authorization': f'Token {API_KEY}',
    'Content-Type': 'application/json',
}

@app.route('/')
def index():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        scoreboard = response.json()['data']
        sorted_data = sorted(scoreboard, key=lambda x: x['pos'])
        top_three = sorted_data[:3]  # Получение первых трех мест
        return render_template('index.html', scoreboard=sorted_data, top_three=top_three)
    return 'Ошибка получения данных'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
