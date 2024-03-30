import pytest

from app.models import Car


@pytest.mark.django_db
def test_model_car_number_valid(create_location):
	car = Car.objects.create(number="1233Z", weight="2", current_location=create_location())
	assert car.number == "1233Z"


@pytest.mark.django_db
def test_model_car_number_invalid(create_location):
	car = Car.objects.create(number="1233Z", weight="2", current_location=create_location())
	cars = Car.objects.all()
	assert len(cars) == 1