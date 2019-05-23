from selenium import webdriver
import unittest

class NewAnonymousVisitorBlankSiteTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_new_anonymous_visitor_sees_no_items(self):
        #Edith comes the TDD Polls site
        #She knew that she's in the right place beacause she sees
        #the title.
        self.browser.get('http://localhost:8000')
        self.assertIn('TDD Polls', self.browser.title)
        self.fail('Write the tests')
        
        #There is no items on the main page.

        #She cannot do anything so she quits.
        self.browser.quit()

# class NewAnonymousVisitorTest(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         #create some items here!

#     def tearDown(self):
#         self.browser.quit()

#     def test_new_visitor_sees_polls_and_can_vote(self):
#         #Edith once again tries the site.
#         #She sees the title of the newest polls in the main page
#         self.fail('Write the tests.')

#         #and the number of votes below them.
#         #It is 0 in the first place.

#         #She clicks and follows the link in the title of the first poll.

#         #She arrives to the page where she can vote.

#         #She selects the option she likes and hits 'Vote' to submit.

#         #She is redirected to the results page.

#         #She can see the result of her vote, because the first option
#         #has one vote, and the other has null.

#         #Then she goes back to the main page.

#         #She notices that the vot number of the first poll went up.
#         #It is 1 now, thanks to her vote.

#     def test_new_visitor_sets_items_on_main_page(self):
#         #Edith notices the drop-down in the upper left corner.
#         #It says '5'.
#         self.fail('Write the tests.')
#         #She notices that 5 polls are visible on the main page.

#         #She selects '10' from the options.
#         #Now there is 10 polls in the main page.

#     def test_new_visitor_can_browse_categories(self):
#         #Edith likes the polls, but she wants them organized.
#         #She notices the category below the polls' title.
#         self.fail('Write the tests.')
#         #It is a link - she clicks the 'Django' link.
#         #She gets redirected to the 'Django' polls.
#         #There is only one poll related to 'Django'.

#         #When she clicks the title, she is on the familiar vote page.

#         #She don't want to vote, so she follwos the link in the menu
#         #to the 'Categories'.

#         #She's on the categories page.

#         #She see 'General' and 'Django'. The URl of the 'Django' category
#         #is the same as she visited before.

#         #Satisfied she quites the page and goes offline.



if __name__ == '__main__':
    unittest.main(warnings='ignore')
