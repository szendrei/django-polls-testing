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
        
        # 

if __name__ == '__main__':
    unittest.main(warnings='ignore')
