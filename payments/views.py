from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Payment
from tenants.models import Tenant
from contracts.models import Contract
from notifications.utils import create_notification
from django.db.models import Max

# LIST


class PaymentListView(ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"

    def get_queryset(self):
        user = self.request.user

        # LANDLORD
        if hasattr(user, 'userprofile') and user.userprofile.role == 'landlord':

            latest_ids = (
                Payment.objects
                .values('contract__tenant')
                .annotate(last_id=Max('id'))
                .values_list('last_id', flat=True)
            )

            return Payment.objects.filter(
                id__in=latest_ids
            ).select_related(
                "contract__tenant",
                "contract__house"
            ).order_by('-id')

        # TENANT
        latest_ids = (
            Payment.objects.filter(contract__tenant__user=user)
            .values('contract__tenant')
            .annotate(last_id=Max('id'))
            .values_list('last_id', flat=True)
        )

        return Payment.objects.filter(
            id__in=latest_ids
        ).select_related(
            "contract__tenant",
            "contract__house"
        ).order_by('-id')


# CREATE


class PaymentCreateView(CreateView):
    model = Payment
    fields = ["contract", "amount_paid", "month", "method"]
    template_name = "payments/payment_form.html"
    success_url = reverse_lazy("payments:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        contracts = Contract.objects.select_related("tenant", "house")

        # landlord sees all
        if hasattr(user, "userprofile") and user.userprofile.role == "landlord":
            contracts = contracts
        else:
            contracts = contracts.filter(tenant__user=user)

        # 🔥 REMOVE DUPLICATES (latest per tenant+house)
        latest_ids = contracts.values('tenant_id', 'house_id').annotate(
            max_id=Max('id')
        ).values_list('max_id', flat=True)

        context["contracts"] = contracts.filter(id__in=latest_ids)

        return context

    def form_valid(self,form):
        response=super().form_valid(form)
        tenant =  form.instance.contract.tenant
        amount = form.instance.amount_paid


         # 🔔 Tenant gets notification
        create_notification(
            user=tenant.user,
            title="Payment Received",
            message=f"Your payment of TZS {amount} has been recorded."
        )

        # 🔔 Landlord gets notification
        create_notification(
            user=self.request.user,
            title="Payment Added",
            message=f"You added payment of TZS {amount} for {tenant.full_name}."
        )
        return response


# UPDATE
class PaymentUpdateView(UpdateView):
    model = Payment
    fields = ["contract","amount_paid","month","method"]
    template_name = "payments/payment_form.html"
    success_url = reverse_lazy("payments:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenants"] = Tenant.objects.all()
        context["contracts"] = Contract.objects.all()
        return context

# =====================================================
# PAYMENT DETAIL (VIEW BUTTON)
# =====================================================
    


class PaymentDetailView(DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenant = self.object.contract.tenant

        history = Payment.objects.filter(
            contract__tenant=tenant
        ).order_by('-id')

        context["history"] = history
        context["tenant"] = tenant
        context["total_paid"] = sum(p.amount_paid for p in history)

        return context
# DELETE
class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = "payments/payment_confirm_delete.html"
    success_url = reverse_lazy("payments:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Payment deleted successfully")
        return super().delete(request, *args, **kwargs)