from django.contrib import admin
from .models import Record, Quarry, Material, TruckNo

admin.site.register(Record)
admin.site.register(Quarry)
admin.site.register(TruckNo)
admin.site.register(Material)

