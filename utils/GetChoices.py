from fuel import models


class Choices:
    """
        Create data for the select forms
    """
    @classmethod
    def fuel_choices(cls, nothing: bool = False) -> list:
        fuel = models.Fuel.objects.values_list('id', 'name').all()
        fuel_choices_list = [itm for itm in fuel]
        if nothing:
            fuel_choices_list.append((0, '-'))
        return fuel_choices_list

    @classmethod
    def fuel_operator_choices(cls, nothing: bool = False) -> list:
        fuel_operator = models.FuelOperator.objects.values_list('id', 'name').all()
        fuel_operator_choices_list = [itm for itm in fuel_operator]
        if nothing:
            fuel_operator_choices_list.append((0, '-'))
        return fuel_operator_choices_list

    @classmethod
    def region_choices(cls, nothing: bool = False) -> list:
        region = models.Region.objects.values_list('id', 'name').all()
        region_choices_list = [itm for itm in region]
        if nothing:
            region_choices_list.append((0, '-'))
        return region_choices_list
