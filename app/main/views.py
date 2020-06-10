from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import (
    current_user,
    login_required
)

from app.account.forms import AddBulkProxyForm, AddProxyForm, EditProxyForm, AddNewProfilesForm
from app.main.forms import CreateTaskForm
from app.models import EditableHTML, Product, Task, User, Profile

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    products = Product.query.all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    list_of_raffle = len(products)

    form = CreateTaskForm()
    return render_template('main/index.html',products=products, tasks=tasks, list_of_raffle=list_of_raffle, form=form)



@main.route('/tasks')
@login_required
def tasks():
    products = Product.query.all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    form = CreateTaskForm()
    return render_template('main/tasks.html',products=products, tasks=tasks, form=form)

@main.route('/tasks/add', methods=['POST'])
@login_required
def tasks_add():
    form = CreateTaskForm()
    flash('Task Added')
    return redirect(url_for('main.tasks'))

@main.route('/profiles')
@login_required
def profiles():
    form = AddNewProfilesForm()
    return render_template('main/profiles.html', form=form, profiles=current_user.profiles)

@main.route('/profiles/add',methods=['POST'])
@login_required
def add_profiles():
    form = AddNewProfilesForm()

    Profile.create(
        name = form.profile_name.data,
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        country = form.country.data,
        province = form.province.data,
        city = form.city.data,
        zipcode = form.zip_code.data,
        address = form.address.data,
        email = form.email.data,
        owner=current_user
    )

    # print(current_user.profiles)
    # form = AddNewProfilesForm()
    return redirect(url_for('main.profiles'))

@main.route('/profiles/delete',methods=['DELETE'])
@login_required
def profile_delete():
    current_user.delete_profile_by_id(request.form['id'])
    return {'msg':'deleted'},200

@main.route('/profiles/edit_profiles/<name>', methods=['GET', 'POST'])
@login_required
def edit_profiles(name):
    # proxies = current_user.get_proxies()
    # # Find Proxy
    # found = [found_proxy for found_proxy in proxies if found_proxy['name'] == name]
    # if len(found) >= 1:

        
    #     form = EditProxyForm()
    #     if form.validate_on_submit():
    #         current_user.edit_proxies(found[0]['name'],form.name.data, form.proxies.data)
    #         return render_template('main/edit_proxies.html',form=form, currentproxy=found[0])  
    #     form.proxies.data = found[0]['proxies']
    #     return render_template('main/edit_proxies.html',form=form, currentproxy=found[0])  
    # return redirect(url_for('main.proxies'))

    profiles = current_user.profiles
    found = [found_profile for found_profile in profiles if found_profile.id == int(name)]
    if len(found) >= 1:
        form = AddNewProfilesForm()
        if form.validate_on_submit():
            found[0].change_data(
                name = form.profile_name.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                country = form.country.data,
                province = form.province.data,
                city = form.city.data,
                zipcode = form.zip_code.data,
                address = form.address.data,
                email = form.email.data
            )
        return render_template('main/edit_profiles.html', form=form, current_profile=found[0])
    return redirect(url_for('main.profiles'))

@main.route('/proxies',methods=['GET'])
@login_required
def proxies():
    proxies = current_user.get_proxies()
    form = AddBulkProxyForm()

    form2 = AddProxyForm()
    print(proxies)
    form2.name_group.choices = [(i['name'], i['name']) for i in proxies]
    return render_template('main/proxies.html',proxies=proxies, form=form, form2=form2)

@main.route('/proxies/add',methods=['POST'])
@login_required
def proxies_add():
    proxies = current_user.get_proxies()

    if request.form['type-form'] == 'add':
        form2 = AddProxyForm()

        current_user.add_proxies(form2.name_group.data,form2.proxies.data)

        return redirect(url_for('main.proxies'))
    elif request.form['type-form'] == 'add_bulk':
        form = AddBulkProxyForm()

        current_user.add_proxies_bulk(form.name.data,form.proxies.data)

        return redirect(url_for('main.proxies'))
    
    return redirect(url_for('main.proxies'))

@main.route('/proxies/edit_proxies/<name>', methods=['GET', 'POST'])
@login_required
def edit_proxies(name):
    proxies = current_user.get_proxies()
    # Find Proxy
    found = [found_proxy for found_proxy in proxies if found_proxy['name'] == name]
    if len(found) >= 1:

        
        form = EditProxyForm()
        if form.validate_on_submit():
            current_user.edit_proxies(found[0]['name'],form.name.data, form.proxies.data)
            return render_template('main/edit_proxies.html',form=form, currentproxy=found[0])  
        form.proxies.data = found[0]['proxies']
        return render_template('main/edit_proxies.html',form=form, currentproxy=found[0])  
    return redirect(url_for('main.proxies'))

@main.route('/proxies/delete',methods=['DELETE'])
@login_required
def proxies_delete():
    current_user.delete_proxy_by_name(request.form['name'])
    return {'msg':'deleted'},200


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
