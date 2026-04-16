# notifications/services.py
from django.utils import timezone
from contracts.models import Contract
from .models import Notification
from .utils import create_notification

def check_contract_notifications():
    today = timezone.now().date()

    contracts = Contract.objects.all()

    for contract in contracts:
        days_left = (contract.end_date - today).days

        tenant = contract.tenant

        # Prevent duplicate notifications
        def already_sent(days):
            return Notification.objects.filter(
                tenant=tenant,
                message__icontains=f"{days} day"
            ).exists()

        # 30 days
        if days_left == 30 and not already_sent(30):
            create_notification(
                tenant,
                "Rent Reminder",
                "Your rent will expire in 30 days"
            )

        # 7 days
        elif days_left == 7 and not already_sent(7):
            create_notification(
                tenant,
                "Rent Reminder",
                "Your rent will expire in 7 days"
            )

        # 1 day
        elif days_left == 1 and not already_sent(1):
            create_notification(
                tenant,
                "Urgent Reminder",
                "Your rent expires tomorrow!"
            )