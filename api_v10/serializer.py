from django.utils import timezone
from rest_framework import serializers

from fuel import models


class PriceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)

    def create(self, validated_data):
        return models.PriceTable.objects.create(
                    id_fuel=models.Fuel.objects.filter(name=validated_data['id_fuel']).first(),
                    id_region=models.Region.objects.filter(name=validated_data["id_region"]).first(),
                    id_fuel_operator=models.FuelOperator.objects.filter(name=validated_data['id_fuel_operator']).first(),
                    date=timezone.now().date(),
                    price=validated_data['price']
                )

    class Meta:
        model = models.PriceTable
        fields = ('id', 'id_fuel', 'id_region', 'id_fuel_operator', 'date', 'price')


class HistoryPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PriceTable
        fields = ('id', 'id_fuel', 'id_region', 'id_fuel_operator', 'date', 'price')