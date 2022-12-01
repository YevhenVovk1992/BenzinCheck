from rest_framework import serializers

from fuel import models


class PriceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    id_fuel = serializers.CharField()
    id_region = serializers.CharField()
    id_fuel_operator = serializers.CharField()
    date = serializers.DateField(read_only=True)
    price = serializers.IntegerField()

    def create(self, validated_data):
        return models.PriceTable.objects.create(
                    id_fuel=models.Fuel.objects.filter(name=validated_data['id_fuel']).first(),
                    id_region=models.Region.objects.filter(name=validated_data["id_region"]).first(),
                    id_fuel_operator=models.FuelOperator.objects.filter(name=validated_data['id_fuel_operator']).first(),
                    date=validated_data["date"],
                    price=validated_data['price']
                )

    def update(self, instance, validated_data):
        instance.id_fuel = models.Fuel.objects.filter(name=validated_data['id_fuel']).first()
        instance.id_region = models.Region.objects.filter(name=validated_data["id_region"]).first()
        instance.id_fuel_operator = models.FuelOperator.objects.filter(name=validated_data['id_fuel_operator']).first()
        instance.date = validated_data["date"]
        instance.price = validated_data['price']
        instance.save()
        return instance


    class Meta:
        model = models.PriceTable
        fields = ('id', 'id_fuel', 'id_region', 'id_fuel_operator', 'date', 'price')