from .models import Samochod
import django_filters


class SamochodFilter(django_filters.FilterSet):
    class Meta:
        model = Samochod
        fields = ['model', 'silnik', 'skrzynia', 'kategoria']