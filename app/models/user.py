from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils import is_license_valid
from .. import db, login_manager

from app.models.util import Settings

import json
class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name

class User(UserMixin, db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    key = db.Column(db.String(), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    proxies = db.Column(db.String)

    last_active = db.Column(db.DateTime())
    settings = db.Column(db.String())

    # Relational
    tasks = db.relationship('Task', backref='by')
    profiles = db.relationship('Profile', backref='owner')

    account_settings = Settings()
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        
    def add_proxies_bulk(self, name, proxies):
        json_data = json.loads(self.proxies)
        json_data.append({
            'name':name,
            'proxies':proxies,
            'total':1
        })

        self.proxies = json.dumps(json_data)
        db.session.commit()

    def get_proxies(self):
        return json.loads(self.proxies)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def get_settings(self):
        if self.settings is None:
            self.settings = self.account_settings.to_json()
            db.session.commit()
        return self.settings

    def set_settings(self, data_dictionary):
        self.account_settings.set_settings(data_dictionary)

        self.settings = self.account_settings.to_json()
        db.session.commit()
        return True
    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_key(self):
        return is_license_valid(self.key)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""

        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        """Verify the new email for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""

        print("Generating User Fake Data to DB")

        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()

        seed()
        for i in range(count):
            u = User(
                username=fake.first_name(),
                email=fake.email(),
                password='password',
                confirmed=True,
                role=choice(roles),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def get_username(self):
        return '%s' % (self.username)

    def __repr__(self):
        return '<User %s>' % self.get_username()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_size = db.Column(db.String(10))
    status = db.Column(db.String(), default='Unstarted')
    entries = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    @staticmethod
    def generate_fake(count=15, **kwargs):
        """Generate a number of fake Tasks for testing."""
        
        print("Generating Task Fake Data to DB")

        sizes = ["US 3","US 4","US 5","US 6","US 7","US 8","US 9"]

        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()

        seed()
        for i in range(count):

            u = User.query.get(choice([1,2,3,4,5,6,7,8,9]))
            p = Product.query.get(choice([1,2,3,4,5,6,7,8,9]))
            t = Task(
                selected_size = choice(sizes),
                entries = choice([1,2,3,4,5,6,7,8,9,10]),
                by=u,
                product=p,
                **kwargs)
            db.session.add(t)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sizes = db.Column(db.String())
    thumbnail = db.Column(db.String())

    active_task = db.relationship('Task', backref='product')

    @staticmethod
    def generate_fake(count=15, **kwargs):
        """Generate a number of fake product for testing."""

        print("Generating Product Fake Data to DB")


        shoes_names = ["Adidas",
                        "Anta",
                        "ASICS",
                        "Babolat",
                        "Brooks",
                        "Converse",
                        "DC",
                        "Diadora",
                        "Dunlop",
                        "Ethletic",
                        "Feiyue",
                        "Fila",
                        "Hoka One One"
                        ]

        thumbnails = [
            "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_2000,h_2000/global/371777/01/sv01/fnd/PNA/fmt/png/Rise-Women's-Sneakers",
            "https://wwws.dior.com/couture/ecommerce/media/catalog/product/cache/1/zoom_image_2/3000x2000/17f82f742ffe127f42dca9de82fb58b1/u/j/1554385504_3SH118YJP_H069_E02_ZH.jpg",
            "https://bobobobo-s3.dexecure.net/5dd8eac362f58.jpg",
            "https://cdn.shopify.com/s/files/1/0238/2821/products/Womens-193-Royale-Blanco-3RMW-Product-102.jpg?v=1563992609"
        ]
        
        sizes = ["US 3","US 4","US 5","US 6","US 7","US 8","US 9"]

        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()

        seed()
        for i in range(count):
            u = Product(
                name = choice(shoes_names),
                thumbnail = choice(thumbnails),
                sizes = str(sizes),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def __repr__(self):
        return '<Product %s>' % self.name
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    
    country = db.Column(db.String(15))
    province = db.Column(db.String(20))
    city = db.Column(db.String(20))
    zipcode = db.Column(db.String(10))
    address = db.Column(db.String())

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
