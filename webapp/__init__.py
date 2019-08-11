from flask import Flask, render_template

from webapp.model import db, News
from webapp.weather import wether_by_city # импортировали свою функцию

# метод фабрики
def create_app():
    app = Flask(__name__) # фласк приложение, __name__ - имя текущего файла
    app.config.from_pyfile('config.py') # загрузка конфигураций
    db.init_app(app) # инициализируем базу данных

    @app.route('/')
    def index():
        title = 'Прогноз погоды'
        weather = wether_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all() # возврат  всех новостей из бд c сортировкой по дате
        return  render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    return app # возвращаем flask приложение

#if __name__ == '__main__': # если этот файл запускается напрямую
    #app.run(debug=True) # debug=True - у фласка есть дебаг режим