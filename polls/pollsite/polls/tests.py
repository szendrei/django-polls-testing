import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def add_choice(question, choice_text, votes=0):
    """
    Add choice to a Question model object with a given 'choice_text' and
    an optional 'votes' number of votes. Default is 0 votes.
    """
    return question.choice_set.create(choice_text=choice_text, votes=votes)

def create_question_with_choice(question_text, days, choice_text, votes=0):
    """
    Creates a question with given 'question_text' a 'pub_date' offset by
    days. Also add a choice with given 'choice_text' and number of votes
    (defualt 0).
    """
    question = create_question(question_text=question_text, days=days)
    add_choice(question, choice_text=choice_text, votes=votes)
    return question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() return False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() retruns True for questions whose pub_date
        is within the las day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with pub_date in the past are displayed on the
        index page. It checks is question with one choice
        is displayed as well. No need for 'test_past_question_with_one_choice'.
        """
        create_question_with_choice(question_text="Past question.",
                                               days=-30,
                                               choice_text='Choice 1.')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question_with_choice(question_text="Future question.",
                                               days=30,
                                               choice_text='Choice 1.')
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question_with_choice(question_text="Past question.",
                                           days=-30,
                                           choice_text='Choice 1.')
        create_question_with_choice(question_text="Future question.",
                                 days=30,
                                 choice_text='Choice 2.')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        create_question_with_choice(question_text="Past question 1.",
                                            days=-30,
                                            choice_text='Choice 1.')
        create_question_with_choice(question_text="Past question 2.",
                                    days=-5,
                                    choice_text='Choice 2.')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_past_question_without_choices(self):
        """
        Question without choices should not be displayed on the index page.
        """
        create_question(question_text='Choiceless question.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response, "No polls are available.")

    def test_past_question_with_multiple_choices(self):
        """
        Questions with at least one choice are listed on the index page.
        """
        choice_question = create_question(question_text='Multiple choices',
                                          days=-1)
        add_choice(choice_question, choice_text='Choice 1', votes=1)
        add_choice(choice_question, choice_text='Choice 2', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Multiple choices>'])

    def test_question_with_choice_and_without_choice(self):
        """
        Only the questions with choice(s) are listed.
        """
        create_question(question_text='Choiceless question', days=-1)
        create_question_with_choice(question_text='Question with choice.',
                                    days=-1,
                                    choice_text='Choose me.',
                                    votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Question with choice.>'])

    def test_two_questions_with_choices(self):
        """
        Both questions with choices are displayed.
        """
        create_question_with_choice(question_text='Choices 1',
                                     days=-5,
                                     choice_text='Choice 1')
        create_question_with_choice(question_text='Choices 2',
                                     days=-30,
                                     choice_text='Choice 2',
                                     votes=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Choices 1>','<Question: Choices 2>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_one_choice(self):
        """
        The detail view if a question with a pub_date in the past
        and one choice displays the question's and the choice's text.
        """
        past_question = create_question(question_text='Past question.', days=-5)
        add_choice(past_question, choice_text='Choice')
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        self.assertContains(response,
                            past_question.choice_set.get(pk=1).choice_text)

    def test_past_question_without_choice(self):
        """
        The detail view of a choiceless quesion return a 404 not found.
        """
        past_question_choiceless = create_question(
            question_text='Past question',
            days=-1)
        url = reverse('polls:detail', args=(past_question_choiceless.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_multiple_choices(self):
        """
        The detail view of a question with multiple choices
        display the question's text and a list of the choice's text.
        """
        past_question_multiple = create_question(
            question_text='Past question with multiple choice.',
            days=-2)
        add_choice(past_question_multiple, choice_text='Choice 1.')
        add_choice(past_question_multiple, choice_text='Choice 2.', votes=1)
        url = reverse('polls:detail', args=(past_question_multiple.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question_multiple.question_text)
        self.assertQuerysetEqual(
            response.context['question'].choice_set.all(),
            ['<Choice: Choice 1.>', '<Choice: Choice 2.>'], ordered=False)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        The results view of the question with a pub_date in the future
        returns a 404 not found like the detail view.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with pub_date in the past
        displays the questions text with the results of the vote.
        """
        past_question = create_question(question_text='Past question.', days=-5)
        past_question_with_votes = add_choice(past_question, 
                                               choice_text='Choice 1.')
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        self.assertContains(response, past_question_with_votes.choice_text)

    def test_past_question_without_choice(self):
        """
        The results view of a past question without choices
        return 404 not found like the detail view.
        """
        past_question = create_question(question_text='Past choiceless question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_with_multiple_choices(self):
        """
        The results view of a past quesrion with multiple
        choices displays the question text with the choices and votes
        of regarding question.
        """
        past_question = create_question(
            question_text='Past question, multiple choices.',
            days = -1)
        add_choice(
            past_question,
            choice_text = 'Choice 1',
            votes = 1)
        add_choice(
            past_question,
            choice_text = 'Choice 2',
            votes = 5)
        add_choice(
            past_question,
            choice_text = 'Choice 3')
        url = reverse('polls:results',
                      args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,
                            past_question.question_text)
        for (chid, votenum) in zip([0,1,2], [1, 5, 0]):
            self.assertEqual(
                response.context['question'].choice_set.all()[chid].votes,
                votenum)


class VoteTestClass(TestCase):
    def test_vote_raise_error(self):
        """
        Voting when nothing selected raises a DoesNotExist error.
        """
        question = create_question(
            question_text="Question 1.",
            days = -2)
        add_choice(question, choice_text="Choice 1.")
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url)
        self.assertRaises("Keyerror")


    def test_vote_increments(self):
        """
        One vote should increment the number of votes of the choice.
        """
        question = create_question(
            question_text="Question 1.",
            days = -2)
        add_choice(question, choice_text="Choice 1.")
        initial_vote = question.choice_set.get(pk=1).votes
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url,
                                    {'choice': question.choice_set.all()[0].pk})
        after_vote = question.choice_set.get(pk=1).votes
        self.assertEqual(initial_vote + 1, after_vote)

    def test_redicerts_on_successful_vote(self):
        """
        After a successful vote the Detail view redirects to a Results view.
        """
        question = create_question(
            question_text="Question 1.",
            days = -2)
        add_choice(question, choice_text="Choice 1.")
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url,
                                    {'choice': question.choice_set.all()[0].pk})
        self.assertRedirects(response, reverse('polls:results', 
                                               args=(question.id,)))

    def test_renders_DetailView_on_failed_vote(self):
        """
        Faild vote should render DeatilView.
        """
        question = create_question(
            question_text="Question 1.",
            days = -2)
        add_choice(question, choice_text="Choice 1.")
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url)
        self.assertTemplateUsed(response, "polls/detail.html")

    def test_renders_error_msg_on_failed_vote(self):
        """
        After an unsuccessful vote the Detail view rendered with
        an appropriate error message.
        """
        question = create_question(
            question_text="Question 1.",
            days = -2)
        add_choice(question, choice_text="Choice 1.")
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url)
        self.assertEqual(response.context['error_message'],
                         "You didn't select a choice.")
