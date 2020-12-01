from wypozyczalnia.models import Rezerwacja
import django_filters


class RezerwacjaFilter(django_filters.FilterSet):
    class Meta:
        model = Rezerwacja
        fields = ['status_rezerwacji', 'data_od', 'data_do', 'samochod', 'uzytkownik']
