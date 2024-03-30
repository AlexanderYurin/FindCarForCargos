from django.urls import path, include
from rest_framework import routers

from app.views import CargoViewSet, CarViewSet


router = routers.DefaultRouter()
router.register(r"cargo", CargoViewSet, basename="cargo")
router.register(r"car", CarViewSet, basename="car")


urlpatterns = [
	path("", include(router.urls))
]
