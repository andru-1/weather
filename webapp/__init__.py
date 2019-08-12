from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required # менеджер для всех логинов

from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import wether_by_city # импортировали свою функцию

# метод фабрики
def create_app():
    app = Flask(__name__) # фласк приложение, __name__ - имя текущего файла
    app.config.from_pyfile('config.py') # загрузка конфигураций
    db.init_app(app) # инициализируем базу данных

    login_meneger = LoginManager()
    login_meneger.init_app(app)
    login_meneger.login_view = 'login' # название функции которая занимается логином пользователя

    @login_meneger.user_loader # получение по id нужного пользователя
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        print(current_user)
        title = 'Прогноз погоды'
        weather = wether_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all() # возврат  всех новостей из бд c сортировкой по дате
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    @app.route("/login")
    def login():
        if current_user.is_authenticated: # если залогинен, то страница логина ненужна
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm() # создали экземпляр нашего класса
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit(): # валидируем данные
            user = User.query.filter(User.username == form.username.data).first() # сравниваем пользователей по имени
            if user and user.check_password(form.password.data): # если пользователь существует и проверка пароля прошла
                login_user(user) # логиним пользователя  запоминаем
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index')) # редиректим на главную

        flash('Неправильные имя или пароль')
        return redirect(url_for('login'))

    @app.route("/logout") # разлогиниваем пользователя
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route("/admin")
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ'

    return app # возвращаем flask приложение

#if __name__ == '__main__': # если этот файл запускается напрямую
    #app.run(debug=True) # debug=True - у фласка есть дебаг режим