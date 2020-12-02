from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
# Register your models here.
from accounts.models import Uzytkownik
from .models import *
from .forms import RezerwacjaAdmin
from accounts.forms import *


class UserAdmin(BaseUserAdmin):
    # Formularze do dodawania i zmiany użytkownika
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Pola które wyświetlam
    list_display = ('email', 'imie', 'nazwisko', 'rola')
    list_filter = ('rola',)
    fieldsets = (
        ('Ogólne', {'fields': ('email', 'password')}),
        ('Informacje Osobiste', {'fields': ('imie', 'nazwisko', 'ulica', 'miasto', 'kod_pocztowy', 'numer_telefonu', 'czy_firma', 'numer_nip', 'nazwa_firmy')}),
        ('Uprawnienia', {'fields': ('rola', 'active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'rola', 'imie', 'nazwisko', 'ulica', 'miasto', 'kod_pocztowy', 'numer_telefonu', 'czy_firma', 'numer_nip', 'nazwa_firmy', 'active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.site_header = "Wypożyczalnia Samochodów"
admin.site.register(Uzytkownik, UserAdmin)
admin.site.register(Rezerwacja, RezerwacjaAdmin)
admin.site.register(Samochod)
admin.site.register(SamochodMarka)
admin.site.register(SamochodModel)
admin.site.register(SamochodSkrzynia)
admin.site.register(SamochodSilnik)
admin.site.register(SamochodKategoria)
admin.site.register(Dokument)
admin.site.register(Platnosc)
admin.site.register(Ubezpieczenie)
admin.site.register(TypUbezpieczenia)
admin.site.register(PlatnoscTyp)

