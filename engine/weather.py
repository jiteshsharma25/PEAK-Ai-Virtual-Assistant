import requests
import eel
@eel.expose
class WeatherService:
    def __init__(self):
        self.api_key = "6144b05826bb658d7d929fc6e95dcf34"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city_name):
        try:
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'city': city_name,
                'temp': data['main']['temp'],
                'desc': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'pressure': data['main']['pressure']
            }
        except Exception as e:
            return {'': str(e)}