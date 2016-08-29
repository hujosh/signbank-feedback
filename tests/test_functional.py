from django_webtest import WebTest


class MyTestCase(WebTest):
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


        
        
        
        

