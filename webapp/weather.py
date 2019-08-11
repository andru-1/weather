from flask import current_app # загружаем возможность обращеня к текущему flask приложению
import requests

def wether_by_city(city_name):
    wether_url = current_app.config['WEATHER_URL']
    para = {
        'key': current_app.config['WEATHER_API_KEY'],
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
    print(wether_by_city('Odessa,Ukraine'))