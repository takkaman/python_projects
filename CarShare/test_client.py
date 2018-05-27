import unittest

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

        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # self.driver = webdriver.Chrome()
        # self.driver.get(self.get_server_url())
        pass

    def tearDown(self):
        """
        Will be called after every test
        """
        pass
        # db.session.remove()
        # db.drop_all()

    # def test_server_is_up_and_running(self):
    #     response = urllib2.urlopen(self.get_server_url())
    #     self.assertEqual(response.code, 200)

class TestModels(TestBase):

    def test_employee_model(self):
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

if __name__ == '__main__':
    unittest.main()