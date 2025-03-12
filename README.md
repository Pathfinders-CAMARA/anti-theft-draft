# A draft of anti-theft functionality
This script helps locate a stolen vehicle by retrieving the location of a linked mobile device, even if GPS jamming is used. It utilizes the **Orange Camara API** to get the device's approximate location.

## Features
- OAuth2 authentication with Camara API
- Retrieves location based on phone number
- Visualizes results on an interactive map using Folium

## Usage
1. Replace `client_id` and `client_secret` with valid credentials.
2. Run the script to obtain an access token.
3. The script queries multiple phone numbers for location data.
4. Generates a **map (mapa.html)** with detected locations.
