from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.models import Cargo, Car, Location
from app.serializers import CargoSerializers, CarSerializers


class CargoViewSet(GenericViewSet):
	queryset = cargos = Cargo.objects.prefetch_related(
		Prefetch("pick_up", queryset=Location.objects.all().only("zip", "lat", "lng")),
		Prefetch("delivery", queryset=Location.objects.all().only("zip", "lat", "lng")),
	)
	serializer_class = CargoSerializers

	def list(self, request) -> Response:
		"""
        Получение списка грузов
        (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль))
        """

		instance = self.get_queryset()
		serializer = self.get_serializer(instance, many=True)

		return Response(
			data=serializer.data,
			status=status.HTTP_200_OK
		)

	def create(self, request) -> Response:
		"""
        Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду)
        """
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(data=serializer.data,
						status=status.HTTP_201_CREATED
						)

	def retrieve(self, request, pk=None):
		"""
        Получение информации о конкретном грузе по ID
        (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с
        расстоянием до выбранного груза);
        """
		instance = self.get_object()
		serializer = self.get_serializer(instance)

		return Response(
			data=serializer.data,
			status=status.HTTP_200_OK
		)

	def update(self, request, pk=None):
		"""
        Редактирование груза по ID (вес, описание)
        """
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data, status=status.HTTP_200_OK)

	def destroy(self, request, pk=None):
		"""Удаление груза по ID."""
		cargo = get_object_or_404(Cargo, pk=pk)
		cargo.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	def get_serializer_context(self):
		context = super().get_serializer_context()
		weight = self.request.query_params.get("weight", None)
		all_cars = Car.objects.prefetch_related(
			Prefetch("current_location", queryset=Location.objects.all().only("lng", "lat"))
		)
		if weight:
			all_cars = all_cars.filter(weight__gte=int(weight))
		context["all_cars"] = all_cars

		context["miles"] = self.request.query_params.get("miles", 450)

		return context


class CarViewSet(UpdateModelMixin, GenericViewSet):
	queryset = Car.objects.all().only("current_location", "weight")
	serializer_class = CarSerializers
