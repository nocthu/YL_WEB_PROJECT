import requests


# try:
#     res = requests.get("http://api.openweathermap.org/data/2.5/weather",
#                  params={'units': 'metric', 'lang': 'ru', 'APPID': appid})
#     data = res.json()
#     print(data)
#
# except Exception as e:
#     print("Exception (weather):", e)
#     pass


s_city = "Petersburg,RU"
city_id = 0
appid = "eacbcd14d851ef4babf54d5073484017"
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                 params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    print(data)
    print("conditions:", data['weather'][0]['description'])
    print("temp:", data['main']['temp'])
    print("temp_min:", data['main']['temp_min'])
    print("temp_max:", data['main']['temp_max'])
except Exception as e:
    print("Exception (find):", e)
    pass