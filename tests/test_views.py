import datetime

from django.test import TestCase, RequestFactory
from django.conf import settings 
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse_lazy, reverse

from feedback.views import (index, missingsign, 
    GeneralFeedbackCreate, wordfeedback, showfeedback, delete)
from feedback.models import GeneralFeedback, MissingSignFeedback, SignFeedback


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
        # Now, let's make sure that the feedback is in the database                                                           
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
        self.data = {"meaning" : "10",
                    "comments" : "10"}
    
     def test_missing_sign_view_renders_right_template(self):
        '''
        The missing sign view should render the 'feedback/missingsign_form.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/missingsign_form.html'):
            response = missingsign(request) 
     
     def test_missing_sign_view_returns_200_response_code_for_a_get_request(self):
        '''
        The response code reutrned by the missing sign view
        should be 200 for a get request.
        '''
        request = self.factory.get(self.url)
        response = missingsign(request) 
        self.assertEqual(response.status_code, 200)
        
     def test_missing_sign_view_redirects_after_a_successful_post_request(self):
        '''
        The missign sign view should redirect back to itself after 
        receiving valid feedback.
        '''
        request = self.factory.post(self.url, self.data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = missingsign(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        
     def test_error_is_displayed_if_neither_comment_nor_meaning_is_submitted(self):
        '''
        Not submitting a comment should render an error on the form.
        '''
        request = self.factory.post(self.url)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = missingsign(request)
        self.assertContains(response, 'This field is required', count=2, status_code=200)    
        
     def test_missing_sign_view_saves_to_database(self):
        '''
        The missing sign view should save
        feedback to database after being submitted.
        '''
        request = self.factory.post(self.url, self.data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = missingsign(request)
        # Now, let's make sure that the feedback is in the database                                                           
        feedback = MissingSignFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a date 
        self.assertIsInstance(feedback[0].date, datetime.date)
        self.assertEqual(feedback[0].date, datetime.date.today())
        # It should have a comment
        self.assertEqual(feedback[0].comment, self.data['comment'])
        # It should have a meaning
        self.assertEqual(feedback[0].meaning, self.data['meaning'])      
        
        
class WordFeedback(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/word/liquid-1/' 
        self.data = {"correct" : "1", "use" : "1", "like" : "1", 
            "whereused" : "auswide", "isAuslan" : "1" }
        self.params = ['liquid', 1]
        
    def test_word_feedback_view_renders_right_template(self):
        '''
        The word feedback view should render the 'feedback/signfeedback_form.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/signfeedback_form.html'):
            response = wordfeedback(request, *self.params)
            
    def test_word_feedback_view_returns_200_response_code_for_a_get_request(self):
        '''
        The response code reutrned by the word feedback view
        should be 200 for a get request.
        '''
        request = self.factory.get(self.url)
        response = wordfeedback(request, *self.params) 
        self.assertEqual(response.status_code, 200)          
             
    def test_error_is_displayed_if_none_of_the_required_fields_are_submitted(self):
        '''
        Not submitting required fields should render an error on the form.
        '''
        request = self.factory.post(self.url)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = wordfeedback(request, *self.params)
        self.assertContains(response, 'This field is required', count=5, status_code=200)
       
    def test_word_feedback_view_redirects_after_successful_post_request(self):
        '''
        The word feedback view should redirect back to itself after
        the submission of valid feedback.
        '''
        request = self.factory.post(self.url, self.data)
        response = wordfeedback(request, *self.params) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)   
                 
    def test_word_feedback_view_saves_to_database(self):
        '''
        Feedback should be saved to the database if 
        it's valid.
        '''
        request = self.factory.post(self.url, self.data)
        response = wordfeedback(request, *self.params)       
        # Now, let's make sure that the feedback is in the database                                                           
        feedback = SignFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a date 
        self.assertIsInstance(feedback[0].date, datetime.date)
        self.assertEqual(feedback[0].date, datetime.date.today())
        self.assertEqual(feedback[0].correct, 1)
        self.assertEqual(feedback[0].use, 1)
        self.assertEqual(feedback[0].like, 1)
        self.assertEqual(feedback[0].whereused, "auswide")
        self.assertEqual(feedback[0].isAuslan, "1")
        
        
class ShowFeedbackView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/show/' 
        
    def test_show_view_renders_right_template(self):            
        '''
        The show feedback view should render the 'feedback/show.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/show.html'):
            response = showfeedback(request)
        
    def test_show_view_returns_200_response_code(self):
        '''
        The response code reutrned by the show  view
        should be 200 for a get request.
        '''
        request = self.factory.get(self.url)
        response = showfeedback(request) 
        self.assertEqual(response.status_code, 200)
        
    def test_general_feedback_is_viewable(self):
        '''
        If there is general feedback, it should be viewable.
        '''
        # Setup the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment)
        feedback.save()
        # Now, let's check whether 'showfeedback' renders it
        request = self.factory.get(self.url)
        response = showfeedback(request)
        self.assertContains(response, comment)
        
    def test_missing_sign_feedback_is_viewable(self):
        '''
        If there is missing sign feedback, it should be viewable.
        '''
        # Setup the missing sign feedback
        comments = "If you can read this, it is correct"
        meaning = "this too"
        feedback = MissingSignFeedback(comments=comments, meaning=meaning)
        feedback.save()    
        request = self.factory.get(self.url)
        response = showfeedback(request)
        self.assertContains(response, comments, count=1)
        self.assertContains(response, meaning, count=1)
            
    def test_sign_feedback_is_viewable(self):
        '''
        If there is sign feedback, it should be viewable
        '''
        data = {"correct" : "1", "use" : "1", "like" : "1", 
            "whereused" : "auswide", "isAuslan" : "1" }
        feedback = SignFeedback(**data)
        feedback.save()
        request = self.factory.get(self.url)
        response = showfeedback(request)
        for field in data:
            # Let's not check for the presence of 
            # 'auswide' because it doesn't show
            if data[field] != 'auswide': 
                self.assertContains(response, data[field])
                
                     
class DeleteView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def delete_view_redirects_on_success(self):
        '''
        The delete view should redirect on success.
        '''
        # Set up the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment)
        feedback.save()
        request = self.factory.get('irrelevant')
        response = delete(request, 'general', feedback.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_general_feedback(self):
        '''
        General feedback should be deletable.
        '''
        # Set up the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment)
        feedback.save()
        request = self.factory.get('irrelevant')
        response = delete(request, 'general', feedback.id)
        # Check that it's gone 
        deleted_feedback = GeneralFeedback.objects.get(pk=feedback.id)
        self.assertEqual('deleted', deleted_feedback.status)
        
    def test_delete_missing_sign_feedback(self):
        '''
        Missing sign feedback should be deletable.
        '''
        # Setup the missing sign feedback
        comments = "If you can read this, it is correct"
        meaning = "this too"
        feedback = MissingSignFeedback(comments=comments, meaning=meaning)
        feedback.save()  
        request = self.factory.get('irrelevant')
        response = delete(request, 'missingsign', feedback.id)
        # Check that it's gone 
        deleted_feedback = MissingSignFeedback.objects.get(pk=feedback.id)
        self.assertEqual('deleted', deleted_feedback.status)  
        
    def test_delete_sign_Feedback(self):
        '''
        Sign feedback should be deletable.
        '''
        data = {"correct" : "1", "use" : "1", "like" : "1", 
            "whereused" : "auswide", "isAuslan" : "1" }
        feedback = SignFeedback(**data)
        feedback.save()
        request = self.factory.get('irrelevant')
        response = delete(request, 'sign', feedback.id)
        # Check that it's gone
        deleted_feedback = SignFeedback.objects.get(pk=feedback.id)
        self.assertEqual('deleted', deleted_feedback.status)  
        
        


                        

  
        
 
    
