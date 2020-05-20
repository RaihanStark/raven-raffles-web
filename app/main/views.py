from flask import Blueprint, render_template, redirect, url_for
from flask_login import (
    current_user,
    login_required
)

from app.account.forms import AddBulkProxyForm
from app.models import EditableHTML, Product, Task, User

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

@main.route('/proxies',methods=['GET'])
@login_required
def proxies():
    proxies = current_user.get_proxies()
    form = AddBulkProxyForm()

    return render_template('main/proxies.html',proxies=proxies, form=form)

@main.route('/proxies/add',methods=['POST'])
@login_required
def proxies_add():
    proxies = current_user.get_proxies()
    
    form = AddBulkProxyForm()
    if form.validate_on_submit():
        current_user.add_proxies_bulk(form.name.data,form.proxies.data)
        return redirect(url_for('main.proxies'))
    return render_template('main/proxies.html',proxies=proxies, form=form)

@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
