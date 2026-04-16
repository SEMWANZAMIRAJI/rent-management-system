# notifications/management/commands/check_notifications.py
from django.core.management.base import BaseCommand
from notifications.services import check_contract_notifications

class Command(BaseCommand):
    help = "Check and create contract notifications"

    def handle(self, *args, **kwargs):
        check_contract_notifications()
        self.stdout.write(self.style.SUCCESS("Notifications checked successfully"))