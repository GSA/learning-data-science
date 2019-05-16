from os import path
import sys
import unittest
from unittest.mock import patch, Mock

import requests
import requests_mock

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from get_resource import get_resource, get_resource_by_date

class GetResourceCase(unittest.TestCase):
     
    @classmethod
    def setUpClass(cls):
        'called once, before any tests'
        cls.response_text = 'foo-baz-12'
        cls.uri = 'http://test.com'
        
    @classmethod
    def tearDownClass(cls):
        'called once, after all tests, if setUpClass successful'
        cls.response_text = None
        cls.uri = None

    @requests_mock.Mocker()
    def test_get_resource(self, mock_request):
        mock_request.register_uri('GET', 
                                  GetResourceCase.uri, 
                                  text = GetResourceCase.response_text)
        result = get_resource(GetResourceCase.uri)
        expected = GetResourceCase.response_text
        self.assertEqual(result, expected)

    @requests_mock.Mocker()
    def test_get_resource_exc(self, mock_request):
        '''
        Mock a connection error
        '''
        mock_request.register_uri('GET', 
                                  GetResourceCase.uri, 
                                  exc = requests.exceptions.ConnectTimeout)
        result = get_resource(GetResourceCase.uri)
        expected = None
        self.assertEqual(result, expected)

    # When you nest decorators, the parameters are passed in to the decorated function in the same order they're
    # applied. This means from the bottom up.
    @patch('get_resource.get_now')
    @requests_mock.Mocker()
    def test_get_resource_by_date_complete_qs(self, mocked_now, mock_request):
        '''
        Test response with complete query param by patching a func that calls datetime.now()
        '''
        now = '2019-05-16'
        mocked_now.return_value = now
        uri = f'{GetResourceCase.uri}?date={now}'
        mock_request.register_uri('GET', 
                                  uri, 
                                  text = GetResourceCase.response_text,
                                  complete_qs = True) #match only the complete query string; no partial/wildcard matches
        result = get_resource_by_date(GetResourceCase.uri)
        expected = GetResourceCase.response_text
        self.assertTrue(result, expected)

        
