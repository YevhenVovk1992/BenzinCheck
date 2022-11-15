from fuel import models


class Choices:
    """
        Create data for the select forms
    """
    @classmethod
    def fuel_choices(cls):
        fuel = models.Fuel.objects.values_list('id', 'name').all()
        fuel_choices_list = [itm for itm in fuel]
        return fuel_choices_list

    @classmethod
    def fuel_operator_choices(cls):
        fuel_operator = models.FuelOperator.objects.values_list('id', 'name').all()
        fuel_operator_choices_list = [itm for itm in fuel_operator]
        return fuel_operator_choices_list

    @classmethod
    def region_choices(cls):
        region = models.Region.objects.values_list('id', 'name').all()
        region_choices_list = [itm for itm in region]
        return region_choices_list
