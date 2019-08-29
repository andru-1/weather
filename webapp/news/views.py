from flask import abort, Blueprint, current_app, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required
from webapp.db import db

from webapp.news.forms import CommentForm # yнаша форма комментирования
from webapp.news.models import News, Comment
from webapp.weather import wether_by_city # импортировали свою функцию
from webapp.utils import get_redirect_target

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
    comment_form = CommentForm(news_id=my_news.id) # передаем в value id новости
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news, comment_form=comment_form)

# обработчик формы комментирования
@blueprint.route('/news/comment', methods=['POST'])
@login_required # если кто-то пошлет данные на страницу, то будет идти проверка на авторизацию
def add_comment():
    #pass # напишем код потом, но при компиляции не получим ошибку - потому что функция не может быть пустой
    form = CommentForm()
    if form.validate_on_submit(): # если форма провалидирована
        comment = Comment(text=form.comment_text.data, news_id=form.news_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')
    else:
        for field, errors in form.errors.items(): # field - название поля, errors - список ошибок
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target()) # редиректим на туже страницу