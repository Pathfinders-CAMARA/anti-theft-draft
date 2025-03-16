import folium

# Środek okręgu
latitude = 52.2298
longitude = 21.0122
radius = 500  # w metrach

# Tworzenie mapy
m = folium.Map(location=[latitude, longitude], zoom_start=14)

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
