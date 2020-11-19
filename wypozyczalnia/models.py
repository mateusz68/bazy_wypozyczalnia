from django.db import models
from accounts.models import Uzytkownik
from django.utils.translation import gettext_lazy as _
# Create your models here.


class SamochodMarka(models.Model):
    nazwa = models.CharField(max_length=50, null=False)


class SamochodModel(models.Model):
    nazwa = models.CharField(max_length=50, null=False)
    marka = models.ForeignKey(SamochodMarka, on_delete=models.CASCADE)


class SamochodSkrzynia(models.Model):
    nazwa = models.CharField(max_length=50, null=False)


class SamochodSilnik(models.Model):
    nazwa = models.CharField(max_length=50, null=False)


class SamochodKategoria(models.Model):
    nazwa = models.CharField(max_length=50, null=False)


class Samochod(models.Model):
    class StatusSamochod(models.TextChoices):
        DOSTEPNY = 'DO', _('Dostępny')
        NIEDOSTEPNY = 'NI', _('Niedostępny')
        SERWISOWANY = 'SE', _('Serwisowany')

    numer_rejestracyjny = models.CharField(max_length=50, null=False)
    kolor = models.CharField(max_length=50, null=True)
    pojemnosc_silnika = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    moc_silnika = models.IntegerField(null=True)
    cena_godzina = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    cena_dzien = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    kaucja = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    model = models.ForeignKey(SamochodModel, on_delete=models.CASCADE)
    kategoria = models.ForeignKey(SamochodKategoria, on_delete=models.RESTRICT, null=False)
    silnik = models.ForeignKey(SamochodSilnik, on_delete=models.RESTRICT, null=False)
    skrzynia = models.ForeignKey(SamochodSkrzynia, on_delete=models.RESTRICT, null=False)
    status_samochodu = models.CharField(max_length=2, choices=StatusSamochod.choices, default=StatusSamochod.DOSTEPNY, null=False)

    def __str__(self):
        return self.model.marka.nazwa + self.model.nazwa + "(" + self.numer_rejestracyjny + ")"


class TypUbezpieczenia(models.Model):
    variant = models.CharField(max_length=50, null=False)


class Ubezpieczenie(models.Model):
    numer_polisy = models.CharField(max_length=50, null=False)
    cena = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    typ = models.ForeignKey(TypUbezpieczenia, on_delete=models.RESTRICT, null=False)


class Rezerwacja(models.Model):
    class StatusRezerwacji(models.TextChoices):
        WERYFIKACJA = 'WE', _('Werfyfikacja')
        ZAAKCEPTOWANA = 'ZA', _('Zaakceptowana')
        ANULOWANA = 'AN', _('Anulowana')
        WTRAKCIE = 'WT', _('W trakcie')
        ZAKONCZONA = 'ZK', _('Zakończona')

    data_od = models.DateTimeField(null=False)
    data_do = models.DateTimeField(null=False)
    uwagi = models.CharField(max_length=200, null=True)
    ubezpieczenie = models.OneToOneField(Ubezpieczenie, on_delete=models.RESTRICT, null=False)
    status_rezerwacji = models.CharField(max_length=2, choices=StatusRezerwacji.choices, default=StatusRezerwacji.WERYFIKACJA, null=False)
    samochod = models.ForeignKey(Samochod, on_delete=models.RESTRICT, null=False)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)


class Dokument(models.Model):
    class DokumentTyp(models.TextChoices):
        FAKTURA = 'FV', _('FAKTURA')
        RACHUNEK = 'RA', _('RACHUNEK')
        POTWIERDZENIE = 'PO', _('POTWIERDZENIE')

    kwota = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    typ = models.CharField(max_length=2, choices=DokumentTyp.choices, default=DokumentTyp.POTWIERDZENIE, null=False)
    rezerwacja = models.ForeignKey(Rezerwacja, on_delete=models.CASCADE)


class DodatkoweOplaty(models.Model):
    rodzaj = models.CharField(max_length=50, null=False)
    wysokosc = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    dokument = models.ForeignKey(Dokument, on_delete=models.CASCADE)


class PlatnoscTyp(models.Model):
    typ = models.CharField(max_length=50, null=False)


class Platnosc(models.Model):
    data = models.DateTimeField(null=False)
    wysokosc = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    typ = models.ForeignKey(PlatnoscTyp, on_delete=models.RESTRICT, null=False)