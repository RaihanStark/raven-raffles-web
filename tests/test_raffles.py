import unittest

from app import create_app, db
from flask import current_app
from app.models import Role, User, Product, Task, Profile
from app.utils import send_to_webhooks
import json

from config import Config


class RafflesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_test = self.app.test_client()
        db.create_all()

    @classmethod
    def setUpClass(cls):
        Product.generate_fake(count=10)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_product_by_id(self):
        res = self.app_test.get('/raffles/products/1',
                                content_type='application/json')
        data = json.loads(res.get_data())
        self.assertEqual(1, data['id'])

    def test_get_product_by_id_error(self):
        res = self.app_test.get('/raffles/products/999',
                                content_type='application/json')
        data = json.loads(res.get_data())
        self.assertEqual(True, data['error'])

    def test_get_variant_product(self):
        p = Product(name="Adidas - Yeezy Boost 700")
        self.assertEqual(p.get_variant(), "Yeezy Boost 700")

    def test_send_to_webhook(self):
        data = {
            'name': 'Yeezy Boost',
            'size': 'US 10',
            'profiles': 'Private Account',
            'proxies': 'USA',
            'entries': 10,
            'status': 'Success'
        }
        r = send_to_webhooks(
            Config.WEBHOOK_TEST_URL, data)
        self.assertTrue(r)
