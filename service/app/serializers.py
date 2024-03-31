from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from geopy.distance import distance
from rest_framework import serializers

from app.models import Cargo, Location, Car


def check_zip_in_location(value, *args, **kwargs):
	data = Location.objects.filter(zip=value)
	if not data.exists():
		raise ValidationError(message=f"Локации с таким индексом: {value} не существует!")


class CargoSerializers(serializers.ModelSerializer):
	pick_up = serializers.CharField(source="pick_up.zip", validators=[check_zip_in_location])
	delivery = serializers.CharField(source="delivery.zip", validators=[check_zip_in_location])
	weight = serializers.IntegerField(validators=[MinValueValidator(limit_value=1),
												  MaxValueValidator(limit_value=1000)])
	cars = serializers.SerializerMethodField()

	class Meta:
		model = Cargo
		fields = ("id", "pick_up", "delivery", "weight", "description", "cars")
		read_only_fields = ("pick_up", "delivery")

	def get_cars(self, obj):
		point_cargo = (obj.pick_up.lat, obj.pick_up.lng)
		all_cars = self.context["all_cars"]
		nearest_cars = list(filter(lambda x: distance(
			point_cargo, (x.current_location.lat, x.current_location.lng)).miles <= 450,
								   all_cars))

		if not nearest_cars:
			return "Нет машин поблизости!"
		serializer = CarSerializers(nearest_cars, many=True)
		return serializer.data

	def create(self, validated_data):
		pick_up_zip = validated_data.get("pick_up").get("zip")
		delivery_zip = validated_data.get("delivery").get("zip")
		weight = validated_data["weight"]
		location = Location.objects.filter(zip__in=[pick_up_zip, delivery_zip])

		cargo = Cargo.objects.create(
			pick_up=location.get(zip=pick_up_zip),
			delivery=location.get(zip=delivery_zip),
			weight=weight
		)

		return cargo

	def update(self, instance, validated_data):
		instance.weight = validated_data.get("weight")
		instance.description = validated_data.get("description")
		instance.save()
		return instance


class CarSerializers(serializers.ModelSerializer):
	current_location = serializers.CharField(validators=[check_zip_in_location])

	class Meta:
		model = Car
		fields = "__all__"
		read_only_fields = ("number",)

	def update(self, instance, validated_data):
		instance.weight = validated_data.get("weight")
		new_location_zip = validated_data.get("current_location")
		new_location = Location.objects.get(zip=new_location_zip)
		instance.current_location = new_location
		instance.save()
		return instance