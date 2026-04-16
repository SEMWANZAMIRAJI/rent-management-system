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
    def tenant(self):
     return self.contract.tenant
    @property
    def house(self):
        return self.contract.house
    def __str__(self):
        return f"{self.tenant} - {self.amount_paid}"