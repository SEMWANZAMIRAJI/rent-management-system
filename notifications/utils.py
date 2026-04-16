# notifications/utils.py
from .models import Notification
# from django.contrib.auth.models import User

def create_notification(title, message, user):
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )