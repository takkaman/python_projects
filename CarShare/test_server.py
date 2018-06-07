import unittest
from zhiliao import login, app
from zhiliao import *
import flask
from flask import json
from modules import *

class Testmain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass
    def test_incorrect_booking(self):
        result =self.app.post('/booking/', data=dict(name="316i", price="145",brand="BMW",bluetooth="bluetooth",seat="5",vehicleType="economic",username="mary",kilometer="150000"),
                               follow_redirects=True)
        self.assertEqual(result.status_code,200 )
    def test_correct_booking(self):
        result = self.app.post('/booking/', data=dict(name="316i", price="145",brand="BMW",bluetooth="bluetooth",seat="5",vehicleType="luxury",username="mary",kilometer="150000"),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    # test whether config data was set up successful
    def testConfig(self):
        self.assertFalse(app.config['SQLALCHEMY_DATABASE_URI'] is '12345')
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)

    def test_incorrect_history(self):

        result = self.app.post('/tables/', data=dict(name="BMW", price="123", password2="1234567899"),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)

# ensure that flask was set up correctly, the reason of returning 302 is redirect(if no login).
    def test_index_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 302)

    # test return information if username or password are invalid
    def test_incorrect_login(self):
        result = self.app.post('/login/', data=dict(username="Mary", password="888"), follow_redirects=True)
        self.assertIn('wrong username or password,please try again', result.data)
    def test_incorrect_login0(self):
        result = self.app.post('/login/', data=dict(username="Ma", password="123"), follow_redirects=True)
        self.assertIn('wrong username or password,please try again', result.data)
    def test_incorrect_login1(self):
        result = self.app.post('/login/', data=dict(username="Ma", password="123"), follow_redirects=True)
        self.assertIn('wrong username or password,please try again', result.data)
    # test login status when login successful
    def test_correct_login(self):
        result = self.app.post('/login/', data=dict(username="leo", password="leo"), follow_redirects=True)
        self.assertEqual(result.status_code, 200)

#Return 302 means redirect to main index if logout successful
    def test_logout(self):
        result = self.app.get('/logout/')
        self.assertEqual(result.status_code, 302)

# test return information if username or password are invalid
    def test_incorrect_register(self):
        result = self.app.post('/register/', data=dict(username="mary", password1="888", password2="999"),
                               follow_redirects=True)
        self.assertIn('different passwords,please try again!', result.data)

    def test_incorrect_register0(self):
        result = self.app.post('/register/', data=dict(username="marey", password1="111", password2="000"),
                               follow_redirects=True)
        self.assertIn('different passwords,please try again!', result.data)


    def test_incorrect_register1(self):
        result = self.app.post('/register/', data=dict(username="marey", password1="111", password2="123899"),
                               follow_redirects=True)
        self.assertIn('different passwords,please try again!', result.data)

    # test regiter status when successful
    # def test_correct_register(self):
    #     result = self.app.post('/register/', data=dict(username="marey", password1="123", password2="123"),
    #                            follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     user = User.query.filter_by(username="marey").first()
    #     db.session.delete(user)
    #     db.session.commit()

    # return car success, redirect to booking 302
    def test_incorrct_return(self):
        result = self.app.post('/return/car/', data=dict(name="BMW_325i_Aut."))
        self.assertEqual(result.status_code, 302)


if __name__ == '__main__':
    unittest.main()
