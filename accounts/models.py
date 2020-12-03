from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Użytkownik musi mieć adres email")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.rola = user.RolaUzytkownika.ADMINISTRATOR
        # user.is_superuser = True
        user.save(using=self._db)
        return user


class Uzytkownik(AbstractBaseUser):
    class RolaUzytkownika(models.TextChoices):
        UZYTKOWNIK = 'US', _('Uzytkownik')
        PRACOWNIK = 'PR', _('Pracownik')
        ADMINISTRATOR = 'AD', _('Administrator')

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    imie = models.CharField(max_length=50, null=True, blank=True)
    nazwisko = models.CharField(max_length=50, null=True, blank=True)
    ulica = models.CharField(max_length=50, null=True)
    miasto = models.CharField(max_length=50, null=True)
    kod_pocztowy = models.CharField(max_length=50, null=True)
    numer_telefonu = models.IntegerField(null=True)
    czy_firma = models.BooleanField(null=False, default=False)
    numer_nip = models.IntegerField(null=True, blank=True)
    nazwa_firmy = models.CharField(max_length=50, null=True, blank=True)
    rola = models.CharField(max_length=2, choices=RolaUzytkownika.choices, default=RolaUzytkownika.UZYTKOWNIK, null=False)
    active = models.BooleanField(default=True, null=False)

    USERNAME_FIELD = 'email'

    object = MyAccountManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.rola in [self.RolaUzytkownika.PRACOWNIK, self.RolaUzytkownika.ADMINISTRATOR]:
            return True
        return False

    @property
    def is_admin(self):
        if self.rola == self.RolaUzytkownika.ADMINISTRATOR:
            return True
        return False

    @property
    def is_active(self):
        return self.active

    class Meta:
        verbose_name_plural = "Użytkownicy"
