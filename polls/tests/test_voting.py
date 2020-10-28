import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from polls.models import Question, Choice


def create_user(username, password, first_name='anonymous', last_name='no surnames', email='foo@boo.com'):
    """Create a User.

    Returns:
        User : a new user
    """
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )


def create_question(question_text, days):
    """Create a question.

    with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    Returns:
        Question : a new question
    """
    pub = timezone.now() + datetime.timedelta(days=days)
    end = pub+datetime.timedelta(days=365)
    return Question.objects.create(
        question_text=question_text,
        pub_date=pub,
        end_date=end
    )


def create_choice(question, choice_text):
    """Create a Choice.

    Returns:
        Choice : a new choice
    """
    return Choice.objects.create(
            question=question,
            choice_text=choice_text,
            votes=0
    )


def create_vote(question, choice, user):
    """Create a Vote."""
    question.update_question_vote(user, choice)


class VotingTests(TestCase):

    def setUp(self):
        self.user = create_user("Kitty", "@yoyo007")
        self.another_user = create_user("Dicky", "puppyisnotkitty")
        self.client.login(username="Kitty", password="@yoyo007")
        self.question = create_question(question_text='Past Question.', days=-5)
        self.choice_a = create_choice(self.question, 'choice_a')
        self.choice_b = create_choice(self.question, 'choice_b')

    def update_choice_vote(self):
        self.choice_a.update_vote()
        self.choice_b.update_vote()

    def test_vote(self):
        """Test if Vote can update the poll"""
        create_vote(self.question, self.choice_a, self.user)
        # self.question.update_question_vote(self.user, self.choice_a)
        self.update_choice_vote()
        self.assertEqual(self.choice_a.votes, 1)
        self.assertEqual(self.choice_b.votes, 0)

    def test_vote_same_question(self):
        """Test when same user vote another choice"""
        create_vote(self.question, self.choice_a, self.user)
        create_vote(self.question, self.choice_b, self.user)
        self.update_choice_vote()
        self.assertEqual(self.choice_a.votes, 0)
        self.assertEqual(self.choice_b.votes, 1)

    def test_vote_same_choice(self):
        """Test when same user vote the same choice"""
        create_vote(self.question, self.choice_a, self.user)
        create_vote(self.question, self.choice_a, self.user)
        self.update_choice_vote()
        self.assertEqual(self.choice_a.votes, 1)
        self.assertEqual(self.choice_b.votes, 0)

    def test_another_user_vote(self):
        """Test when another user vote the same question"""
        create_vote(self.question, self.choice_a, self.user)
        create_vote(self.question, self.choice_b, self.another_user)
        self.update_choice_vote()
        self.assertEqual(self.choice_a.votes, 1)
        self.assertEqual(self.choice_b.votes, 1)

    def test_another_user_vote_same_choice(self):
        """Test when another user vote the same question,and same choice"""
        create_vote(self.question, self.choice_a, self.user)
        create_vote(self.question, self.choice_a, self.another_user)
        self.update_choice_vote()
        self.assertEqual(self.choice_a.votes, 2)
        self.assertEqual(self.choice_b.votes, 0)
