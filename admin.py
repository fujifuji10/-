from django.contrib import admin
from .models import(
  Housing, HouseComments, HousingPictures, DetailHouse
)
# Register your models here.

admin.site.register(
  [Housing, HouseComments, HousingPictures, DetailHouse]
)