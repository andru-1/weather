from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required # менеджер для всех логинов

from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route("/login")
def login():
    if current_user.is_authenticated: # если залогинен, то страница логина ненужна
        return redirect(url_for('news.index')) # перенаправляем на главную
    title = 'Авторизация'
    login_form = LoginForm() # создали экземпляр нашего класса
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit(): # валидируем данные
        user = User.query.filter(User.username == form.username.data).first() # сравниваем пользователей по имени
        if user and user.check_password(form.password.data): # если пользователь существует и проверка пароля прошла
            login_user(user, remember=form.remember_me.data) # логиним пользователя  запоминаем, remember - данные чекбокса с "запомнить меня"
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('news.index')) # редиректим на главную

    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route("/logout") # разлогиниваем пользователя
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index')) # перенаправляем на главную