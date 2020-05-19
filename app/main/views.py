from flask import Blueprint, render_template
from flask_login import (
    current_user,
    login_required
)
from app.models import EditableHTML, Product

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    products = Product.query.all()
    print(products)
    return render_template('main/index.html',products=products)



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
