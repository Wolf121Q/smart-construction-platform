from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from datetime import datetime
# Signals For Logged In and Logged Out

@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    user.last_login = datetime.now()
    user.save()

@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    user.last_logout = datetime.now()
    user.save()