import unittest
import zhiliao

class Testzhiliao(unittest.TestCase):
   # def __init__(self):

    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testLogin(self):
        self.assertEqual("leo", username = ('leo'), password = ('leo'))
        self.assertFalse('000', password = ('password'))


if __name__ == '__main__':
      unittest.main()