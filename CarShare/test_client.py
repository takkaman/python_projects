import unittest
import time
from flask import abort, url_for
import urllib2
from flask_testing import TestCase, LiveServerTestCase
from selenium import webdriver

from zhiliao import *
from modules import *

class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        app = create_app()
        # app.config.update(
        #     # Specify the test database
        #     # SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2016@localhost/dreamteam_test',
        #     # Change the port that the liveserver listens on
        #     LIVESERVER_PORT=8943
        # )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        self.driver = webdriver.Chrome("C:/Users/phyan/Downloads/chromedriver_win32/chromedriver.exe")

        # self.driver.quit()

    def tearDown(self):
        """
        Will be called after every test
        """
        self.driver.quit()
        # db.session.remove()
        # db.drop_all()



class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in Employee table
        """
        bf_add = User.query.count()
        user = User(username="test", password="test")
        db.session.add(user)
        db.session.commit()
        af_add = User.query.count()
        db.session.delete(user)
        db.session.commit()
        af_del = User.query.count()
        self.assertEqual(af_add - bf_add, 1)
        self.assertEqual(af_add - af_del, 1)

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen('http://127.0.0.1:5000/')
        self.assertEqual(response.code, 200)


    def test_register_user(self):
        self.driver.get('http://127.0.0.1:5000/')
        self.driver.find_element_by_name("register").click()
        bf_add = User.query.count()
        self.driver.find_element_by_name("username").send_keys("test1")
        self.driver.find_element_by_name("password1").send_keys("test1")
        self.driver.find_element_by_name("password2").send_keys("test1")
        self.driver.find_element_by_name("signup").click()
        time.sleep(5)
        db.session.commit()
        af_add = User.query.count()
        self.assertEqual(af_add - bf_add, 1)
        user = User.query.filter_by(username="test1").first()
        db.session.delete(user)
        time.sleep(5)
        db.session.commit()

    # test whether config data was set up successful
    def testConfig(self):
        self.assertFalse(app.config['SQLALCHEMY_DATABASE_URI'] is '12345')
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)



if __name__ == '__main__':
    unittest.main()