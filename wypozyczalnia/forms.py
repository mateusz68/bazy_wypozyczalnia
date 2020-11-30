from django import forms
from django.contrib import admin
from django.db.models import Q
from django.shortcuts import get_object_or_404

from wypozyczalnia.models import *


class RezerwacjaForm(forms.ModelForm):
    class Meta:
        model: Rezerwacja
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        data_do = cleaned_data.get('data_do')
        data_od = cleaned_data.get('data_od')
        if data_od > data_do:
            raise forms.ValidationError('Błędny zakres dat. Data zakończenia rezerwacji musi być większa od daty rozpoczecia rezerwacji!')
        samochod = cleaned_data.get('samochod')
        # temp = Rezerwacja.objects.filter(samochod_id=samochod.id, data_do__range=(data_od, data_do), data_od__range=(data_od, data_do))
        temp = Rezerwacja.objects.filter((Q(data_do__range=(data_od, data_do)) | Q(data_od__range=(data_od, data_do))) & Q(
            samochod_id=self.samochod_val.id))
        if len(temp) != 0:
            raise forms.ValidationError('Błędny zakres dat. Inne wypożyczenie jest już w tym przedziale!')
        return cleaned_data


class RezerwacjaAdmin(admin.ModelAdmin):
    form = RezerwacjaForm
    # list_display = ('data_od', 'data_do')


class RezerwacjaUserForm(forms.ModelForm):
    typ_ubezpieczenie = forms.Select()

    def __init__(self, *args, key, **kwargs):
        print(key)
        super(RezerwacjaUserForm, self).__init__(*args, **kwargs)
        samochod = Samochod.objects.filter(pk=key)
        self.samochod_val = Samochod.objects.get(pk=key)
        typy = TypUbezpieczenia.objects.all()
        self.fields['typ_ubezpieczenie'] = forms.ChoiceField(choices=((x.id, x) for x in typy),
                                                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Rezerwacja
        fields = ['data_od', 'data_do', 'uwagi']
        widgets = {
            'data_od': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_do': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'uwagi': forms.TextInput(attrs={'class': 'form-control'}),
            'samochod': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_do = cleaned_data.get('data_do')
        data_od = cleaned_data.get('data_od')
        if data_od > data_do:
            raise forms.ValidationError({'data_do': 'Błędny zakres dat. Data zakończenia rezerwacji musi być większa od daty rozpoczecia rezerwacji!'})
        # samochod = cleaned_data.get('samochod')
        # temp = Rezerwacja.objects.filter(Q(data_do__range=(data_od, data_do)) | Q(data_od__range=(data_od, data_do)))
        samochod = cleaned_data.get('samochod')
        temp = Rezerwacja.objects.filter((Q(data_do__range=(data_od, data_do)) | Q(data_od__range=(data_od, data_do))) &Q(samochod_id=self.samochod_val.id) )
        if len(temp) != 0:
            raise forms.ValidationError({'data_do': 'Błędny zakres dat. Inna rezerwacja jest już w tym przedziale czasowym!'})
        return cleaned_data