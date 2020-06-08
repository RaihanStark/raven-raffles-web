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


raffles = Blueprint('raffles', __name__)

@raffles.route('/')
def index():
    return {'msg':'success'}