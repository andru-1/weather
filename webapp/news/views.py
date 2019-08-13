from flask import Blueprint, current_app, render_template
from webapp.news.models import News
from webapp.weather import wether_by_city # импортировали свою функцию

blueprint = Blueprint('news', __name__)

@blueprint.route('/')
def index():
    title = 'Прогноз погоды'
    weather = wether_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.order_by(News.published.desc()).all() # возврат  всех новостей из бд c сортировкой по дате
    return render_template('index.html', page_title=title, weather=weather, news_list=news_list)