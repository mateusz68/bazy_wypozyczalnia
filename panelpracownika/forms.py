from django import forms
from django.forms import ModelForm
from wypozyczalnia.models import TypUbezpieczenia


class UbezpieczenieTypForm(ModelForm):
    class Meta:
        model = TypUbezpieczenia
        fields = ['variant']


class UbezpieczenieTypDeleteForm(ModelForm):
    class Meta:
        model = TypUbezpieczenia
        fields = []
