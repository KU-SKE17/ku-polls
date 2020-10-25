import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class PollDatesTests(TestCase):
    """Tests of question model."""

    def setUp(self):
        """Create constant itme use for tests in this class."""
        self.add_time_one_year = datetime.timedelta(days=365)

    def test_was_published_recently_with_future_question(self):
        """Test for was_published_recently().

        was_published_recently() must returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        end_time = time+self.add_time_one_year
        future_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Test for was_published_recently().

        was_published_recently() must returns False for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end_time = time+self.add_time_one_year
        old_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test for was_published_recently().

        was_published_recently() must returns True for questions whose pub_date is within the last day.
        """
        delta = datetime.timedelta(hours=23, minutes=59, seconds=59)
        time = timezone.now() - delta
        end_time = time+self.add_time_one_year
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_closed_is_work(self):
        """Test for was_closed().

        was_closed() must returns True for questions whose end_date is now or passed.
        """
        time = timezone.now()
        after_day = time + self.add_time_one_year
        question1 = Question(pub_date=time, end_date=after_day)
        self.assertIs(question1.was_closed(), False)
        question2 = Question(pub_date=time, end_date=time)
        self.assertIs(question2.was_closed(), True)
        end_time = time-datetime.timedelta(days=1)
        question3 = Question(pub_date=time, end_date=end_time)
        self.assertIs(question3.was_closed(), True)

    def test_is_published_is_work(self):
        """Test for is_published().

        is_published() must returns True for questions
        whose pub_date is already published.
        """
        time = timezone.now()
        day_before = time - self.add_time_one_year
        after_day = time + self.add_time_one_year
        question1 = Question(pub_date=time, end_date=after_day)
        self.assertIs(question1.is_published(), True)
        question2 = Question(pub_date=day_before, end_date=after_day)
        self.assertIs(question2.is_published(), True)
        question3 = Question(pub_date=after_day, end_date=after_day+self.add_time_one_year)
        self.assertIs(question3.is_published(), False)
        question4 = Question(pub_date=after_day, end_date=time)
        self.assertIs(question4.is_published(), False)
        question5 = Question(pub_date=time, end_date=time)
        self.assertIs(question5.is_published(), True)

    def test_can_vote_is_work(self):
        """Test for can_vote().

        can_vote() must returns True for questions whose pub_date is already published and end_date is not come yet.
        """
        time = timezone.now()
        day_before = time-self.add_time_one_year
        after_day = time+self.add_time_one_year
        question1 = Question(pub_date=time, end_date=after_day)
        self.assertIs(question1.can_vote(), True)
        question2 = Question(pub_date=day_before, end_date=after_day)
        self.assertIs(question2.can_vote(), True)
        question3 = Question(pub_date=after_day, end_date=after_day+self.add_time_one_year)
        self.assertIs(question3.can_vote(), False)
        question4 = Question(pub_date=after_day, end_date=time)
        self.assertIs(question4.can_vote(), False)
        question5 = Question(pub_date=time, end_date=time)
        self.assertIs(question5.can_vote(), False)
        question6 = Question(pub_date=day_before, end_date=time)
        self.assertIs(question6.can_vote(), False)
