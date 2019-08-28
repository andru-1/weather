from flask import abort, Blueprint, current_app, render_template
from webapp.news.models import News
from webapp.weather import wether_by_city # импортировали свою функцию

blueprint = Blueprint('news', __name__)

@blueprint.route('/')
def index():
    title = 'Прогноз погоды'
    weather = wether_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    #news_list = News.query.order_by(News.published.desc()).all() # возврат всех новостей из бд c сортировкой по дате
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all() # фильтр по новостям у которых текст существует
    return render_template('news/index.html', page_title=title, weather=weather, news_list=news_list)

@blueprint.route('/news/<int:news_id>') # только число
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first() # нашли запись
    if not my_news: # если не нашли запись, то возвращаем 404
        abort(404)
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news)
