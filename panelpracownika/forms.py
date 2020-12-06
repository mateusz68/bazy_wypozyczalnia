from django import forms
from django.db.models import Q
from django.forms import ModelForm
from wypozyczalnia.models import *


class DodajPlatnoscZamownie(ModelForm):
    class Meta:
        model = Platnosc
        fields = ['data', 'wysokosc', 'typ']
        widgets = {
            'data': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'wysokosc': forms.NumberInput(attrs={'class': 'form-control'}),
            'typ': forms.Select(attrs={'class': 'form-control'}),
        }


class RezerwacjaEditForm(ModelForm):
    def __init__(self, *args, key, **kwargs):
        super(RezerwacjaEditForm, self).__init__(*args, **kwargs)
        self.key = key

    class Meta:
        model = Rezerwacja
        fields = ['data_od', 'data_do', 'uwagi', 'samochod', 'uzytkownik']
        widgets = {
            'data_od': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'data_do': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'uwagi': forms.TextInput(attrs={'class': 'form-control'}),
            'samochod': forms.Select(attrs={'class': 'form-control'}),
            'uzytkownik': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_do = cleaned_data.get('data_do')
        data_od = cleaned_data.get('data_od')
        if data_od > data_do:
            raise forms.ValidationError({'data_do': 'Błędny zakres dat. Data zakończenia rezerwacji musi być większa od daty rozpoczecia rezerwacji!'})
        samochod = cleaned_data.get('samochod')
        temp = Rezerwacja.objects.filter(
            (Q(data_do__range=(data_od, data_do)) | Q(data_od__range=(data_od, data_do))) & Q(
                samochod_id=samochod.id) & ~Q(pk=self.key))
        if len(temp) != 0:
            raise forms.ValidationError({'data_do': 'Błędny zakres dat. Inne wypożyczenie jest już w tym przedziale!'})
        return cleaned_data


class RezerwacjaForm(ModelForm):
    typ_ubezpieczenie = forms.Select()
    def __init__(self, *args, **kwargs):
        super(RezerwacjaForm, self).__init__(*args, **kwargs)
        typy = TypUbezpieczenia.objects.all()
        self.fields['typ_ubezpieczenie'] = forms.ChoiceField(choices=( (x.id, x) for x in typy), widget=forms.Select(attrs={'class' : 'form-control'}))

    class Meta:
        model = Rezerwacja
        fields = ['data_od', 'data_do', 'uwagi', 'samochod', 'uzytkownik']
        widgets = {
            'data_od': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_do': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'uwagi': forms.TextInput(attrs={'class': 'form-control'}),
            # 'ubezpieczenie': forms.Select(attrs={'class': 'form-control'}),
            # 'status_rezerwacji': forms.Select(attrs={'class': 'form-control'}),
            'samochod': forms.Select(attrs={'class': 'form-control'}),
            'uzytkownik': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_do = cleaned_data.get('data_do')
        data_od = cleaned_data.get('data_od')
        if data_od > data_do:
            raise forms.ValidationError({'data_do': 'Błędny zakres dat. Data zakończenia rezerwacji musi być większa od daty rozpoczecia rezerwacji!'})
        samochod = cleaned_data.get('samochod')
        # temp = Rezerwacja.objects.filter(samochod_id=samochod.id, data_do__range=(data_od, data_do), data_od__range=(data_od, data_do))
        temp = Rezerwacja.objects.filter(
            (Q(data_do__range=(data_od, data_do)) | Q(data_od__range=(data_od, data_do))) & Q(
                samochod_id=samochod))
        if len(temp) != 0:
            raise forms.ValidationError({'data_do': 'Błędny zakres dat. Inne wypożyczenie jest już w tym przedziale!'})
        return cleaned_data


class DokumentForm(ModelForm):
    class Meta:
        model = Dokument
        fields = ['kwota', 'typ', 'rezerwacja']
        widgets = {
            'kwota': forms.NumberInput(attrs={'class': 'form-control'}),
            'typ': forms.Select(attrs={'class': 'form-control'}),
            'rezerwacja': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        rezerwacja = cleaned_data.get('rezerwacja')
        typ = cleaned_data.get('typ')
        dokumenty = Dokument.objects.filter(rezerwacja_id=rezerwacja.id, typ=typ)
        if len(dokumenty) != 0:
            raise forms.ValidationError({'typ': 'Dokument tego typu został już wygenerowany dla tej rezerwacji!'})
        return cleaned_data


class DokumentDeleteForm(ModelForm):
    class Meta:
        model = Dokument
        fields = []


class RezerwacjaDeleteForm(ModelForm):
    class Meta:
        model = Rezerwacja
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
        fields = ['variant', 'stawka']
        widgets = {
            'variant': forms.TextInput(attrs={'class': 'form-control'}),
            'stawka': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UbezpieczenieTypDeleteForm(ModelForm):
    class Meta:
        model = TypUbezpieczenia
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        get_instance = self.instance
        ubezpieczenie = Ubezpieczenie.objects.filter(typ_id=get_instance.id)
        if len(ubezpieczenie) != 0:
            raise forms.ValidationError('Nie można usunąc wybranego typu ubezpieczenia ponieważ jest przypisane do niego ubezpieczenia!')
        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        get_instance = self.instance
        rezerwacja = Rezerwacja.objects.filter(ubezpieczenie_id=get_instance.id)
        if len(rezerwacja) != 0:
            raise forms.ValidationError('Nie można usunąc wybranego ubezpieczenia ponieważ jest przypisana do niego rezerwacja!')
        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        get_instance = self.instance
        samochody = Samochod.objects.filter(kategoria_id=get_instance.id)
        if len(samochody) != 0:
            raise forms.ValidationError('Nie można usunąc wybranej kategorii ponieważ są przypisane do niej samochody!')
        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        get_instance = self.instance
        samochody = Samochod.objects.filter(silnik_id=get_instance.id)
        if len(samochody) != 0:
            raise forms.ValidationError('Nie można usunąc wybranego rodzaju silnika ponieważ są przypisane do niego samochody!')
        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        get_instance = self.instance
        samochody = Samochod.objects.filter(skrzynia_id=get_instance.id)
        if len(samochody) != 0:
            raise forms.ValidationError('Nie można usunąc wybranego rodzaju skrzyni biegów ponieważ są przypisane do niego samochody!')
        return cleaned_data


class SamochodForm(ModelForm):
    class Meta:
        model = Samochod
        fields = ['numer_rejestracyjny', 'zdjecie', 'kolor', 'pojemnosc_silnika', 'moc_silnika', 'cena_godzina', 'cena_dzien', 'kaucja', 'model', 'kategoria', 'silnik', 'skrzynia', 'status_samochodu']
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

    def clean(self):
        cleaned_data = super().clean()
        get_instance = self.instance
        rezerwacja = Rezerwacja.objects.filter(samochod_id=get_instance.id)
        if len(rezerwacja) != 0:
            raise forms.ValidationError('Nie można usunąc wybranego samochodu ponieważ jest przypisana do niego przynajmniej jedna rezerwacja!')
        return cleaned_data