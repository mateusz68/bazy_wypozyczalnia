from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div
from django_filters.widgets import RangeWidget
from dal import autocomplete
from django_select2.forms import Select2Widget

from wypozyczalnia.models import *
from accounts.models import Uzytkownik
import django_filters

from django_select2 import forms as s2forms


class PlatnosciFilter(django_filters.FilterSet):
    data_range = django_filters.DateTimeFromToRangeFilter(field_name='data',
                                                         label='Data (przedział)',
                                                         widget=RangeWidget(attrs={'class': 'form-control', 'type': 'datetime-local'}))

    class Meta:
        model = Platnosc
        fields = ['typ']



class UbezpieczeniaFilter(django_filters.FilterSet):
    class Meta:
        model = Ubezpieczenie
        fields = ['typ']


class DodatkoweOplatyFilter(django_filters.FilterSet):
    dokument = django_filters.ModelChoiceFilter(
        queryset=Dokument.objects.all(),
        widget=Select2Widget()
    )
    class Meta:
        model = DodatkoweOplaty
        fields = ['dokument']


class DokumentyFilter(django_filters.FilterSet):
    rezerwacja = django_filters.ModelChoiceFilter(
        queryset=Rezerwacja.objects.all(),
        widget=Select2Widget(attrs={'data-width': '100%'})
    )
    class Meta:
        model = Dokument
        fields = ['typ', 'rezerwacja']


class RezerwacjaFilter(django_filters.FilterSet):
    data_od_range = django_filters.DateTimeFromToRangeFilter(field_name='data_od',
                                                        label='Data od (przedział)', widget=RangeWidget(attrs={'class': 'form-control  col-md-6', 'type': 'datetime-local'}))
    data_do_range = django_filters.DateTimeFromToRangeFilter(field_name='data_do',
                                                         label='Data do (przedział)',
                                                         widget=RangeWidget(attrs={'class': 'form-control  col-md-6', 'type': 'datetime-local'}))
    samochod = django_filters.ModelChoiceFilter(
        queryset=Samochod.objects.all(),
        widget=Select2Widget()
    )
    uzytkownik = django_filters.ModelChoiceFilter(
        queryset=Uzytkownik.object.all(),
        widget=Select2Widget()
    )
    class Meta:
        model = Rezerwacja
        fields = ['status_rezerwacji', 'samochod', 'uzytkownik']