import requests

def wether_by_cyty(city_name):
    wether_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    para = {
        'key': '9d3bf4bc06864414aa4122545191008',
        'q': city_name,
        'format': 'json',
        'num_of_day': 1,
        'lang': 'ru'
    }
    result = requests.get(wether_url, params=para)
    weather = result.json()
    if 'data' in weather: # проверка на существование элемента 'data'
        if 'current_condition' in weather['data']: # проверка на существование элемента 'current_condition'
            try: # если есть, то возвращаем
                return weather['data']['current_condition'][0]
            except(IndexError, TypeError): # иначе обрабатываем возможные ошибки и вызвращаем False
                return False
    return False
