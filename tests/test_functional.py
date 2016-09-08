import datetime
from django_webtest import WebTest
from feedback.models import GeneralFeedback


class IndexPage(WebTest):
    def test_index_page_clicking_on_general_feedback(self):
        # The user goes to the index page...
        index = self.app.get('/')
        self.assertTemplateUsed(index, "feedback/index.html")

        # He clicks on the 1st general feedback link
        genereal_feedback = index.click('General Feedback', index = 0)
        # He is taken to the general feedback form
        self.assertTemplateUsed( genereal_feedback, "feedback/generalfeedback_form.html")
        
        # The user goes back to the index page...
        index = self.app.get('/')

        # He clicks on the 2nd general feedback link
        genereal_feedback = index.click('General Feedback', index = 1)
        # He is taken to the general feedback form
        self.assertTemplateUsed( genereal_feedback, "feedback/generalfeedback_form.html")

        # The user goes back to the index page...
        index = self.app.get('/')

        # He tries to click on the 3rd general feedback link
        # ...There isn't one...
        with self.assertRaises(IndexError):
            index.click('General Feedback', index = 2)

    def test_index_page_clicking_on_missing_sign_feedback(self): 
        # The user goes to the index page...
        index = self.app.get('/')
        self.assertTemplateUsed(index, "feedback/index.html")

        # He clicks on the 1st missing sign link
        missing_sign = index.click('Report a Missing Sign', index = 0)
        # He is taken to the general feedback form
        self.assertTemplateUsed(missing_sign, "feedback/missingsign_form.html")
        
        # The user goes back to the index page...
        index = self.app.get('/')

        # He clicks on the 2nd missing sign link
        missing_sign = index.click('Report a Missing Sign', index = 1)
        # He is taken to the general feedback form
        self.assertTemplateUsed(missing_sign, "feedback/missingsign_form.html")

        # The user goes back to the index page...
        index = self.app.get('/')

        # He tries to click on the 3rd missing sign link
        # ...There isn't one...
        with self.assertRaises(IndexError):
            index.click('Report a Missing Sign', index = 2)


class GenearlFeedbackPage(WebTest):
    def setUp(self):
        self.data = {'comment' : 'this is a comment' }
    
    def go_to_general_feedback_page(self):
         # The user goes to the genereal feedback page...
        general_feedback = self.app.get('/generalfeedback/')
        self.assertTemplateUsed(general_feedback, 'feedback/generalfeedback_form.html')
        # He sees one form
        self.assertEqual(len(general_feedback.forms), 1)
        return general_feedback
                        
    def test_submit_general_feedback(self):
        
        # The user goes to the general feedback page
        general_feedback = self.go_to_general_feedback_page()
        # He enters a comment
        general_feedback.form['comment'] = self.data['comment']
        # He clicks the submit button
        redirect = general_feedback.form.submit()
        # He should be redirected 
        self.assertIn('302', redirect.status)
        message_page = redirect.follow()
        self.assertIn('Thanks for your comment. We value your contribution', message_page)
        
        # Now let's make sure that the feedback is in the database                                                           
        feedback = GeneralFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a date 
        self.assertIsInstance(feedback[0].date, datetime.date)
        self.assertEqual(feedback[0].date, datetime.date.today())
        # It should have a comment
        self.assertEqual(feedback[0].comment, self.data['comment'])
        
    def test_submit_general_feedback_with_empty_Feedback_field(self):
        general_feedback = self.go_to_general_feedback_page()
        # He clicks the submit button without any data in the comment field
        form_errors = general_feedback.form.submit()
        # He should not have been redirected
        self.assertIn('200', form_errors.status)
        # There should be no success message 
        self.assertNotIn('Thanks for your comment. We value your contribution', form_errors)
        # He should be back on the general feedback form
        self.assertTemplateUsed(general_feedback, 'feedback/generalfeedback_form.html')
        self.assertIn("General Feedback", form_errors)
        # He should see the form
        self.assertEqual(len(general_feedback.forms), 1)
        # He should see an error message indicating that the form was not submitted
        self.assertIn("This field is required", form_errors)
        
        
        
  
        

