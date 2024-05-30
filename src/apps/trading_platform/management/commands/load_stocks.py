import csv
import os

from django.core.management.base import BaseCommand

from src.apps.trading_platform.models import Stock


class Command(BaseCommand):
    help = 'Load stocks from a CSV file'

    def handle(self, *args: str, **kwargs: str) -> None:
        """Handle command execution."""
        csv_file_path = os.path.join("src", "apps", "trading_platform", "static", "stocks.csv")

        with open(csv_file_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                indicator, created = Stock.objects.get_or_create(name=name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Indicator "{name}" added successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Indicator "{name}" already exists.'))
