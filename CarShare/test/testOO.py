import unittest
import zhiliao

class Testzhiliao(unittest.TestCase):
    def __init__(self):

    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testLogin(self):
        self.assertEqual("kelly", username = ('username'))
        self.assertFalse('000', password = request.form.get('password'))
    def testRigester(self):
        self.assertFalse('kally',zhiliao.register(username='User.kelly'))
        self.assertTrue(zhiliao.register(password1='User.123'),'123')
        self.assertFalse(zhiliao.register(password2='User.123'), '321')
        self.assertNotEqual(zhiliao.register(password1='password2'))
    def testCar_rental(self):
        self.assertTrue()


if __name__=='__main__':
    unittest.main()