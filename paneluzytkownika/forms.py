from django import forms
from django.forms import ModelForm
from wypozyczalnia.models import *


class ZmienDanePrywatna(ModelForm):
    imie = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nazwisko = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Uzytkownik
        fields = ['imie', 'nazwisko', 'ulica', 'miasto', 'kod_pocztowy', 'numer_telefonu']
        widgets = {
            'imie': forms.TextInput(attrs={'class': 'form-control'}),
            'nazwisko': forms.TextInput(attrs={'class': 'form-control'}),
            'ulica': forms.TextInput(attrs={'class': 'form-control'}),
            'miasto': forms.TextInput(attrs={'class': 'form-control'}),
            'kod_pocztowy': forms.TextInput(attrs={'class': 'form-control'}),
            'numer_telefonu': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AnulujRezerwacje(ModelForm):
    class Meta:
        model = Rezerwacja
        fields = []


class ZmienDaneFirma(ModelForm):
    nazwa_firmy = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    numer_nip = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Uzytkownik
        fields = ['numer_nip', 'nazwa_firmy','ulica', 'miasto', 'kod_pocztowy', 'numer_telefonu']
        widgets = {
            'numer_nip': forms.TextInput(attrs={'class': 'form-control'}),
            'nazwa_firmy': forms.NumberInput(attrs={'class': 'form-control'}),
            'ulica': forms.TextInput(attrs={'class': 'form-control'}),
            'miasto': forms.TextInput(attrs={'class': 'form-control'}),
            'kod_pocztowy': forms.TextInput(attrs={'class': 'form-control'}),
            'numer_telefonu': forms.NumberInput(attrs={'class': 'form-control'}),
        }