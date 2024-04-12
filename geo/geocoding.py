import requests
import json
# Проверяем можно ли определить координаты по названию города
def get_cord(city_name: str):
    api_key = "313ed803e5f87c3929f5a6824377acf4"
    city = city_name
    country_code = "643"
    limit = "1"

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit={limit}&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Сохранение данных в файл geo.json
    #with open('geo.json','w', encoding='utf-8') as file:
    #    json.dump(data, file, indent=2, ensure_ascii=False)

    """if data == [] :
        return 0, 0, 0
    else:
        return 1, data[0]['lat'],data[0]['lon']
    """
    if data == []:
        return 0
    else:
        return 1
# Определяем координаты по названию города
def get_cord_ll(city_name: str):
    api_key = "313ed803e5f87c3929f5a6824377acf4"
    city = city_name
    country_code = "643"
    limit = "1"

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit={limit}&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Сохранение данных в файл geo.json
    #with open('geo.json','w', encoding='utf-8') as file:
    #    json.dump(data, file, indent=2, ensure_ascii=False)

    if data == [] :
        return 0, 0, 0
    else:
        return 1, data[0]['lat'],data[0]['lon']

""" Тестирование функционала
name_city = "Нижний Новгород"
res, lat, lon = get_cord(name_city)
if res == 0:
    print("Города с таким названием не найдено")
else:
    print(f"Город {name_city} имеет координаты:\nx:{lat}\ny:{lon}")
"""
