from webapp import db, create_app

# создание бд
db.create_all(app=create_app())