import os
import eel
from engine.features import *
from engine.command import *
from engine.weather import WeatherService
eel.init("web")
playassistantsound()
weather = WeatherService()
eel.expose(weather.get_weather)
os.system('start msedge.exe --app="http://localhost:8000/index.html"')
eel.start('index.html',mode=None,host="localhost",block=True)