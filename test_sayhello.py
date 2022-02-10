from ast import Pass
import unittest
from module_foo import sayhello
class SayHelloTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_sayhello(self):
        rv = sayhello()
        self.assertEqual(rv, 'hello!')
    
    def test_sayhello_to_somebody(self):
        rv = sayhello(to='Grey')
        self.assertEqual(rv, 'hello, Grey!')

if __name__== '__main__':
    unittest.main()
