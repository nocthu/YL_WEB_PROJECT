import pyowm

owm = pyowm.OWM('571078ba4550483db1e114541200905')

# Search for current weather in London (Great Britain)
observation = owm.weather_at_place('Moscow,RU')
w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
w.get_wind()                  # {'speed': 4.6, 'deg': 330}
w.get_humidity()              # 87
w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

