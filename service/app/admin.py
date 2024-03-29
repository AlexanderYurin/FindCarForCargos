from django.contrib import admin

from app.models import Location, Car, Cargo

# Register your models here.
admin.site.register(Location)
admin.site.register(Car)
admin.site.register(Cargo)