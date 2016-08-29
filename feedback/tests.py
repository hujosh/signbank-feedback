import datetime

from django.test import TestCase, override_settings, RequestFactory
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.conf import settings 
from django.urls import reverse_lazy
from django.shortcuts import render

from .views import index, GeneralFeedbackCreate, missingsign
from .models import GeneralFeedback


# Instead of using the urls.py file in signbank
# as the base urls.py, use the urls.py in feedback 
#@override_settings(ROOT_URLCONF="feedback.urls")
class IndexPage(TestCase):
    '''
    The tests in here test for the correctness of 
    'index view'
    '''
    def setUp(self):
        self.factory = RequestFactory()
        self.url = "/feedback/"
    
    def test_root_url_resolves_to_index_view(self):
        '''
        '/' should be routed to the index function
        in views.py
        '''
        found = resolve(self.url)
        self.assertEqual(found.func, index)
   
    def test_uses_index_template(self):
        '''
        'The index' view should render the 'feedback/index.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/index.html'):
            response = index(request)
          
    def test_right_sign_language_is_rendered(self):
        '''
        The sign language rendered in the template
        'feedback/index.html' should equal the 
        'LANGUAGE_NAME' variable in 'settings.py'.
        '''
        LANGUAGE_NAME = settings.LANGUAGE_NAME
        response = self.client.get(self.url)
        self.assertContains(response, LANGUAGE_NAME)
                
    def test_resonse_code_is_200(self):
        '''The response code reutrned by 'index()'
        should be 200.
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        
#@override_settings(ROOT_URLCONF="feedback.urls")
class GenerealFeedback(TestCase):
    '''The tests in here check for the
       correctness of the general feedback view.
    '''
    def setUp(self):
        self.url = "/feedback/generalfeedback/"
        self.data = {"comment": "This is a comment"}
    
    def test_general_feedback_form_url_resolves_to_generalfeedback_view(self):
        '''
        'generalfeedback/' should be routed to the GeneralFeedbackCreate
        class in views.py
        '''
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, GeneralFeedbackCreate.__name__)

    def test_generalfeedback_form_template_used(self):
        '''
        'GeneralFeedbackCreate()' should render the 
        'feedback/generalfeedback_form.html' template
        '''
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "feedback/generalfeedback_form.html")
        
    def test_response_code_200_returned_by_GeneralFeeedbackCreate(self):
        '''
        The response code reutrned by 'GenerealFeedbackCreate'
        should be 200.
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_success_message_displayed_when_form_submitted_successfully(self):
        '''A success message should be displayed when form data
           is submitted correctly. 
        '''   
        response = self.client.post(self.url, self.data, follow = True)
        self.assertContains(response, GeneralFeedbackCreate.success_message)
                
    def test_redirect_occurrs_after_successful_submission_of_form(self):
        '''
        A successful form submission should trigger a rediect.
        '''
        response = self.client.post(self.url, self.data, follow = True)
        self.assertRedirects(response, reverse_lazy("feedback:generalfeedback"))
    
    def test_an_error_is_displayed_if_no_comment_is_submitted(self):
        '''
        Not submitting a comment should display an error.
        '''
        response = self.client.post(self.url)
        self.assertFormError(response, 'form', 'comment', 'This field is required.')
        
    def test_feedback_saved_to_database(self):
        '''
        Feedback should be saved to the database
        after being submitted.
        '''
        response = self.client.post(self.url, self.data)
        # Now let's make sure that the name and feedback are in the database                                                           
        feedback = GeneralFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a date 
        self.assertIsInstance(feedback[0].date, datetime.date)
        self.assertEqual(feedback[0].date, datetime.date.today())
        # It should have a comment
        self.assertEqual(feedback[0].comment, self.data['comment'])
        

#@override_settings(ROOT_URLCONF="feedback.urls")                
class MissingSignFeedback(TestCase):
    '''
    The tests in here test for the correctness of the 
    missing sign feedback view.
    '''
    def setUp(self):
        self.url = "/feedback/missingsign/"

    def test_missing_sign_url_resolves_to_missing_sign_view(self):
        '''
        '/missingsign/' should be routed to the missingsign function
        in views.py
        '''
        found = resolve(self.url)
        self.assertEqual(found.func, missingsign)     
        
    def test_uses_missing_sign_form_template(self):
        '''
        'missingsign()' should render the 'feedback/missingsign_form.html'
        template
        '''
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "feedback/missingsign_form.html")
           
    def test_response_code_200_returned_by_missingsign_for_get(self):
        '''
        The response code reutrned by 'missingsign()'
        should be 200 for get requests.
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
   
