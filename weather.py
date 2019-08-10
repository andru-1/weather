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

    try:
        result = requests.get(wether_url, params=para)
        result.raise_for_status() # сгенерирует ошибку когда сервер вернул 4хх или 5хх ошибку
        weather = result.json()
        if 'data' in weather: # проверка на существование элемента 'data'
            if 'current_condition' in weather['data']: # проверка на существование элемента 'current_condition'
                try: # если есть, то возвращаем
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError): # иначе обрабатываем возможные ошибки и вызвращаем False
                    return False
    except(requests.RequestException, ValueError): # перехватываем исключения (например нет интернета), не верный формат json
        print('Сетевая ошибка')
        return False
    return False

if __name__ == '__main__':
    print(wether_by_cyty('Odessa,Ukraine'))