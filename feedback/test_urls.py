from django.test import TestCase
from django.core.urlresolvers import resolve

from dictionary.views import search


class DictionaryURLs(TestCase):
    def test_root_url_resolves_to_search_view(self):
        '''
        '/' should be routed to the search function
        in 'views.py'
        '''
        found = resolve('/')
        self.assertEqual(found.func, search)
            
     def test_search_url_resolves_to_search_view(self):
        '''
        '/search/' should be routed to the search function
        in 'views.py'
        '''
        found = resolve('/search/')
        self.assertEqual(found.func, search)
