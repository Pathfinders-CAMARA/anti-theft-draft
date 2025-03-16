import requests
import json

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
    access_token = response_data.get('access_token')
    return response_data['access_token']

def call_api(access_token,phone_number='33699901032'):
    api_url = 'https://api.orange.com/camara/orange-lab/location-retrieval/v0.3/retrieve'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-correlator': 'your_correlator'
    }
    data = {
        "device": {
            "phoneNumber": f"+{phone_number}"
        },
        "maxAge": 60000
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


# Replace 'your_client_id' and 'your_client_secret' with actual values
client_id = 'XXXXX'
client_secret = 'XXXXX'
scope = ""

access_token = get_access_token(client_id, client_secret, scope)
api_response = call_api(access_token)
# resp = json.dumps(api_response, indent=4)
# print(resp)



import folium
latitude = api_response["area"]["center"]["latitude"]
longitude = api_response["area"]["center"]["longitude"]
radius=api_response["area"]["radius"]
m = folium.Map(location=[latitude, longitude], zoom_start=14)


for number in range(33699901031,33699901041):
    print(number)
    api_response = call_api(access_token,str(number))

    if("area" in api_response):


        latitude = api_response["area"]["center"]["latitude"]
        longitude = api_response["area"]["center"]["longitude"]
        radius=api_response["area"]["radius"]

        # Tworzenie mapy


        # Dodanie kółka
        folium.Circle(
            location=[latitude, longitude],
            radius=radius,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.3,
            popup="Obszar 500m"
        ).add_to(m)

        # Zapisanie do pliku i wyświetlenie
        m.save("mapa.html")
