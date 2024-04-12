import requests
from bs4 import BeautifulSoup
from weather.forecast_day import Forecast
from weather.forecast_week import Forecast_week
# Отправляем запрос на html страницу с данными о погоде на день
def get_html(link:str):
    cookies = {
        'ab_audience_2': '18',
        'cityIP': '4355',
        '_gid': 'GA1.2.301596128.1700483015',
        '_ym_uid': '1700483016114106815',
        '_ym_d': '1700483016',
        '_ym_isad': '1',
        '_ym_visorc': 'b',
        '_gat': '1',
        '_ga_JQ0KX9JMHV': 'GS1.1.1700483015.1.1.1700483165.60.0.0',
        '_ga': 'GA1.1.22345823.1700483015',
    }

    headers = {
        'authority': 'www.gismeteo.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'ab_audience_2=18; cityIP=4355; _gid=GA1.2.301596128.1700483015; _ym_uid=1700483016114106815; _ym_d=1700483016; _ym_isad=1; _ym_visorc=b; _gat=1; _ga_JQ0KX9JMHV=GS1.1.1700483015.1.1.1700483165.60.0.0; _ga=GA1.1.22345823.1700483015',
        'referer': 'https://yandex.ru/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36',
    }

    response = requests.get(link, cookies=cookies, headers=headers)
    return response.text
# Отправляем запрос на html страницу с данными о погоде на неделю
def get_html_week(link):

    headers = {
        'authority': 'www.gismeteo.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'ab_audience_2=64; cityIP=4335; _gid=GA1.2.1927169668.1700741570; _ym_uid=1700741570284313414; _ym_d=1700741570; _ym_isad=1; _ym_visorc=b; _ga_JQ0KX9JMHV=GS1.1.1700741570.1.1.1700742455.41.0.0; _ga=GA1.2.1887195620.1700741570',
        'referer': 'https://www.gismeteo.ru/weather-semenov-4335/tomorrow/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36',
    }

    response = requests.get(link+'10-days/', headers=headers)
    return response.text
# Сохранение html страницы в файл
def save_html(response, file_name):
    res = str(response.text)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(res)
# Чтение html страницы из файла
def read_html(file_name):
    with open(file_name,encoding='utf-8') as file:
        response = file.read()
    return response
#Сбор данных о погоде на день
def find_date(response):
    f = Forecast('NN')
    f.time = ['0:00','3:00','6:00','9:00','12:00','15:00','18:00','21:00']
    soup = BeautifulSoup(response, "html.parser")
    text = soup.find('div',class_='weathertabs day-1').find_all('span',class_="unit unit_temperature_c")
    f.temp_now = text[0].text
    f.temp_feel = text[1].text
    text = soup.find("div", class_='widget-items').find_all('div', class_='weather-icon tooltip')

    for element in text:
        f.description.append(element.attrs['data-text'])
    text = soup.find('div', class_='widget-row-chart widget-row-chart-temperature row-with-caption').find('div', class_='chart').find_all('span',class_='unit unit_temperature_c')
    for element in text:
        f.temp.append(element.string)
    f.time_now = soup.find('a',class_='weathertab weathertab-link tooltip').find('div',class_='day').string
    return f
#Сбор данных о погоде на неделю
def find_date_week(response,city_name):
    f = Forecast_week(city_name)
    f.time = ['0:00','3:00','6:00','9:00','12:00','15:00','18:00','21:00']
    soup = BeautifulSoup(response, "html.parser")

    text = soup.find("div", class_='widget-items').find_all('div', class_='weather-icon tooltip')

    for element in text:
        f.description.append(element.attrs['data-text'])
    text = soup.find('div', class_='widget-row widget-row-days-date').find_all('div', class_='day')
    for element in text:
        f.days_name.append(element.string)
    text = soup.find('div', class_='widget-row widget-row-days-date').find_all('div', class_='date')
    for element in text:
        f.days_int.append(element.string[:2])
    text = soup.find('div', class_='chart ten-days').find_all('div', class_='maxt')
    for element in text:
        f.temp_max.append(element.contents[0].string)
    text = soup.find('div', class_='chart ten-days').find_all('div', class_='mint')
    for element in text:
        f.temp_min.append(element.contents[0].string)
    return f
#Перевод данных о погоде на день в читаемую строку
def str_forecast(f:Forecast):
    #Проверяем удалось ли собрать данные
    if f.description == []:
        return None
    else:
        str = 'Температура '+f.temp_now+'\u2103 . Ощущается как '+f.temp_feel+'\u2103 \n'
        for i in range(8):
            str = str+'Температура в '+f.time[i]+' '+f.temp[i]+'\u2103  На улице '+f.description[i]+'\n'
        return str
#Перевод данных о погоде на неделю в читаемую строку    
def str_forecast_week(f:Forecast_week):
    #Проверяем удалось ли собрать данные
    if f.description == []:
        return None
    else:
        str = f'Погода в {f.city_name}:\n'
        for i in range(7):
            str = str+f'{f.days_name[i]} {f.days_int[i]} число.\n На улице {f.description[i]}. Температура от {f.temp_min[i]} до {f.temp_max[i]}\n'
        return str
# Сборка всех функций в одну и получение читаемой строки
def get_forecast_day_str(link:str):
    return str_forecast(find_date(get_html(link)))
# Сборка всех функций в одну и получение читаемой строки
def get_forecast_week_str (link:str, city_name: str):
    return str_forecast_week(find_date_week(get_html_week(link),city_name))

#save_html(get_html())










