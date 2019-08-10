from flask import Flask, render_template

from python_org_news import get_python_news
from weather import wether_by_cyty # импортировали свою функцию

app = Flask(__name__) # фласк приложение, __name__ - имя текущего файла

@app.route('/')
def index():
    title = 'Прогноз погоды'
    weather = wether_by_cyty('Odessa,Ukraine')
    news_list = get_python_news()
    return  render_template('index.html', page_title=title, weather=weather, news_list=news_list)

if __name__ == '__main__': # если этот файл запускается напрямую
    app.run(debug=True) # debug=True - у фласка есть дебаг режим