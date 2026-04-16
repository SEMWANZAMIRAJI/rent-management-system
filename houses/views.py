from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import House

class HouseListView(ListView):
    model = House
    template_name = "houses/house_list.html"
    context_object_name="houses"


class HouseCreateView(CreateView):
    model = House
    fields = ["house_number","location","total_rooms","rent_price"]
    template_name = "houses/house_form.html"
    success_url = reverse_lazy("houses:list")


class HouseUpdateView(UpdateView):
    model = House
    fields = ["house_number","location","total_rooms"]
    template_name = "houses/house_form.html"
    success_url = reverse_lazy("houses:list")


class HouseDeleteView(DeleteView):
    model = House
    template_name = "houses/house_delete.html"
    success_url = reverse_lazy("houses:list")