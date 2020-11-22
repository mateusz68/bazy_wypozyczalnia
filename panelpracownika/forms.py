from django import forms
from django.forms import ModelForm
from wypozyczalnia.models import *


class UbezpieczenieTypForm(ModelForm):
    class Meta:
        model = TypUbezpieczenia
        fields = ['variant']
        widgets = {
            'variant': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UbezpieczenieTypDeleteForm(ModelForm):
    class Meta:
        model = TypUbezpieczenia
        fields = []


class ModelForm(ModelForm):
    class Meta:
        model = SamochodModel
        fields = ['nazwa', 'marka']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
            'marka': forms.Select(attrs={'class': 'form-control'}),
        }


class ModelDeleteForm(ModelForm):
    class Meta:
        model = SamochodModel
        fields = []


class MarkaForm(ModelForm):
    class Meta:
        model = SamochodMarka
        fields = ['nazwa']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MarkaDeleteForm(ModelForm):
    class Meta:
        model = SamochodMarka
        fields = []


class KategoriaSamochoduForm(ModelForm):
    class Meta:
        model = SamochodKategoria
        fields = ['nazwa']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
        }


class KategoriaSamochoduDeleteForm(ModelForm):
    class Meta:
        model = SamochodKategoria
        fields = []


class SilnikSamochodForm(ModelForm):
    class Meta:
        model = SamochodSilnik
        fields = ['nazwa']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SilnikSamochodDeleteForm(ModelForm):
    class Meta:
        model = SamochodSilnik
        fields = []

class SkrzyniaSamochodForm(ModelForm):
    class Meta:
        model = SamochodSkrzynia
        fields = ['nazwa']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SkrzyniaSamochodDeleteForm(ModelForm):
    class Meta:
        model = SamochodSkrzynia
        fields = []
