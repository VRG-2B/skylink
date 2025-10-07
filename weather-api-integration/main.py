import requests

city = 'vilnius' # Laikinas placeholderis, kol ateityje gausiu miesto inputą iš Minecraft

# Funkcija, kuri grąžina miesto platumą ir ilgumą
def get_lat_lon(city):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': city,
        'format': 'json',
        'limit': 1,
    }

    response = requests.get(url, params=params, headers={'User-Agent': 'city-lat-lon-script'})
    data = response.json()

    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon

# Funkcija, kuri grąžina miesto temperatūrą
def get_temperature():
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': get_lat_lon(city)[0],
        'longitude': get_lat_lon(city)[1],
        'current': 'temperature_2m',
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data['current']['temperature_2m']

print(get_lat_lon('Uk/London'))
