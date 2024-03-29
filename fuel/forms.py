from django import forms
from django.contrib.auth.models import User

from fuel import models


class FuelForm(forms.ModelForm):
    name = forms.CharField(
        max_length=120,
        label='Name of the fuel',
        widget=forms.TextInput(attrs={'class': 'form__input'})
    )
    type = forms.ChoiceField(
        choices=models.Fuel.FuelType.choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-inline'})
    )

    class Meta:
        model = models.Fuel
        fields = ('name', 'type')


class RegionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        label='Name of the region',
        widget=forms.TextInput(attrs={'class': 'form__input'})
    )

    class Meta:
        model = models.Region
        fields = ('name', )


class FuelOperatorForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        label='Name of the fuel operator',
        widget=forms.TextInput(attrs={'class': 'form__input'})
    )
    info = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form__input'})
    )
    official_site = forms.URLField(
        max_length=250,
        label='URL',
        widget=forms.TextInput(attrs={'class': 'form__input'})
    )

    class Meta:
        model = models.FuelOperator
        fields = ('name', 'info', 'official_site')


class UserLogin(forms.Form):
    username = forms.CharField(
        max_length=120,
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form__input'})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form__input'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')