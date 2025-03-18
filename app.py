# from flask import Flask, render_template, jsonify
# from flask_socketio import SocketIO
# import requests
# import json
# import folium
# import threading
# import time
# import random
# import numpy as np

# base_lat = 48.8566  # Paryż
# base_lng = 2.3522


# start_lat, start_lng = 48.8600642869461, 2.356881359794606
# end_lat, end_lng = 48.86260871301927, 2.3598038121761085
# total_time = 20  # Czas w sekundach
# steps = 20  # Ilość kroków (1 krok = 1 sekunda)


# app = Flask(__name__)
# socketio = SocketIO(app, async_mode='threading')
# def get_access_token(client_id, client_secret, scope):
#     token_url = 'https://api.orange.com/oauth/v3/token'
#     payload = {
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'scope': scope
#     }
#     response = requests.post(token_url, data=payload)
#     response_data = response.json()
#     return response_data.get('access_token')
# # Funkcja do generowania losowych stref (wielokątów) w Paryżu
# # Funkcja do generowania losowych stref (wielokątów) w Paryżu
# def get_zones():
#     zones = []

#     # Pierwsza strefa (czerwona) - po lewej
#     polygon_1 = [
#         [base_lat, base_lng],
#         [base_lat + 0.005, base_lng],
#         [base_lat + 0.005, base_lng + 0.005],
#         [base_lat, base_lng + 0.005],
#         [base_lat, base_lng]  # Zamknięcie pętli
#     ]

#     # Druga strefa (zielona) - po prawej, obok pierwszej
#     polygon_2 = [
#         [base_lat + 0.0025, base_lng + 0.006],  # Odsunięcie w prawo o 0.006 stopnia
#         [base_lat + 0.005 + 0.0025, base_lng + 0.006],
#         [base_lat + 0.005 + 0.0025, base_lng + 0.011],
#         [base_lat + 0.0025, base_lng + 0.011],
#         [base_lat + 0.0025, base_lng + 0.006]  # Zamknięcie pętli
#     ]

#     zones.append({"polygon": polygon_1, "color": "red"})
#     zones.append({"polygon": polygon_2, "color": "green"})

#     return zones


# # Funkcja do pobierania lokalizacji
# def call_api(access_token, phone_number):
#     api_url = 'https://api.orange.com/camara/orange-lab/location-retrieval/v0.3/retrieve'
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'x-correlator': 'your_correlator'
#     }
#     data = {
#         "device": {"phoneNumber": f"+{phone_number}"},
#         "maxAge": 60000
#     }
#     response = requests.post(api_url, headers=headers, json=data)
#     return response.json()


# def move_point():
#     latitudes = np.linspace(start_lat, end_lat, steps)  # Interpolacja współrzędnych
#     longitudes = np.linspace(start_lng, end_lng, steps)

#     for i in range(steps):
#         socketio.emit('new_location', {
#             'lat': round(latitudes[i], 17),  # Zaokrąglamy do 7 miejsc po przecinku
#             'lng': round(longitudes[i], 17),
#             'radius': 10  # Stały promień dla wizualizacji
#         })
#         print({
#             'lat': round(latitudes[i], 17),  # Zaokrąglamy do 7 miejsc po przecinku
#             'lng': round(longitudes[i], 17),
#             'radius': 10  # Stały promień dla wizualizacji
#         })
#         time.sleep(1)  # Przemieszczenie co 1 sekunda

# # Endpoint do zwrócenia listy stref
# @app.route('/zones')
# def zones():
#     return jsonify(get_zones())

# @app.route('/')
# def index():
#     return render_template('index.html')

# # Pobieranie lokalizacji urządzeń
# def track_phones():
#     client_id = 'XXX'
#     client_secret = 'XXX'
#     scope = ""
#     access_token = get_access_token(client_id, client_secret, scope)

#     # for number in range(33699901031, 33699901041):
#     #     # time.sleep(5)  # Oczekiwanie 5 sekund przed kolejną aktualizacją
#     #     api_response = call_api(access_token, str(number))

#     #     if "area" in api_response:
#     #         latitude = api_response["area"]["center"]["latitude"]
#     #         longitude = api_response["area"]["center"]["longitude"]
#     #         radius = api_response["area"]["radius"]

#     #         socketio.emit('new_location', {
#     #             'lat': latitude,
#     #             'lng': longitude,
#     #             'radius': radius
#     #         })
#     move_point()
#     # while True:
#         #symulacja ruchu elemetnu między dwoma strefami 

#         # time.sleep(1)  # Oczekiwanie 5 sekund przed kolejną aktualizacją

# @socketio.on('connect')
# def start_tracking():
#     thread = threading.Thread(target=track_phones)
#     thread.daemon = True
#     thread.start()

# if __name__ == '__main__':
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)





from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import numpy as np
import threading
import time
import math

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

# Stałe dla Paryża
base_lat = 48.8566
base_lng = 2.3522

# Współrzędne ruchu

end_lat, end_lng = 48.86501150149537, 2.362541102251586
start_lat, start_lng = 48.857510599472, 2.354222372748941
total_time = 80  # Czas na pełen cykl (tam i z powrotem)
steps = 160  # Ilość kroków

# Startowy timestamp
start_time = time.time()

# Funkcja generująca stałe strefy
def get_zones():
    return [
        {
            "polygon": [
                [base_lat, base_lng],
                [base_lat + 0.005, base_lng],
                [base_lat + 0.005, base_lng + 0.005],
                [base_lat, base_lng + 0.005],
                [base_lat, base_lng]
            ],
            "color": "red",
            "name": "30 kph zone"
        },
        {
            "polygon": [
                [base_lat + 0.0025, base_lng + 0.006],
                [base_lat + 0.0075, base_lng + 0.006],
                [base_lat + 0.0075, base_lng + 0.011],
                [base_lat + 0.0025, base_lng + 0.011],
                [base_lat + 0.0025, base_lng + 0.006]
            ],
            "color": "green",
            "name": "50 kph zone"
        }
    ]

@app.route('/zones')
def zones():
    return jsonify(get_zones())

@app.route('/')
def index():
    return render_template('index.html')

# Funkcja do synchronizacji ruchu
def move_point():
    global start_time
    latitudes_forward = np.linspace(start_lat, end_lat, steps//2)
    longitudes_forward = np.linspace(start_lng, end_lng, steps//2)
    latitudes_backward = np.linspace(end_lat, start_lat, steps//2)
    longitudes_backward = np.linspace(end_lng, start_lng, steps//2)

    while True:
        current_time = time.time()
        elapsed_time = (current_time - start_time) % total_time  # Cykliczne odmierzanie czasu
        index = int((elapsed_time / (total_time / steps)) % steps)  # Obliczenie pozycji w cyklu

        # Ruch tam i z powrotem
        if index < steps // 2:
            lat = latitudes_forward[index]
            lng = longitudes_forward[index]
        else:
            lat = latitudes_backward[index - steps // 2]
            lng = longitudes_backward[index - steps // 2]

        socketio.emit('new_location', {
            'lat': round(lat, 7),
            'lng': round(lng, 7),
            'radius': 10
        })

        time.sleep(1)  # Wysyłanie co sekundę

# Uruchamiamy ruch tylko raz
thread = threading.Thread(target=move_point)
thread.daemon = True
thread.start()

@socketio.on('connect')
def send_current_position():
    current_time = time.time()
    elapsed_time = (current_time - start_time) % total_time
    index = int((elapsed_time / (total_time / steps)) % steps)

    if index < steps // 2:
        lat = np.linspace(start_lat, end_lat, steps//2)[index]
        lng = np.linspace(start_lng, end_lng, steps//2)[index]
    else:
        lat = np.linspace(end_lat, start_lat, steps//2)[index - steps//2]
        lng = np.linspace(end_lng, start_lng, steps//2)[index - steps//2]

    socketio.emit('new_location', {
        'lat': round(lat, 7),
        'lng': round(lng, 7),
        'radius': 10
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
