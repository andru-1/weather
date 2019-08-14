from functools import wraps # помощник в создании декораторов

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user # config - достает EXEMPT_METHODS с конфигов flask_login

def admin_required(func): # называем декоратор
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash('Эта страница только для админов')
            return redirect(url_for('news.index'))
        return func(*args, **kwargs)
    return decorated_view