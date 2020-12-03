from django_filters.widgets import RangeWidget
from dal import autocomplete

from wypozyczalnia.models import *
import django_filters


class PlatnosciFilter(django_filters.FilterSet):
    data_range = django_filters.DateTimeFromToRangeFilter(field_name='data',
                                                         label='Data (przedział)',
                                                         widget=RangeWidget(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Platnosc
        fields = ['typ']


class UbezpieczeniaFilter(django_filters.FilterSet):
    class Meta:
        model = Ubezpieczenie
        fields = ['typ']


class DodatkoweOplatyFilter(django_filters.FilterSet):
    dokument = django_filters.ModelChoiceFilter(field_name='dokument', queryset=Dokument.objects.all())

    class Meta:
        model = DodatkoweOplaty
        fields = ['dokument']
        # widgets = {
        #     'dokument': autocomplete.ModelSelect2(url='panelpracownika:user_autocomplete')
        # }


class DokumentyFilter(django_filters.FilterSet):
    class Meta:
        model = Dokument
        fields = ['typ', 'rezerwacja']


class RezerwacjaFilter(django_filters.FilterSet):
    data_od_range = django_filters.DateTimeFromToRangeFilter(field_name='data_od',
                                                        label='Data od (przedział)', widget=RangeWidget(attrs={'type': 'datetime-local'}))
    data_do_range = django_filters.DateTimeFromToRangeFilter(field_name='data_do',
                                                         label='Data do (przedział)',
                                                         widget=RangeWidget(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Rezerwacja
        fields = ['status_rezerwacji', 'samochod', 'uzytkownik']