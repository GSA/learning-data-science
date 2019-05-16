import unittest
import sys
import inspect
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from divide import divide

class DivideCase(unittest.TestCase):

    def setUp(self):
        '''
        Called once before each test
        '''
        self.log_point()
        self.int_x = 1
        self.int_y = 2
        self.zero = 0
        self.float_x = 1.0
        self.float_y = 2.0
        self.str_x = '1'
        self.str_y = '2'
        
    def tearDown(self):
        '''
        Called once after each test
        '''
        self.log_point() 
        self.int_x = None
        self.int_y = None
        self.zero = None
        self.float_x = None
        self.float_y = None
        self.str_x = None
        self.str_y = None
        

    def test_divide_int_args(self):
        '''
        Test with int args
        '''
        self.log_point() 
        result = divide(self.int_x, self.int_y)
        expected = .5
        self.assertEqual(result, expected)

    def test_divide_float_args(self):
        '''
        Test with float args
        '''
        self.log_point() 
        result = divide(self.float_x, self.float_y)
        expected = .5
        self.assertEqual(result, expected)

    def test_divide_int_float_args(self):
        '''
        Test with float and int args
        '''
        self.log_point() 
        result = divide(self.int_x, self.float_y)
        expected = .5
        self.assertEqual(result, expected)

    def test_divide_str_args(self):
        '''
        Test with str args
        '''
        self.log_point() 
        result = divide(self.str_x, self.str_y)
        expected = 0
        self.assertEqual(result, expected)

    def test_divide_by_zero(self):
        '''
        Test divide by zero
        '''
        self.log_point() 
        result = divide(self.int_x, self.zero)
        expected = 0
        self.assertEqual(result, expected)

    def log_point(self):
        '''
        A utility method using the inspect module to demonstrate the control flow through the tests.
        '''
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))