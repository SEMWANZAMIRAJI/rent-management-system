from django.urls import path
from .views import *

app_name = "contracts"

urlpatterns = [
    path("", ContractListView.as_view(), name="list"),
    path("add/", ContractCreateView.as_view(), name="add"),
     path('<int:pk>/edit/', ContractUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name='delete'),
    path('<int:pk>/', ContractDetailView.as_view(), name='detail'), # Hii ndiyo ilikuwa inakosekana
    path('contract/<int:pk>/pdf/', ContractPDFView.as_view(), name='export_pdf'),
    
]