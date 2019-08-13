from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required # менеджер для всех логинов

from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint

# метод фабрики
def create_app():
    app = Flask(__name__) # фласк приложение, __name__ - имя текущего файла
    app.config.from_pyfile('config.py') # загрузка конфигураций
    db.init_app(app) # инициализируем базу данных

    login_meneger = LoginManager()
    login_meneger.init_app(app)
    login_meneger.login_view = 'user.login' # название функции которая занимается логином пользователя
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)

    @login_meneger.user_loader # получение по id нужного пользователя
    def load_user(user_id):
        return User.query.get(user_id)

    return app # возвращаем flask приложение

#if __name__ == '__main__': # если этот файл запускается напрямую
    #app.run(debug=True) # debug=True - у фласка есть дебаг режим