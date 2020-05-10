import pyowm, requests, pprint
#
# owm = pyowm.OWM('eacbcd14d851ef4babf54d5073484017')
#
# # Search for current weather in London (Great Britain)
# observation = owm.weather_at_place('москва')
# w = observation.get_weather()
# print(w)                      # <Weather - reference time=2013-12-18 09:20,
#                               # status=Clouds>
#
# # Weather details
# w.get_wind()                  # {'speed': 4.6, 'deg': 330}
# w.get_humidity()              # 87
# w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
#
# city = 'москва'
# url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eacbcd14d851ef4babf54d5073484017'
# appid = 'eacbcd14d851ef4babf54d5073484017'
# city_id = 0
# r = requests.get(url.format(city)).json()
# res = requests.get("http://api.openweathermap.org/data/2.5/weather",
#                    params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
# weather = {
#     'city': city,
#     'temperature': r['main']['temp'],
#     'description': r['weather'][0]['description'],
#     'icon': r['weather'][0]['icon']
# }
# print(res)
city = 'Moscow'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eacbcd14d851ef4babf54d5073484017'
appid = 'eacbcd14d851ef4babf54d5073484017'
city_id = 0
r = requests.get(url.format(city)).json()
pprint.pprint(r)
weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
}