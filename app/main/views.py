from flask import Blueprint, render_template
from flask_login import (
    current_user,
    login_required
)
from app.models import EditableHTML, Product, Task

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    products = Product.query.all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    list_of_raffle = len(products)
    return render_template('main/index.html',products=products, tasks=tasks, list_of_raffle=list_of_raffle)



@main.route('/tasks')
@login_required
def tasks():
    return render_template('main/tasks.html')

@main.route('/proxies')
@login_required
def proxies():
    return render_template('main/proxies.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
