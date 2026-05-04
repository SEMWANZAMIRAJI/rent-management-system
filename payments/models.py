from django.db import models
from contracts.models import Contract
from tenants.models import Tenant
class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=20,null=True,blank=True)

    method = models.CharField(max_length=50,null=True,blank=True)
    # tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,null=True,blank=True)
    @property
    def total_months(self):
        return (self.contract.end_date.year - self.contract.start_date.year) * 12 + \
               (self.contract.end_date.month - self.contract.start_date.month)

    @property
    def total_rent(self):
        return self.total_months * self.amount_paid
    def __str__(self):
        return f"{self.contract.tenant} - {self.amount_paid}"