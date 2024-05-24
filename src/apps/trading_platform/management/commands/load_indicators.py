import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from src.apps.trading_platform.models import Indicator


class Command(BaseCommand):
    help = 'Load indicators from a CSV file'

    def handle(self, *args: str, **kwargs: str) -> None:
        """Handle command execution."""
        csv_file_path = os.path.join(settings.BASE_DIR.parent, 'indicators.csv')

        with open(csv_file_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                indicator, created = Indicator.objects.get_or_create(name=name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Indicator "{name}" added successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Indicator "{name}" already exists.'))
