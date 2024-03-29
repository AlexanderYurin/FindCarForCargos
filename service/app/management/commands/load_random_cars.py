import random
import string

from django.core.management.base import BaseCommand

from app.models import Car


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for _ in range(40):
            number = f"{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}"
            Car.objects.create(
                number=number,
                weight=random.randint(1, 1000)

            )
        self.stdout.write(self.style.SUCCESS("Машины успешно созданы."))