import unittest
import zhiliao
class Testzhiliao(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLogin(self):
        self.assertEqual("kelly", zhiliao.login(username='kelly'))
        self.assertFalse('000',zhiliao.login(password='123'))

    def testRigester(self):
        self.assertFalse('kally',zhiliao.register(username='User.kelly'))
        self.assertTrue(zhiliao.register(password1='User.123'),'123')
        self.assertFalse(zhiliao.register(password2='User.123'), '321')
        self.assertNotEqual(zhiliao.register(password1='password2'))
if __name__ =='__main__':
    unittest.main()
