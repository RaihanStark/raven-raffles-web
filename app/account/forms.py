from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    HiddenField,
    TextAreaField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.models import User


from app.utils import is_license_valid, is_anticaptcha_valid

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[InputRequired(),
                                  Length(1, 64)])
    key = StringField(
        'License Key', validators=[InputRequired()])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired()
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired(),EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        elif len(username.data) <= 6:
            raise ValidationError('Username must be at least 6 characters')

    def validate_key(self,key):
        if is_license_valid(key.data) == False or User.query.filter_by(key=key.data).first() is not None:
            raise ValidationError('Please use a different license.')

    def validate_password(self, password):
        if len(password.data) <= 6:
            raise ValidationError('Password must be at least 6 characters')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Reset password')

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Set password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Update password')


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class SettingsForm(FlaskForm):
    webhooks = StringField('Discord Webhooks')
    anticaptcha_key = StringField('AntiCaptcha Key')
    submit = SubmitField('Save settings')

    def validate_anticaptcha_key(self, anticaptcha_key):
        if anticaptcha_key.data != "":
            if is_anticaptcha_valid(anticaptcha_key.data)['errorId'] == True:
                raise ValidationError('Key is not Exist. Leave it blank if you don\'t have it')

class AddBulkProxyForm(FlaskForm):
    name = StringField('Name Group', validators=[InputRequired()])
    proxies = TextAreaField('List of Proxy', validators=[InputRequired()])
    submit = SubmitField('Save')