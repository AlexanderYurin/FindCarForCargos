import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.models import Cargo


@pytest.mark.django_db
def test_create_cargo_valid(create_location):
	client = APIClient()
	location = create_location()
	url = reverse("cargo-list")
	data = {
		"pick_up": location.zip,
		"delivery": location.zip,
		"weight": 120
	}
	response = client.post(path=url,
						   data=data,
						   format="json")
	cargos = Cargo.objects.all()

	assert response.status_code == 201
	assert len(cargos) == 1


@pytest.mark.django_db
def test_retrieve_cargo(create_cargo):
	cargo = create_cargo()
	client = APIClient()
	url = reverse("cargo-detail", kwargs={"pk": cargo.pk})
	response = client.get(url)
	assert response.status_code == 200


@pytest.mark.django_db
def test_update_cargo(create_cargo):
	cargo = create_cargo()
	client = APIClient()
	url = reverse("cargo-detail", kwargs={"pk": cargo.pk})
	data = {
		"weight": 200,
		"description": "Test"
	}
	response = client.put(
		path=url,
		data=data,
		format="json")
	assert response.status_code == 200
	cargo.refresh_from_db()
	assert cargo.weight == 200
	assert cargo.description == "Test"


@pytest.mark.django_db
def test_delete_cargo(create_cargo):
	cargo = create_cargo()
	client = APIClient()
	url = reverse("cargo-detail", kwargs={'pk': cargo.pk})
	response = client.delete(url)
	assert response.status_code == 204
	assert Cargo.objects.count() == 0


@pytest.mark.django_db
def test_update_car(create_car, create_location):
	location = create_location(zip="12313")
	car = create_car()
	client = APIClient()
	url = reverse("car-detail", kwargs={"pk": car.pk})
	data = {"weight": 200,
			"current_location": "12313"}
	response = client.put(url, data, format='json')
	assert response.status_code == 200
	car.refresh_from_db()
	assert car.weight == 200
