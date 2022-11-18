from django import forms


from fuel import models


class FuelForm(forms.ModelForm):
    name = forms.CharField(max_length=120, label='Name of the fuel')
    type = forms.ChoiceField(choices=models.Fuel.FuelType.choices)

    class Meta:
        model = models.Fuel
        fields = ('name', 'type')


class RegionForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Name of the region')

    class Meta:
        model = models.Region
        fields = ('name', )


class FuelOperatorForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Name of the fuel operator')
    info = forms.CharField(label='Description', widget=forms.Textarea)
    official_site = forms.URLField(max_length=250, label='URL')

    class Meta:
        model = models.FuelOperator
        fields = ('name', 'info', 'official_site')


class UserLogin(forms.Form):
    username = forms.CharField(max_length=120, label='Name')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())