import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
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


class AuthTests(TestCase):
    """Tests of Authentication."""

    def setUp(self):
        self.question = create_question(question_text='Past Question.', days=-5)
        self.user = get_user_model().objects.create_user(
            username="Kitty",
            email="yoyo@gmail.com",
            password="@yoyo007",
            first_name="Yoyo",
            last_name="Limkool"
        )

    def test_login_to_index(self):
        """Check index page contain username after login"""
        self.client.login(username="Kitty", password="@yoyo007")
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_not_login_to_index(self):
        """Check index page not contain username after login and contain login button"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)
        self.assertContains(response, 'Login')

    def test_login_to_detail(self):
        """Check detail page contain username after login"""
        self.client.login(username="Kitty", password="@yoyo007")
        response = self.client.get(reverse("polls:detail", args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_not_login_to_detail(self):
        """Check detail redirect to login page if not login"""
        response = self.client.get(reverse("polls:detail", args=(self.question.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/polls/1/')

    def test_login_vote(self):
        """Check detail page contain username after login"""
        self.client.login(username="Kitty", password="@yoyo007")
        response = self.client.get(reverse('polls:vote', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_not_login_vote(self):
        """Check detail redirect to login page if not login"""
        response = self.client.get(reverse('polls:vote', args=(self.question.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/polls/1/vote/')
