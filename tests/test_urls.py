from django.test import TestCase
from django.core.urlresolvers import resolve

from feedback.views import index, GeneralFeedbackCreate, missingsign

class FeedbackURLs(TestCase):
    
    def test_root_url_resolves_to_index_view(self):
        '''
        '/' should be routed to the index function
        in views.py
        '''
        found = resolve('/')
        self.assertEqual(found.func, index)
         
    def test_general_feedback_url_resolves_to_general_feedback_view(self):
        '''
        '/generalfeedback/' should be routed to the GeneralFeedbackCreate
        class in views.py
        '''
        found = resolve('/generalfeedback/')
        self.assertEqual(found.func.__name__, GeneralFeedbackCreate.__name__)
  
    def test_missing_sign_url_resolves_to_missing_sign_view(self):
        '''
        '/missingsign/' should be routed to the missingsign function
        in views.py
        '''
        found = resolve('/missingsign/')
        self.assertEqual(found.func, missingsign) 
