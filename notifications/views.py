# notifications/views.py
from django.views.generic import ListView, View
from django.shortcuts import redirect
from .models import Notification
from django.contrib import messages

class NotificationListView(ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        user = self.request.user
        
        # 1. Angalia kama huyu aliyelog-in ni Landlord kupitia UserProfile
        if hasattr(user, 'userprofile') and user.userprofile.role == 'landlord':
            # Landlord anaona malipo yote ya wapangaji wote
            return Notification.objects.all().order_by('-id')
        
        return Notification.objects.filter(
            user=self.request.user   # 🔥 muhimu sana
        ).order_by("-created_at")



class MarkAsReadView(View):
    def get(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            messages.success(request, "Notification marked as read.")
        except Notification.DoesNotExist:
            messages.error(request, "Notification not found or does not belong to you.")
        return redirect('notifications:list')