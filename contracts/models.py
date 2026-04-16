from django.db import models
from tenants.models import Tenant
from houses.models import House
from django.core.exceptions import ValidationError

class Contract(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(db_index=True)

    def total_months(self):
        return (self.end_date.year - self.start_date.year) * 12 + (self.end_date.month - self.start_date.month)

    def total_rent(self):
        return self.total_months() * self.rent_amount
    
    from datetime import date

    @property
    def contract_months(self):
        if self.start_date and self.end_date:
            return (self.end_date.year - self.start_date.year) * 12 + \
               (self.end_date.month - self.start_date.month)
        return 0


    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")


    def __str__(self):
        return f"{self.tenant} Contracts - {self.house}"