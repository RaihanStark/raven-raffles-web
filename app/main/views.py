from flask import Blueprint, render_template
from flask_login import (
    current_user,
    login_required
)
from app.models import EditableHTML

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('main/index.html')



@main.route('/tasks')
@login_required
def tasks():
    return render_template('main/tasks.html')




@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
