from rest_framework import serializers

from fuel import models


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PriceTable
        fields = ('id_fuel', 'id_region', 'id_fuel_operator', 'date', 'price')