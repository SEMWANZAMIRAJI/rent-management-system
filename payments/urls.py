from django.urls import path
from .views import PaymentListView, PaymentCreateView,PaymentUpdateView,PaymentDeleteView,PaymentDetailView

app_name = "payments"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("add/", PaymentCreateView.as_view(), name="add"),
    path('<int:pk>/edit/', PaymentUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', PaymentDeleteView.as_view(), name='delete'),
    path("<int:pk>/", PaymentDetailView.as_view(), name="detail"),
    
]