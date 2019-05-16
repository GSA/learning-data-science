from os import path
import sys
import unittest
from unittest.mock import patch, Mock

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from main import get_ints_from_resource, main

class MainCase(unittest.TestCase):

    def setUp(self):
        #add fixtures here
        pass

    def tearDown(self):
        #add fixture(s) here
        pass

    def test_get_ints_from_resource(self):
        #write unit test here
        pass

    def test_main(self):
        #write unit test here
        pass
    