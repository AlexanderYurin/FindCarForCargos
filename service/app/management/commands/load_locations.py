import csv
from django.core.management.base import BaseCommand

from app.models import Location


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		file_path = "./data_location/uszips.csv"
		with open(file_path, "r", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				Location.objects.create(
					city=row["city"],
					state_name=row["state_name"],
					zip=row["zip"],
					lat=row["lat"],
					lng=row["lng"]
				)
		self.stdout.write(self.style.SUCCESS("Данные о местоположении успешно загружены."))
