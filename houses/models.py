from django.db import models

class House(models.Model):
    house_number = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    total_rooms = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    

    def __str__(self):
        return self.house_number