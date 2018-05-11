import unittest
from zhiliao import login,app
import zhiliao

class Testzhiliao(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass


    def test_login(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 302)

if __name__ =='__main__':
    unittest.main()
