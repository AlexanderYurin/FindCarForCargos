import pytest

from app.serializers import CargoSerializers, CarSerializers


@pytest.mark.django_db
def test_cargo_serializer_create_valid(create_location):
	location = create_location()

	cargo_data = {
		"pick_up": location.zip,
		"delivery": location.zip,
		"weight": 100,
		"description": "Test cargo"
	}
	serializer = CargoSerializers(data=cargo_data)
	assert serializer.is_valid()


@pytest.mark.django_db
def test_cargo_serializer_create_invalid_zip(create_location):
	location = create_location()
	cargo_data = {
		"pick_up": "123123",
		"delivery": "123123",
		"weight": 100,
		"description": "Test cargo"
	}
	serializer = CargoSerializers(data=cargo_data)
	assert not serializer.is_valid()
	assert "pick_up" in serializer.errors
	assert "delivery" in serializer.errors


@pytest.mark.django_db
def test_car_serializer_update(create_car, create_location):
	location = create_location(
			zip="12347",
			lat="1.234568",
			lng="5.678909")
	car = create_car()

	car_data = {
		"weight": 600,
		"current_location": location.zip
	}
	serializer = CarSerializers(instance=car, data=car_data)
	assert serializer.is_valid()
	updated_car = serializer.save()
	assert updated_car.weight == 600
	assert updated_car.current_location.zip == location.zip
