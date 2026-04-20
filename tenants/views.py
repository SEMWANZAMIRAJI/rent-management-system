from django.contrib.auth import models
from django.views.generic import ListView, CreateView,TemplateView,View,UpdateView,DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from django.urls import reverse_lazy
from django.views import View
from tenants.models import Tenant, UserProfile
from houses.models import House
from contracts.models import Contract
from payments.models import Payment
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum  # ✅ CORRECT

class HomePageView(TemplateView):
    template_name = "home.html"

class TenantListView(ListView):
    model = Tenant
    template_name = "tenants/tenant_list.html"
    context_object_name="tenants"

class TenantCreateView(CreateView):
    model = Tenant
    fields = ["full_name","phone","email","property","room_number"]
    template_name = "tenants/tenant_form.html"
    success_url = reverse_lazy("tenants:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()  # Pass houses for <select>
        return context

# class TenantCreateView(CreateView):
#     model = Tenant
#     fields = ['full_name', 'phone', 'email']
#     template_name = 'tenants/create.html'
#     success_url = '/tenants/'

class TenantUpdateView(UpdateView):
    model = Tenant
    fields = ["full_name", "phone", "email", "property", "room_number"]
    template_name = "tenants/tenant_form.html"
    success_url = reverse_lazy("tenants:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()  # Needed for <select>
        return context

class TenantDeleteView(DeleteView):
    model = Tenant
    template_name = "tenants/tenant_confirm_delete.html"
    success_url = reverse_lazy("tenants:list")


# ================= LOGIN VIEW =================
class LoginView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone = request.POST.get('username')  # phone number used as username
        password = request.POST.get('password')

        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('tenants:dashboard')  # change this to your dashboard url
        else:
            messages.error(request, "Invalid phone number or password")
            return render(request, self.template_name)

# ================= REGISTER VIEW =================



class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone = request.POST.get('username')  # phone number as username
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        if User.objects.filter(username=phone).exists():
            messages.error(request, "Phone number already registered")
            return render(request, self.template_name)

        # 1️⃣ Create User
        user = User.objects.create_user(username=phone, password=password)

        # 2️⃣ Create UserProfile (default role = tenant)
        UserProfile.objects.create(user=user, role='tenant')

        # 3️⃣ Create Tenant record (fields optional)
        Tenant.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            email=email
        )

        messages.success(request, "Account created successfully. You can now login.")
        return redirect('tenants:login')

# ================= LOGOUT VIEW =================

class LogoutView(View):
    def get(self, request):
        logout(request)  # this clears the session
        return redirect('tenants:login')  # redirect user to login page
    

    
# ================= DASHBOARD VIEW =================


class DashboardView(LoginRequiredMixin, View):
    login_url = 'tenants:login'
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        profile = request.user.userprofile

        now = timezone.now()
        current_month = now.strftime("%B")

        # Common data
        pending_notifications = Notification.objects.filter(is_read=False).count()

        if profile.role == 'tenant':
            # Get only data relevant to this tenant
            tenant_profile = request.user.tenant_profile
            contracts = Contract.objects.filter(tenant=tenant_profile)
            total_contracts = contracts.count()
            pending_payments = Payment.objects.filter(
                contract__tenant=tenant_profile, month=current_month
            ).count()
            monthly_revenue = Payment.objects.filter(
                contract__tenant=tenant_profile, month=current_month
            ).aggregate(total=Sum('amount_paid'))['total'] or 0

            context = {
                "role": "tenant",
                "total_contracts": total_contracts,
                "pending_payments": pending_payments,
                "monthly_revenue": monthly_revenue,
                "pending_notifications": pending_notifications,
            }

        elif profile.role == 'landlord':
            # Landlord sees overall data
            total_tenants = Tenant.objects.count()
            total_houses = House.objects.count()
            total_contracts = Contract.objects.count()
            monthly_revenue = Payment.objects.filter(month=current_month).aggregate(
                total=Sum('amount_paid')
            )['total'] or 0
            pending_payments = Contract.objects.filter(
                end_date__lte=now + timedelta(days=7)
            ).count()

            context = {
                "role": "landlord",
                "total_tenants": total_tenants,
                "total_houses": total_houses,
                "total_contracts": total_contracts,
                "monthly_revenue": monthly_revenue,
                "pending_payments": pending_payments,
                "pending_notifications": pending_notifications,
            }

        return render(request, self.template_name, context)

