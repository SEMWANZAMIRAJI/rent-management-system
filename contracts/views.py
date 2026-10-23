from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Contract
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from tenants.models import Tenant
from houses.models import House
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Max
from datetime import date
from calendar import monthrange
# ---------------- LIST ----------------


class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "contracts/contract_list.html"
    context_object_name = "contracts"



class ContractCreateView(CreateView):
    model = Contract
    fields = ['tenant', 'house', 'rent_amount', 'start_date', 'end_date','total_rent', 'contract_months']
    template_name = "contracts/contract_form.html"
    success_url = reverse_lazy("contracts:list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()  # hii inaita model.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenants"] = Tenant.objects.all()
        context["houses"] = House.objects.all()
        return context

    
# ---------------- UPDATE ----------------
class ContractUpdateView(UpdateView):
    model = Contract
    fields = ['tenant', 'house', 'rent_amount', 'start_date', 'end_date','total_rent']
    template_name = "contracts/contract_form.html"
    success_url = reverse_lazy("contracts:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenants"] = Tenant.objects.all()
        context["houses"] = House.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        contract = self.get_object()
        tenant_id = request.POST.get("tenant")
        house_id = request.POST.get("house")
        rent_amount = request.POST.get("rent_amount")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        total_rent = request.POST.get("total_rent")

        errors = []
        if not tenant_id: errors.append("Tenant is required")
        if not house_id: errors.append("House is required")
        if not rent_amount: errors.append("Rent amount is required")
        if not start_date: errors.append("Start date is required")
        if not end_date: errors.append("End date is required")
        if not total_rent: errors.append("Total rent is required")

        if errors:
            for e in errors:
                messages.error(request, e)
            return redirect("contracts:edit", pk=contract.pk)

        contract.tenant_id = tenant_id
        contract.house_id = house_id
        contract.rent_amount = rent_amount
        contract.start_date = start_date
        contract.end_date = end_date
        contract.total_rent = total_rent
        contract.save()

        messages.success(request, "Contract updated successfully!")
        return redirect("contracts:list")

# ---------------- DELETE ----------------
class ContractDeleteView(DeleteView):
    model = Contract
    template_name = "contracts/contract_confirm_delete.html"
    success_url = reverse_lazy("contracts:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Contract deleted successfully!")
        return super().delete(request, *args, **kwargs)
    


class ContractDetailView(LoginRequiredMixin, DetailView):
    model = Contract
    template_name = "contracts/contract_detail.html"
    context_object_name = "contract"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contract = self.object

        # 🔥 ALL CONTRACT HISTORY FOR SAME TENANT
        context["history"] = Contract.objects.filter(
            tenant=contract.tenant
        ).order_by('-id')

        return context


class ContractPDFView(View):
    def get(self, request, pk):
        contract = Contract.objects.get(pk=pk)
        template = get_template('contracts/contract_pdf.html')
        html = template.render({'contract': contract})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="contract.pdf"'

        pisa.CreatePDF(html, dest=response)
        return response





