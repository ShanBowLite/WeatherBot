import requests
import json

def get_weather(la:str,lo:str):
    api_key = "313ed803e5f87c3929f5a6824377acf4"
    lat = la
    lon = lo
    lang = "ru"
    units = "metric"

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang={lang}&units={units}&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Сохранение данных в файл geo.json
    #with open('weather.json','w', encoding='utf-8') as file:
    #    json.dump(data, file, indent=2, ensure_ascii=False)

    if data == [] :
        return 0, 0, 0
    else:
        return 1, round(data["main"]["temp"]), round(data["main"]["feels_like"])

"""
# Тестирование функционала
c = u"\u00b0"
lat = "56.3264816"
lon = "44.0051395"
res, temp, feels_like = get_weather(lat,lon)
if res == 0:
    print("В данный момент данные о погоде в этом городе недоступны.")
else:
    print(f"Температура {temp}{c}\nОщущается как {feels_like}{c}")
"""