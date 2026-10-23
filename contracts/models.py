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
    total_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    contract_months = models.PositiveIntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):

        # 🔥 months user provided (NOT auto)
        if self.contract_months and self.rent_amount:
            self.total_rent = self.contract_months * float(self.rent_amount)

        super().save(*args, **kwargs)

   


    def __str__(self):
        return f"{self.tenant} Contracts - {self.house}"