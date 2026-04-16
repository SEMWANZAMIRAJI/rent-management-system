from django.db import models
from houses.models import House
from django.contrib.auth.models import User

# ================= USER PROFILE WITH ROLE =================
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

class Tenant(models.Model):
    full_name = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile',null=True,blank=True)
    property = models.ForeignKey(House,on_delete=models.CASCADE,null=True,blank=True)

    room_number = models.CharField(max_length=20,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.full_name
    

