from selenium import webdriver
import unittest

class NewVisitorLogInTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_sign_up_and_log_in(self):
        # Edith goes to the Polls app homepage
        self.browser.get('http://localhost:8000')
        
        # She noticies the title mentions polls
        self.assertIn('Polls', self.browser.title)
        self.fail('Finish the tests.')
        
        # She sees a note that she needs to sign in
        # if she wants to create a question
        
        
        # She clicks on the "sign up" link (since
        # she do not have an account)
        
        # She is prompted to choose a username 
        # and password
        
        # When she clicks the sig up button
        # she is logged in automatically
        
        # She is suspicious, se logs out
        
        # And log in again

if __name__ == '__main__':
    unittest.main(warnings='ignore')
