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

# Funkcija, kuri grąžina ar lyja mieste
def get_rain_status():
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': get_lat_lon(city)[0],
        'longitude': get_lat_lon(city)[1],
        'current': 'precipitation',  # Dabartinis kritulių kiekis mm
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['current']['precipitation'] > 0:
        return True
    else:
        return False

# Funkcija, kuri grąžina saulėtekio ir saulėlydžio laikus
def get_sunrise_sunset():
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': get_lat_lon(city)[0],
        'longitude': get_lat_lon(city)[1],
        'daily': 'sunrise,sunset',
        'timezone': 'auto',
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Išgauname tik laiką (po 'T' simbolio)
    sunrise_time = data['daily']['sunrise'][0].split('T')[1]
    sunset_time = data['daily']['sunset'][0].split('T')[1]
    
    return sunrise_time, sunset_time

# Funkcija, kuri grąžina ar yra perkūnija 
def get_thunder():
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': get_lat_lon(city)[0],
        'longitude': get_lat_lon(city)[1],
        'current': 'weather_code',
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['current']['weather_code'] > 94 and data['current']['weather_code'] < 100:
        return True
    else:
        return False
