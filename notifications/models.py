from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,null=True)
    is_read = models.BooleanField(default=False,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message