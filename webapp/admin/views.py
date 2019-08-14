from flask import Blueprint, render_template
#from flask_login import current_user, login_required
from webapp.user.decorators import admin_required # вызываем наш декоратор

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def admin_index(): # если проверка admin_required прошла, то он точно админ
    #return 'Привет админ'
    title = 'Админпанель'
    return render_template('admin/index.html', page_title=title)
