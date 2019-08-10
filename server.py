from flask import Flask
from weather import wether_by_cyty # импортировали свою функцию

app = Flask(__name__) # фласк приложение, __name__ - имя текущего файла

@app.route('/')
def index():
    weather = wether_by_cyty('Odessa,Ukraine')
    #weather = False 
    # делаем проверку что бы не упал сервер
    if weather:
        return f"Погода: {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}" # f - форматирование строк
    else:
        return "Сервис погоды временно недоступен"
if __name__ == '__main__': # если этот файл запускается напрямую
    app.run(debug=True) # debug=True - у фласка есть дебаг режим