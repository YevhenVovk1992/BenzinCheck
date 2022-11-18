from django.contrib import admin

from fuel.models import FuelOperator, Fuel, Region, PriceTable


# Register your models here.
class FuelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_display_links = ['id', 'name', 'type']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


class FuelOperatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'info', 'official_site']
    list_display_links = ['id', 'name', 'info', 'official_site']


class PriceTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_fuel', 'id_region', 'id_fuel_operator', 'date', 'price']
    list_display_links = ['id', 'id_fuel', 'id_region', 'id_fuel_operator', 'date', 'price']
    list_filter = ['id_fuel', 'id_region', 'id_fuel_operator', 'date']


admin.site.register(Fuel, FuelAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(FuelOperator, FuelOperatorAdmin)
admin.site.register(PriceTable, PriceTableAdmin)
