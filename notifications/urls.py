from django.urls import path
from .views import NotificationListView,MarkAsReadView

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
     
    path('<int:pk>/read/', MarkAsReadView.as_view(), name='read'),
]