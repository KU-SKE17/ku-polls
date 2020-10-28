import logging

from django.contrib import messages
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)-4s %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
)
logger = logging.getLogger(__name__)


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('polls:index')
            return redirect('login')
        else:
            msg = f"Form is not valid"
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('signup'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Display log message, when successful login."""
    logger.info('user: {user} - login using ip: {ip}'.format(
        user=user,
        ip=request.META.get('REMOTE_ADDR')
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """Display log message, when successful logout."""
    logger.info('user: {user} - logout using ip: {ip}'.format(
        user=user,
        ip=request.META.get('REMOTE_ADDR')
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    """Display log message, when unsuccessful login."""
    logger.warning('user: {user} - failed to login using ip: {ip}'.format(
        user=credentials['username'],
        ip=request.META.get('REMOTE_ADDR')
    ))
