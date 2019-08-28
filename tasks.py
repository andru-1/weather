from celery import Celery

from webapp import create_app
from webapp.news.parsers import habr

from celery.schedules import crontab # управление расписанием

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# для запуска очереди celery
# from tasks import habr_content
# habr_content.delay()

@celery_app.task
def habr_snippets():
    with flask_app.app_context():
        habr.get_news_snippets()

@celery_app.task
def habr_content():
    with flask_app.app_context():
        habr.get_news_content()

# запуск задач по расписанию (tasks - файл)
# celery -A tasks beat
# celery -A tasks worker -B --loglevel=INFO - запуск расписания и воркера паралельно
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), habr_content.s()) # выполнение раз в минуту s() - просто надо ставить впереди