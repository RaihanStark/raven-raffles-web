from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    IntegerField,
    SelectField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from flask_login import (
    current_user,
    login_required
)

from app import db
from app.models import Profile

class CreateTaskForm(FlaskForm):
    raffle_id = StringField('raffle id',validators=[InputRequired()])
    size = SelectField('size', validators=[InputRequired()],coerce=str,choices=[("default","Select Size")])
    entries = IntegerField('entries',validators=[InputRequired()])
    profiles = QuerySelectField(
        'profiles',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Profile).filter_by(owner_id=current_user.id).all()
        )
    cc_number = StringField('Credit Card Number',validators=[InputRequired()])
    cc_exp = StringField('Credit Card Expired Date',validators=[InputRequired()])
    cc_cvv = StringField('Credit Card CVV',validators=[InputRequired()])
    submit = SubmitField('Proceed')
