import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 54.6892,
    "longitude": 25.2798,
    "current": "is_day,temperature_2m,rain",
}

response = requests.get(url, params=params)

data = response.json()
print("Temperatūra:", data["current"]["temperature_2m"], "°C")
print("Ar diena:", "Taip" if data["current"]["is_day"] == 1 else "Ne")
print("Ar lyja:", "Taip" if data["current"]["rain"] > 0 else "Ne")
