import requests
s_city = "Petersburg,RU"
city_id = 0
appid = "буквенно-цифровой APPID"
appid2 = "571078ba4550483db1e114541200905"

try:
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()

except Exception as e:
    print("Exception (weather):", e)
    pass
