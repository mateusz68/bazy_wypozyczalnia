from django.db import models
from accounts.models import Uzytkownik
from django.utils.translation import gettext_lazy as _
# Create your models here.


class SamochodMarka(models.Model):
    nazwa = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Marki Samochodów'


class SamochodModel(models.Model):
    nazwa = models.CharField(max_length=50, null=False)
    marka = models.ForeignKey(SamochodMarka, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' %(self.marka.nazwa, self.nazwa)

    class Meta:
        verbose_name_plural = 'Modele Samochodów'


class SamochodSkrzynia(models.Model):
    nazwa = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Typy Skrzyń Biegów'


class SamochodSilnik(models.Model):
    nazwa = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Typy Silników'


class SamochodKategoria(models.Model):
    nazwa = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Kategorie Samochodów'


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
    zdjecie = models.ImageField(upload_to='uploads/%Y/%m')
    model = models.ForeignKey(SamochodModel, on_delete=models.CASCADE)
    kategoria = models.ForeignKey(SamochodKategoria, on_delete=models.RESTRICT, null=False)
    silnik = models.ForeignKey(SamochodSilnik, on_delete=models.RESTRICT, null=False)
    skrzynia = models.ForeignKey(SamochodSkrzynia, on_delete=models.RESTRICT, null=False)
    status_samochodu = models.CharField(max_length=2, choices=StatusSamochod.choices, default=StatusSamochod.DOSTEPNY, null=False)

    def __str__(self):
        return '%s %s (%s) [Status: %s]' % (self.model.marka, self.model.nazwa, self.numer_rejestracyjny, self.get_status_samochodu_display())

    class Meta:
        verbose_name_plural = 'Samochody'


class TypUbezpieczenia(models.Model):
    variant = models.CharField(max_length=50, null=False)
    stawka = models.IntegerField(null=False, help_text="Jest to procentowy koszt ubezpieczenia w stosunku do całkowitego kosztu wypożyczenia")

    def __str__(self):
        return self.variant

    class Meta:
        verbose_name_plural = 'Typy Ubezpieczeń'


class Ubezpieczenie(models.Model):
    numer_polisy = models.CharField(max_length=50, null=False)
    cena = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    typ = models.ForeignKey(TypUbezpieczenia, on_delete=models.RESTRICT, null=False)

    def __str__(self):
        return '%s %s' %(self.typ.variant, self.numer_polisy)

    def get_koszt(self, koszt):
        return (koszt * self.typ.stawka)/100

    class Meta:
        verbose_name_plural = 'Ubezpieczenia'


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

    def get_czas_trwania(self):
        return self.data_do - self.data_od

    def get_koszt(self):
        liczba = self.get_czas_trwania()
        if liczba.days < 1:
            liczba = int(round(liczba.seconds/3600))
            koszt = liczba * self.samochod.cena_godzina
        else:
            if liczba.seconds/3600 > 3:
                liczba = liczba.days + 1
            else:
                liczba = liczba.days
            koszt = liczba * self.samochod.cena_dzien
        koszt += self.ubezpieczenie.cena
        return koszt

    def calculate_koszt(self):
        liczba = self.get_czas_trwania()
        if liczba.days < 1:
            liczba = int(round(liczba.seconds/3600))
            koszt = liczba * self.samochod.cena_godzina
        else:
            if liczba.seconds/3600 > 3:
                liczba = liczba.days + 1
            else:
                liczba = liczba.days
            koszt = liczba * self.samochod.cena_dzien
        return koszt

    def __str__(self):
        return '%s %s %s [Status: %s]' % (self.uzytkownik, self.samochod, self.pk, self.get_status_rezerwacji_display())

    class Meta:
        verbose_name_plural = 'Rezerwacje'


class Dokument(models.Model):
    class DokumentTyp(models.TextChoices):
        FAKTURA = 'FV', _('FAKTURA')
        KAUCJA = 'KA', _('KAUCJA')

    kwota = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    typ = models.CharField(max_length=2, choices=DokumentTyp.choices, default=DokumentTyp.FAKTURA, null=False)
    rezerwacja = models.ForeignKey(Rezerwacja, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' %(self.get_typ_display(), self.rezerwacja.id)

    class Meta:
        verbose_name_plural = 'Dokumenty'


class DodatkoweOplaty(models.Model):
    rodzaj = models.CharField(max_length=50, null=False)
    wysokosc = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    dokument = models.ForeignKey(Dokument, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' %(self.rodzaj, self.dokument)

    class Meta:
        verbose_name_plural = 'Dodatkowe Opłaty'


class PlatnoscTyp(models.Model):
    typ = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.typ

    class Meta:
        verbose_name_plural = 'Typy Płatności'


class Platnosc(models.Model):
    data = models.DateTimeField(null=False)
    wysokosc = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    typ = models.ForeignKey(PlatnoscTyp, on_delete=models.RESTRICT, null=False)
    dokument = models.ForeignKey(Dokument, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '%s %s %s' %(self.typ, self.data, self.dokument.pk)

    class Meta:
        verbose_name_plural = 'Płatności'

