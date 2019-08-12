from webapp import db, create_app

# создание бд, вызываем каждый раз "python create_db.py" когда создаем новые данные таблиц в моделе webapp/model.py
db.create_all(app=create_app())