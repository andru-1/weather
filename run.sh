#!/bin/sh
export FLASK_APP=webapp && FLASK_ENV=development && flask run
# для запуска в корне проекта выполнить команду chmod +x run.sh и для запуска сервера "./run.sh"