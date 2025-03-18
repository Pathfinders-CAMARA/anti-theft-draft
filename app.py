from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import requests
import json
import folium
import threading
import time
import random

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
def get_access_token(client_id, client_secret, scope):
    token_url = 'https://api.orange.com/oauth/v3/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()
    return response_data.get('access_token')
# Funkcja do generowania losowych stref (wielokątów) w Paryżu
def get_zones():
    zones = []
    base_lat = 48.8566  # Paryż
    base_lng = 2.3522

    for _ in range(5):  # Generujemy 5 losowych stref
        offset_lat = random.uniform(-0.01, 0.01)
        offset_lng = random.uniform(-0.01, 0.01)

        # Tworzymy prostokątny wielokąt (4 punkty + powrót do pierwszego)
        polygon = [
            [base_lat + offset_lat, base_lng + offset_lng],
            [base_lat + offset_lat + 0.005, base_lng + offset_lng],
            [base_lat + offset_lat + 0.005, base_lng + offset_lng + 0.005],
            [base_lat + offset_lat, base_lng + offset_lng + 0.005],
            [base_lat + offset_lat, base_lng + offset_lng]  # Zamykamy pętlę
        ]
        zones.append(polygon)

    return zones

# Funkcja do pobierania lokalizacji
def call_api(access_token, phone_number):
    api_url = 'https://api.orange.com/camara/orange-lab/location-retrieval/v0.3/retrieve'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-correlator': 'your_correlator'
    }
    data = {
        "device": {"phoneNumber": f"+{phone_number}"},
        "maxAge": 60000
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


# Endpoint do zwrócenia listy stref
@app.route('/zones')
def zones():
    return jsonify(get_zones())

@app.route('/')
def index():
    return render_template('index.html')

# Pobieranie lokalizacji urządzeń
def track_phones():
    client_id = 'XXXX'
    client_secret = 'XXXX'
    scope = ""
    access_token = get_access_token(client_id, client_secret, scope)
    while True:
        for number in range(33699901031, 33699901041):
            # time.sleep(5)  # Oczekiwanie 5 sekund przed kolejną aktualizacją
            api_response = call_api(access_token, str(number))

            if "area" in api_response:
                latitude = api_response["area"]["center"]["latitude"]
                longitude = api_response["area"]["center"]["longitude"]
                radius = api_response["area"]["radius"]

                socketio.emit('new_location', {
                    'lat': latitude,
                    'lng': longitude,
                    'radius': radius
                })

        time.sleep(1)  # Oczekiwanie 5 sekund przed kolejną aktualizacją

@socketio.on('connect')
def start_tracking():
    thread = threading.Thread(target=track_phones)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)

