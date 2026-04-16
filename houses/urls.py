from django.urls import path
from .views import *

app_name = "houses"

urlpatterns = [

    path("list/", HouseListView.as_view(), name="list"),
    path("add/", HouseCreateView.as_view(), name="add"),
    path("edit/<int:pk>/", HouseUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", HouseDeleteView.as_view(), name="delete"),

]