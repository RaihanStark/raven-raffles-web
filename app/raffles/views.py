from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from app.models import Product, Task

raffles = Blueprint('raffles', __name__)

@raffles.route('/products/<int:id>', methods=['GET'])
def index(id):
    try:
        selected_product = Product.query.filter_by(id=id).first()
        return {'id':selected_product.id,'name':selected_product.name,'size':selected_product.sizes}
    except:
        return {'error': True, 'msg':'Product not found'},404