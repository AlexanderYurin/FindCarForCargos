import random

from django.db import models, OperationalError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import QuerySet


# Create your models here.
# - Груз обязательно должен содержать следующие характеристики:
#     - локация pick-up;
#     - локация delivery;
#     - вес (1-1000);
#     - описание.
# - Машина обязательно должна в себя включать следующие характеристики:
#     - уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце, пример: "1234A", "2534B", "9999Z")
#     - текущая локация;
#     - грузоподъемность (1-1000).
# - Локация должна содержать в себе следующие характеристики:
#     - город;
#     - штат;
#     - почтовый индекс (zip);
#     - широта;
#     - долгота.


class Location(models.Model):
	city = models.CharField(max_length=50)
	state_name = models.CharField(max_length=50)
	zip = models.CharField(max_length=50, db_index=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lng = models.DecimalField(max_digits=9, decimal_places=6)

	def __str__(self):
		return f"{self.zip}"


class Cargo(models.Model):
	pick_up = models.ForeignKey(to="Location", on_delete=models.PROTECT, related_name="cargo_pick_up")
	delivery = models.ForeignKey(to="Location", on_delete=models.PROTECT, related_name="cargo_delivery")
	weight = models.IntegerField(default=1, validators=[MinValueValidator(limit_value=1),
														MaxValueValidator(limit_value=1000)])
	description = models.TextField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f"Груз из {self.pick_up} в {self.delivery}"


class Car(models.Model):
	number = models.CharField(max_length=5,
							  validators=[RegexValidator(regex=r"^[1-9][0-9]{3}[A-Z]$", message="Не верный формат!")],
							  unique=True)

	weight = models.IntegerField(default=1, validators=[MinValueValidator(limit_value=1),
														MaxValueValidator(limit_value=1000)])
	current_location = models.ForeignKey(to="Location",
										 on_delete=models.PROTECT,
										 null=True, blank=True)

	def save(self, *args, **kwargs):
		# Проверяем была ли выбрана локация.
		if not self.current_location_id:
			self.current_location_id = self.random_current_location()
		super().save(*args, **kwargs)

	@staticmethod
	def random_current_location() -> int:
		"""Функция для получения случайной локации для машины, если он не был задан"""
		try:
			locations = Location.objects.all()
			return random.choice(locations).pk
		except OperationalError:
			return

	def __str__(self):
		return f"Номер: {self.number} Вес: {self.weight}"
