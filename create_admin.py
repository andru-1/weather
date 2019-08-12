from getpass import getpass # запрашивает инпут в командной строке
import sys

from webapp import create_app # наше фласк приложение
from webapp.model import db, User # наши модели

app = create_app()

with app.app_context():
    username = input('Введите имя:')

    if User.query.filter(User.username == username).count(): # проверка на существование пользователя
        print('Пользователь с таким именем уже есть')
        sys.exit(0)

    password1 = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')

    if not password1 == password2: # проверка на совпадение паролей
        print('Пароли не одинаковые')
        sys.exit(0)
    
    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))