import requests

from webapp.db import db # подключение бд
from webapp.news.models import News

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 YaBrowser/19.7.1.114 Yowser/2.5 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

# сохранение в бд
def save_news(title, url, published):
    # делаем проверку на то есть ли новость в бд
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()