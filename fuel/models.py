from django.db import models
from django.utils.translation import gettext_lazy
from django.core.validators import MinValueValidator

from utils.validator import DateValidator


# Create your models here.
class Fuel(models.Model):
    class FuelType(models.TextChoices):
        Petrol = 'Petrol', gettext_lazy('Petrol')
        Diesel = 'Diesel', gettext_lazy('Diesel')
        Gas = 'Gas', gettext_lazy('Gas')

    name = models.CharField(max_length=120, null=False)
    type = models.CharField(max_length=50, choices=FuelType.choices, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Region(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class FuelOperator(models.Model):
    name = models.CharField(max_length=200, null=False)
    info = models.TextField(null=False)
    official_site = models.URLField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PriceTable(models.Model):
    id_fuel = models.ForeignKey(Fuel, null=False, related_name='fuel', on_delete=models.RESTRICT)
    id_region = models.ForeignKey(Region, null=False, related_name='region', on_delete=models.RESTRICT)
    id_fuel_operator = models.ForeignKey(FuelOperator, null=False, related_name='operator', on_delete=models.RESTRICT)
    date = models.DateField(null=False, validators=[DateValidator.date_validator])
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        validators=[MinValueValidator(limit_value=1, message='Price must be greater then 0')]
    )

    class Meta:
        ordering = ['date']


class UpdateDatabase(models.Model):
    id_task = models.CharField(max_length=250, null=False)
    run_date = models.DateField(null=False, validators=[DateValidator.date_validator])
    status = models.CharField(max_length=100, null=False)
