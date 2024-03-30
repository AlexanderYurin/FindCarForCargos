import pytest

from app.models import Location, Car, Cargo


@pytest.fixture
def create_location():
	def _create_location(
			city="Test City",
			state_name="Test State",
			zip="12345",
			lat="1.234567",
			lng="5.678901"):
		return Location.objects.create(
			city=city,
			state_name=state_name,
			zip=zip,
			lat=lat,
			lng=lng
		)

	return _create_location


@pytest.fixture
def create_car(create_location):
	location = create_location()

	def _create_car(number="1234A", weight=500):
		return Car.objects.create(
			number=number,
			weight=weight,
		)

	return _create_car


@pytest.fixture
def create_cargo(create_location):
	location = create_location()

	def _create_cargo(pick_up=location, delivery=location, weight=100):
		return Cargo.objects.create(
			pick_up=pick_up,
			delivery=delivery,
			weight=weight,
		)

	return _create_cargo
