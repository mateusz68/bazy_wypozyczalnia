from django import forms
from django.forms import ModelForm
from wypozyczalnia.models import *


class CustomForm(ModelForm):

    def __init__(self, key, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        print(key)
        dokumenty = Dokument.objects.filter(rezerwacja_id=key)
        self.fields['dokument'] = forms.ChoiceField(choices=( (x.id, x) for x in dokumenty), widget=forms.Select(attrs={'class' : 'form-control'}))

    class Meta:
        model = Platnosc
        fields = ['data', 'wysokosc', 'typ', 'dokument']
        widgets = {
            'data': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'wysokosc': forms.NumberInput(attrs={'class': 'form-control'}),
            'typ': forms.Select(attrs={'class': 'form-control'}),
            # 'dokument': forms.Select(attrs={'class': 'form-control'}),
        }


class RezerwacjaForm(ModelForm):
    class Meta:
        model = Rezerwacja
        fields = ['data_od', 'data_do', 'uwagi', 'ubezpieczenie', 'status_rezerwacji', 'samochod', 'uzytkownik']
        widgets = {
            'data_od': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'data_do': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'uwagi': forms.TextInput(attrs={'class': 'form-control'}),
            'ubezpieczenie': forms.Select(attrs={'class': 'form-control'}),
            'status_rezerwacji': forms.Select(attrs={'class': 'form-control'}),
            'samochod': forms.Select(attrs={'class': 'form-control'}),
            'uzytkownik': forms.Select(attrs={'class': 'form-control'}),
        }



class RezerwacjaDeleteForm(ModelForm):
    class Meta:
        model = Rezerwacja
        fields = []


class DokumentForm(ModelForm):
    class Meta:
        model = Dokument
        fields = ['kwota', 'typ', 'rezerwacja']
        widgets = {
            'kwota': forms.NumberInput(attrs={'class': 'form-control'}),
            'typ': forms.Select(attrs={'class': 'form-control'}),
            'rezerwacja': forms.Select(attrs={'class': 'form-control'}),
        }


class DokumentDeleteForm(ModelForm):
    class Meta:
        model = Dokument
        fields = []


class DodatkoweOplatyForm(ModelForm):
    class Meta:
        model = DodatkoweOplaty
        fields = ['rodzaj', 'wysokosc', 'dokument']
        widgets = {
            'rodzaj': forms.TextInput(attrs={'class': 'form-control'}),
            'wysokosc': forms.NumberInput(attrs={'class': 'form-control'}),
            'dokument': forms.Select(attrs={'class': 'form-control'}),
        }


class DodatkoweOplatyDeleteForm(ModelForm):
    class Meta:
        model = DodatkoweOplaty
        fields = []


class RezerwacjeDeleteForm(ModelForm):
    class Meta:
        model = Rezerwacja
        fields = []


class RezerwacjeZmienStatusForm(ModelForm):
    class Meta:
        model = Rezerwacja
        fields = ['status_rezerwacji']
        widgets = {
            'status_rezerwacji': forms.Select(attrs={'class': 'form-control'}),
        }

class PlatnoscForm(ModelForm):
    class Meta:
        model = Platnosc
        fields = ['data', 'wysokosc', 'typ', 'dokument']
        widgets = {
            'data': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'wysokosc': forms.NumberInput(attrs={'class': 'form-control'}),
            'typ': forms.Select(attrs={'class': 'form-control'}),
            'dokument': forms.Select(attrs={'class': 'form-control'}),
        }


class PlatnoscDeleteForm(ModelForm):
    class Meta:
        model = Dokument
        fields = []


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


class UbezpieczenieForm(ModelForm):
    class Meta:
        model = Ubezpieczenie
        fields = ['numer_polisy', 'cena', 'typ']
        widgets = {
            'numer_polisy': forms.NumberInput(attrs={'class': 'form-control'}),
            'cena': forms.NumberInput(attrs={'class': 'form-control'}),
            'typ': forms.Select(attrs={'class': 'form-control'}),
        }


class UbezpieczenieDeleteForm(ModelForm):
    class Meta:
        model = Ubezpieczenie
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


class SamochodForm(ModelForm):
    class Meta:
        model = Samochod
        fields = ['numer_rejestracyjny', 'kolor', 'pojemnosc_silnika', 'moc_silnika', 'cena_godzina', 'cena_dzien', 'kaucja', 'model', 'kategoria', 'silnik', 'skrzynia', 'status_samochodu']
        widgets = {
            'numer_rejestracyjny': forms.TextInput(attrs={'class': 'form-control'}),
            'kolor': forms.TextInput(attrs={'class': 'form-control'}),
            'pojemnosc_silnika': forms.NumberInput(attrs={'class': 'form-control'}),
            'moc_silnika': forms.NumberInput(attrs={'class': 'form-control'}),
            'cena_godzina': forms.NumberInput(attrs={'class': 'form-control'}),
            'cena_dzien': forms.NumberInput(attrs={'class': 'form-control'}),
            'kaucja': forms.NumberInput(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'kategoria': forms.Select(attrs={'class': 'form-control'}),
            'silnik': forms.Select(attrs={'class': 'form-control'}),
            'skrzynia': forms.Select(attrs={'class': 'form-control'}),
            'status_samochodu': forms.Select(attrs={'class': 'form-control'}),
        }


class SamochodDeleteForm(ModelForm):
    class Meta:
        model = Samochod
        fields = []