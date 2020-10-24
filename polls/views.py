"""Views for polls app."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    """ListView for index page contain question queryset."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the all published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())

@login_required
def detail(request, question_id):
    """View for detail page of that question_id question.

    If that question is not published redirect to index and
    set the error message.

    Args:
        question_id (int): question's id

    Returns:
        HttpResponse : the question detail page
        or index page with error messages
    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        msg = f"Poll: \"{question.question_text}\" is not longer publish."
        messages.error(request, msg)
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    """View for results page."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """View for vote page of that question_id question.

    Args:
        question_id (int): question's id

    Returns:
        HttpResponse : Vote page
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        url = reverse('polls:results', args=(question.id,))
        return HttpResponseRedirect(url)
