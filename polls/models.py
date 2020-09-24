import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date closed')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = 'Published recently?'

    def was_closed(self):
        now = timezone.now()
        return self.end_date <= now

    was_closed.boolean = True
    was_closed.short_description = 'Closed?'

    def is_published(self):
        now = timezone.now()
        return self.pub_date <= now

    is_published.boolean = True
    is_published.short_description = 'Published?'

    def can_vote(self):
        return self.is_published() and not self.was_closed()

    def was_closed_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.end_date <= now

    was_closed_recently.admin_order_field = 'end_date'
    was_closed_recently.boolean = True
    was_closed_recently.short_description = 'Closed recently?'

    def total_vote(self):
        votes = self.choice_set.aggregate(models.Sum('votes'))
        return votes['votes__sum']

    def reset_vote(self):
        choices = self.choice_set.all()
        for choice in choices:
            choice.votes = 0
            choice.save()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
