import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


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


class DetailViewTests(TestCase):
    """Tests of detail view."""

    def test_future_question(self):
        """Test for the detail view of a question with a pub_date in the future.

        It must returns a 404 not found.
        """
        text = 'Future question'
        future_question = create_question(question_text=text, days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Test for the detail view of a question with a pub_date in the past.

        It must displays the question's text.
        """
        past_question = create_question(question_text='Past Question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
