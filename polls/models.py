"""Models for Question and Choice."""
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question Model.

    Args:
        models : Question details (question_text, pub_date, end_date)
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date closed')

    def __str__(self):
        """Return a string represent of the question.

        Returns:
            String : the question text
        """
        return self.question_text

    def was_published_recently(self):
        """Return true if pub_date passes in 24 hrs.

        Returns:
            bool : true if question was published in 24 hrs.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = 'Published recently?'

    def was_closed(self):
        """Return true if end_date passed.

        Returns:
            bool : true if question was closed.
        """
        now = timezone.now()
        return self.end_date <= now

    was_closed.boolean = True
    was_closed.short_description = 'Closed?'

    def is_published(self):
        """Return true if pub_date passed.

        Returns:
            bool : true if question was published.
        """
        now = timezone.now()
        return self.pub_date <= now

    is_published.boolean = True
    is_published.short_description = 'Published?'

    def can_vote(self):
        """Return true if pub_date passed and end_date did not pass yet.

        Returns:
            bool : true if question is still active.
        """
        return self.is_published() and not self.was_closed()

    def was_closed_recently(self):
        """Return true if end_date passes in 24 hrs.

        Returns:
            bool : true if question was closed in 24 hrs.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.end_date <= now

    was_closed_recently.admin_order_field = 'end_date'
    was_closed_recently.boolean = True
    was_closed_recently.short_description = 'Closed recently?'

    def update_question_vote(self, user, choice):
        """Add a vote and Update number of votes for each choice base on Vote item"""
        try:
            previous_vote = user.vote_set.get(question=self)
            previous_vote.choice = choice
            previous_vote.save()
        except (KeyError, Vote.DoesNotExist):
            Vote.objects.create(question=self, choice=choice, user=user)

        for choice in self.choice_set.all():
            choice.update_vote()
            choice.save()

    def voted_status(self, user):
        """Return a string represent of the user vote status.

        Args:
            user : Current user

        Return:
            String : the user vote status
        """
        try:
            previous_vote = user.vote_set.get(question=self)
            return f"{user.username} have voted for {previous_vote.choice}"
        except (KeyError, Vote.DoesNotExist):
            return f"{user.username} have never voted for this question before"

    def get_current_choice(self, user):
        try:
            previous_vote = user.vote_set.get(question=self)
            return previous_vote.choice
        except (KeyError, Vote.DoesNotExist):
            return False


class Choice(models.Model):
    """Choice Model.

    Args:
        models : Choice details (question, choice_text, votes)
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def update_vote(self):
        self.votes = len(self.vote_set.all())

    def __str__(self):
        """Return a string represent of the choice.

        Returns:
            String : the choice text
        """
        return self.choice_text


class Vote(models.Model):
    """Vote Model.

    Args:
        models : Vote details (question, choice, user)
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
