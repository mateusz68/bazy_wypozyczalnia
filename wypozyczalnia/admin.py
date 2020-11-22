from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.models import Group
# Register your models here.
from accounts.models import Uzytkownik
from .models import *


class UserAdmin(BaseUserAdmin):
    # Formularze do dodawania i zmiany użytkownika
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Pola które wyświetlam
    list_display = ('email', 'imie', 'nazwisko')
    # list_filter = ('admin',)
    fieldsets = (
        ('Ogólne', {'fields': ('email', 'password')}),
        ('Informacje Osobiste', {'fields': ('imie', 'nazwisko')}),
        ('Uprawnienia', {'fields': ('rola',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'rola', 'imie', 'nazwisko')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.site_header = "Wypożyczalnia Samochodów"
admin.site.register(Uzytkownik)
admin.site.register(Rezerwacja)
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