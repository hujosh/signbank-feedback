from django.test import TestCase

from feedback.models import SignFeedback
from .test_views import create_user

class SignFeedbackTests(TestCase):
    def setUp(self):
        self.data =  {'comment' : 'This is a comment', 'name' : 'dog-1',
                       'user' : create_user()}
    def test_string_method(self):
        '''
        The name returned by the __str__ method 
        of a SignFeedback instance should be 'name by user on date'. 
        '''
        #First, create the signfeedback
        feedback = SignFeedback(**self.data)
        feedback.save()
        # Let's retrieve the feedback from the database...
        feedback = SignFeedback.objects.get(pk=1)
        date = feedback.date
        user_name = feedback.user.first_name
        name = feedback.name
        feedback_name = "%s by %s on %s"%(name, user_name, date)
        self.assertEqual(feedback_name, str(feedback))
        
        
