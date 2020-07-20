from flask import url_for
from wtforms.fields import Field
from wtforms.widgets import HiddenInput
from wtforms.compat import text_type
from flask_login import (
    current_user,
    login_required
)
from config import Config
import requests
import json

from discord_webhook import DiscordWebhook,  DiscordEmbed


def register_template_utils(app):
    """Register Jinja 2 helpers (called from __init__.py)."""

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    app.add_template_global(index_for_role)


def index_for_role(role):
    return url_for(role.index)


def is_license_valid(key):
    """Checking License Key from External API

    Args:
        key (str): Serial Key for Raven Restocks

    Returns:
        bool: If the key is valid
    """
    r = requests.post(
        'https://xserver.boxmarshall.com/api/v2/authorize/validate/no-device', json={"serialkey": key})
    return r.json()['success']


def is_anticaptcha_valid(key):
    """Getting anticaptcha balance

    Args:
        key (str): Client key for Anti-Captcha

    Returns:
        dict: Anticaptcha balance with status_code
    """
    r = requests.post('https://api.anti-captcha.com/getBalance',
                      json={'clientKey': key})

    return r.json()


def send_to_webhooks(url, data):
    """Send nontification to webhooks

    Args:
        url (str): Webhooks url
        data (dict): A dictionary of the products
            for example:
                data = {
                    'name': 'Yeezy Boost',
                    'size': 'US 10',
                    'profiles': 'Private Account',
                    'proxies': 'USA',
                    'entries': 10,
                    'status': 'Success'
                }

    Returns:
        bool: If message sucessfully sent
    """

    webhook = DiscordWebhook(url)

    embed = DiscordEmbed(title=Config.WEBHOOK_HEADER_TITLE,
                         description=':athletic_shoe: {}'.format(data['name']), color=0xC462DB)
    embed.set_author(name=Config.WEBHOOK_AUTHOR_NAME, url=Config.WEBHOOK_AUTHOR_URL,
                     icon_url=Config.WEBHOOK_AUTHOR_ICON_URL)
    embed.set_footer(text=Config.WEBHOOK_FOOTER_TEXT)
    embed.set_timestamp()
    embed.add_embed_field(name='Size', value=data['size'])
    embed.add_embed_field(name='Profiles', value=data['profiles'])
    embed.add_embed_field(name='Proxies ', value=data['proxies'])
    embed.add_embed_field(name='Entries', value=data['entries'])
    embed.add_embed_field(
        name='Status', value=':zap: {}'.format(data['status']))
    embed.set_thumbnail(
        url='https://avatars0.githubusercontent.com/u/14542790')
    embed.set_image(url='https://avatars0.githubusercontent.com/u/14542790')
    webhook.add_embed(embed)
    response = webhook.execute()
    if response.status_code == 401:
        return False
    return True


def format_cc_to_json(number, exp, cvv):
    """Formatting seperate cc information into one json value

    Args:
        number (str): Credit Card Number
        exp (str): Expiration Date (MM/YYYY)
        cvv (str): CVV

    Returns:
        json: Returns formatted cc information.
            for example:
                credit_card = {
                    'number':"4444444444",
                    'exp_year':"2024",
                    'exp_month':"03",
                    'cvv':"123"
                }

    """
    credit_card = {
        'number': number.replace(' ', ''),
        'exp_year': exp.split('/')[1],
        'exp_month': exp.split('/')[0],
        'cvv': cvv
    }
    return json.dumps(credit_card)


def get_proxy_by_name(name):
    """Get current user's selected proxy"""
    return [i for i in current_user.get_proxies() if i['name'] == name]


class CustomSelectField(Field):
    widget = HiddenInput()

    def __init__(self, label='', validators=None, multiple=False,
                 choices=[], allow_custom=True, **kwargs):
        super(CustomSelectField, self).__init__(label, validators, **kwargs)
        self.multiple = multiple
        self.choices = choices
        self.allow_custom = allow_custom

    def _value(self):
        return text_type(self.data) if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[1]
            self.raw_data = [valuelist[1]]
        else:
            self.data = ''
