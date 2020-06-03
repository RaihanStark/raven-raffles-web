import time
import unittest
import json

from app import create_app, db
from app.models import AnonymousUser, Permission, Role, User, Profile


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='password')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='password')
        with self.assertRaises(AttributeError):
            u.password()

    def test_password_verification(self):
        u = User(password='password')
        self.assertTrue(u.verify_password('password'))
        self.assertFalse(u.verify_password('notpassword'))

    def test_password_salts_are_random(self):
        u = User(password='password')
        u2 = User(password='password')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='password')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm_account(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='password')
        u2 = User(password='notpassword')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm_account(token))

    def test_expired_confirmation_token(self):
        u = User(password='password')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm_account(token))

    def test_valid_reset_token(self):
        u = User(password='password')
        db.session.add(u)
        db.session.commit()
        token = u.generate_password_reset_token()
        self.assertTrue(u.reset_password(token, 'notpassword'))
        self.assertTrue(u.verify_password('notpassword'))

    def test_invalid_reset_token(self):
        u1 = User(password='password')
        u2 = User(password='notpassword')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_password_reset_token()
        self.assertFalse(u2.reset_password(token, 'notnotpassword'))
        self.assertTrue(u2.verify_password('notpassword'))

    def test_valid_email_change_token(self):
        u = User(email='user@example.com', password='password')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('otheruser@example.org')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'otheruser@example.org')

    def test_invalid_email_change_token(self):
        u1 = User(email='user@example.com', password='password')
        u2 = User(email='otheruser@example.org', password='notpassword')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token('otherotheruser@example.net')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'otheruser@example.org')

    def test_duplicate_email_change_token(self):
        u1 = User(email='user@example.com', password='password')
        u2 = User(email='otheruser@example.org', password='notpassword')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('user@example.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'otheruser@example.org')

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='user@example.com', password='password')
        self.assertTrue(u.can(Permission.GENERAL))
        self.assertFalse(u.can(Permission.ADMINISTER))

    def test_make_administrator(self):
        Role.insert_roles()
        u = User(email='user@example.com', password='password')
        self.assertFalse(u.can(Permission.ADMINISTER))
        u.role = Role.query.filter_by(
            permissions=Permission.ADMINISTER).first()
        self.assertTrue(u.can(Permission.ADMINISTER))

    def test_administrator(self):
        Role.insert_roles()
        r = Role.query.filter_by(permissions=Permission.ADMINISTER).first()
        u = User(email='user@example.com', password='password', role=r)
        self.assertTrue(u.can(Permission.ADMINISTER))
        self.assertTrue(u.can(Permission.GENERAL))
        self.assertTrue(u.is_admin())

    def test_anonymous(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.GENERAL))

    def test_valid_verify_key(self):
        u = User(key="RAVEN-89VM2F38JCEZ6L8KKADA121638")
        self.assertTrue(u.verify_key())

    def test_invalid_verify_key(self):
        u = User(key="invalid-key")
        self.assertFalse(u.verify_key())

    def test_get_empty_proxies(self):
        u = User()
        self.assertEqual([],u.get_proxies())

    def test_get_valid_proxies(self):
        u = User()
        u.add_proxies_bulk('test', '0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443')
        self.assertEqual([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        }],u.get_proxies())

    def test_add_bulk_empty_proxies(self):
        u = User()
        u.add_proxies_bulk('test', '0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443')
        self.assertEqual([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        }],u.get_proxies())

    def test_add_bulk_exist_proxies(self):
        u = User(proxies=json.dumps([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        }]))
        u.add_proxies_bulk('test2', '0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443')
        self.assertEqual([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        },{
            'name':'test2',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        }],u.get_proxies())
    
    def test_add_bulk_exist_same_name_proxies(self):
        u = User(proxies=json.dumps([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        }]))
        u.add_proxies_bulk('test', '0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443')
        self.assertEqual([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        },{
            'name':'test(1)',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n0.0.0.0:443",
            'total':3
        }],u.get_proxies())

    def test_add_one_proxy_to_group(self):
        u = User(proxies=json.dumps([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443",
            'total':2
        }]))
        u.add_proxies('test', '1.1.1.1:443')
        self.assertEqual([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n1.1.1.1:443",
            'total':3
        }],u.get_proxies())

    def test_delete_one_group_proxies(self):
        u = User(proxies=json.dumps([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443",
            'total':2
        }]))
        u.delete_proxy_by_name('test')
        self.assertEqual([],u.get_proxies())
    
    def test_filter_empty_proxies(self):
        u = User(proxies=json.dumps([]))
        u.add_proxies_bulk('USA', '0.0.0.0\r\n0.0.0.0\r\n\r\n\r\n\r\n')
        self.assertEqual([{
            'name':'USA',
            'proxies':"0.0.0.0\n0.0.0.0",
            'total':2
        }],u.get_proxies())
    
    def test_update_old_proxy(self):
        u = User(proxies=json.dumps([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443",
            'total':2
        }]))
        u.edit_proxies('test','test',"0.0.0.0:443\n0.0.0.0:443\n1.1.1.1:443")
        self.assertEqual([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n1.1.1.1:443",
            'total':3
        }],u.get_proxies())
    
    def test_update_name_old_proxy(self):
        u = User(proxies=json.dumps([{
            'name':'test',
            'proxies':"0.0.0.0:443\n0.0.0.0:443",
            'total':2
        }]))
        u.edit_proxies('test','test2',"0.0.0.0:443\n0.0.0.0:443\n1.1.1.1:443")
        self.assertEqual([{
            'name':'test2',
            'proxies':"0.0.0.0:443\n0.0.0.0:443\n1.1.1.1:443",
            'total':3
        }],u.get_proxies())

    def test_create_new_profile_success(self):
        u = User()
        Profile.create(name="test1", owner=u)

        self.assertEqual("test1",u.profiles[0].name)

    def test_delete_profile(self):
        u = User()
        Profile.create(name="test1", owner=u)

        u.delete_profile_by_id(1)
        self.assertEqual(
            0,len(u.profiles)
        )
    
    def test_delete_uncreated_profile(self):
        u = User()

        self.assertFalse(u.delete_profile_by_id(99))
        
    def test_change_profile(self):
        u = User()
        Profile.create(name="test1", owner=u)
        u.profiles[0].change_data(name='test2')
        self.assertEqual("test2",u.profiles[0].name)