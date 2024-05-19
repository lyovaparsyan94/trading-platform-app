import csv
import os
from django.core.management.base import BaseCommand
from src.apps.trading_platform.models import Indicator


class Command(BaseCommand):
    help = 'Load indicators from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), '../../../../../indicators.csv')

        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                if not Indicator.objects.filter(name=name).exists():
                    Indicator.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Indicator "{name}" added successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Indicator "{name}" already exists.'))
