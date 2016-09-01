import datetime

from django.test import TestCase, RequestFactory
from django.conf import settings 
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse_lazy

from feedback.views import index, missingsign, GeneralFeedbackCreate
from feedback.models import GeneralFeedback


class IndexView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/' 
        
    def test_index_view_renders_right_template(self):
        '''
        'The index' view should render the 'feedback/index.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/index.html'):
            response = index(request) 
                        
    def test_index_view_returns_200_response_code(self):
        '''
        The response code reutrned by the index view
        should be 200.
        '''
        request = self.factory.get(self.url)
        response = index(request)
        self.assertEqual(response.status_code, 200)
                        
    def test_right_sign_language_is_rendered(self):
        '''
        The sign language rendered in the template
        'feedback/index.html' should equal the 
        'LANGUAGE_NAME' variable in 'settings.py'.
        '''
        LANGUAGE_NAME = settings.LANGUAGE_NAME
        request = self.factory.get(self.url)
        response = index(request)
        self.assertContains(response, LANGUAGE_NAME)
        
        
class GeneralFeedbackView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # The url is irrelevant for when RequestFactory is used...
        self.url = "/generalfeedback/"
        self.data = {"comment": "This is a comment"}
        
    def test_general_feedback_view_renders_right_template_for_get_request(self):
        '''
        The general feedback view should render
        'feedback/generalfeedback_form.html' for get requests. 
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/generalfeedback_form.html'):
            response = GeneralFeedbackCreate.as_view()(request)
            response.render()
                            
    def test_general_feedback_view_returns_200_response_for_get_request(self):
        '''
        The response code reutrned by the general feedback view
        should be 200 for a get.
        '''
        request = self.factory.get(self.url)
        response = GeneralFeedbackCreate.as_view()(request) 
        self.assertEqual(response.status_code, 200)
        
    def test_general_feedback_view_redirects_after_successful_post_request(self):
        '''
        The genreal feedback view should redirect back to itself
        after a successful post.
        '''
        request = self.factory.post(self.url, self.data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)      
        response = GeneralFeedbackCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (self.url))
           
    def test_error_is_displayed_if_no_comment_is_submitted(self):
        '''
        Not submitting a comment should render an error.
        '''
        request = self.factory.post(self.url)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = GeneralFeedbackCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)     
        self.assertContains(response, 'This field is required')                

    def test_general_feedback_view_saves_to_database(self):
        '''
        The general feedback view should save
        feedback to database after being submitted.
        '''
        request = self.factory.post(self.url, self.data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = GeneralFeedbackCreate.as_view()(request)
        # Now let's make sure that the feedback is in the database                                                           
        feedback = GeneralFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a date 
        self.assertIsInstance(feedback[0].date, datetime.date)
        self.assertEqual(feedback[0].date, datetime.date.today())
        # It should have a comment
        self.assertEqual(feedback[0].comment, self.data['comment'])
        
        
class MissingSignView(TestCase):
     def setUp(self):
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/missingsign/' 
        self.data = {"meaning": "This is meaning", 
            "comment" : "This is a comment"}
    
     def test_missing_sign_view_renders_right_template(self):
        '''
        The missing sign view should render the 'feedback/missingsign_form.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/missingsign_form.html'):
            response = missingsign(request) 
     
     def test_missing_sign_view_returns_200_response_code_for_get_request(self):
        '''
        The response code reutrned by the missing sign view
        should be 200 for get requests.
        '''
        request = self.factory.get(self.url)
        response = missingsign(request) 
        self.assertEqual(response.status_code, 200)
                   
     

   
        
 
    
