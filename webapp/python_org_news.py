from datetime import datetime

import requests
from bs4 import BeautifulSoup # html разборщик

from webapp.db import db, News # подключение бд
from webapp.news.models import News

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

def get_python_news():
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title =  news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, '%Y-%m-%d') # преобразование даты  внужный формат
            except(ValueError):
                published = datetime.now()
            save_news(title, url, published)

# сохранение в бд
def save_news(title, url, published):
    # делаем проверку на то есть ли новость в бд
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()