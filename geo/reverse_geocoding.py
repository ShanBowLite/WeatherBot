import requests
import json
# Поиск русского названия города по координатам
def get_city_name(lat: str,lot:str):
    api_key = "313ed803e5f87c3929f5a6824377acf4"
    la = lat
    lo= lot
    limit = "1"

    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={la}&lon={lo}&limit={limit}&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Сохранение данных в файл geo.json
    #with open('reverse_geo.json','w', encoding='utf-8') as file:
    #    json.dump(data, file, indent=2, ensure_ascii=False)

    if data == [] :
        return 0, "" 
    else:
        return 1, data[0]["local_names"]["ru"]

"""
# Тестирование функционала
lat = "56.3264816"
lon = "44.0051395"
res, city_name = get_city_name(lat,lon)
if res == 0:
    print("Города с такими координатами не найдено")
else:
    print(f"Город {city_name} имеет координаты:\nx:{lat}\ny:{lon}")
"""