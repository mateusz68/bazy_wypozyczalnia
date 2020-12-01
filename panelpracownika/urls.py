from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'panelpracownika'
urlpatterns = [
    # path('', views.home, name='home'),
    # Rezerwacje
    path('rezerwacje', views.rezerwacje, name="rezerwacje"),
    path('rezerwacje/dodaj', views.rezerwacja_dodaj, name="rezerwacja_dodaj"),
    path('rezerwacje/edytuj/<int:pk>', views.rezerwacja_edytuj, name="rezerwacja_edytuj"),
    path('rezerwacje/szczegoly/<int:pk>', views.rezerwacja_szczegoly, name="rezerwacja_szczegoly"),
    path('rezerwacje/zmien_status/<int:pk>', views.rezerwacja_zmien_stan, name="rezerwacja_zmien_stan"),
    path('rezerwacje/usun/<int:pk>', views.rezerwacje_usun, name="rezerwacje_usun"),
    path('rezerwacje/dodaj_platnosc', views.dodaj_platnosc_rezerwacja, name="dodaj_platnosc_rezerwacja"),
    path('rezerwacje/test/<int:pk>', views.test, name="test"),
    # Modele Samochodów
    path('samochod', views.samochod, name="samochod"),
    path('samochod/dodaj', views.samochod_dodaj, name="samochod_dodaj"),
    path('samochod/edytuj/<int:pk>', views.samochod_edytuj, name="samochod_edytuj"),
    path('samochod/usun/<int:pk>', views.samochod_usun, name="samochod_usun"),
    # Typ Ubezpieczenia
    path('typ_ubezpieczenia', views.typ_ubezpieczenia, name="typ_ubezpieczenia"),
    path('typ_ubezpieczenia/dodaj', views.typ_ubezpieczenia_dodaj, name="typ_ubezpieczenia_dodaj"),
    path('typ_ubezpieczenia/edytuj/<int:pk>', views.typ_ubezpieczenia_edytuj, name="typ_ubezpieczenia_edytuj"),
    path('typ_ubezpieczenia/usun/<int:pk>', views.typ_ubezpieczenia_usun, name="typ_ubezpieczenia_usun"),
    # Ubezpieczenie
    path('ubezpieczenie', views.ubezpieczenie, name="ubezpieczenie"),
    path('ubezpieczenie/dodaj', views.ubezpieczenie_dodaj, name="ubezpieczenie_dodaj"),
    path('ubezpieczenie/edytuj/<int:pk>', views.ubezpieczenie_edytuj, name="ubezpieczenie_edytuj"),
    path('ubezpieczenie/usun/<int:pk>', views.ubezpieczenie_usun, name="ubezpieczenie_usun"),
    # Dodatkowe Opłaty
    path('dodatkowe_oplaty', views.dodatkowe_oplaty, name="dodatkowe_oplaty"),
    path('dodatkowe_oplaty/dodaj', views.dodatkowe_oplaty_dodaj, name="dodatkowe_oplaty_dodaj"),
    path('dodatkowe_oplaty/edytuj/<int:pk>', views.dodatkowe_oplaty_edytuj, name="dodatkowe_oplaty_edytuj"),
    path('dodatkowe_oplaty/usun/<int:pk>', views.dodatkowe_oplaty_usun, name="dodatkowe_oplaty_usun"),
    # Dokument
    path('dokumenty', views.dokumenty, name="dokumenty"),
    path('dokumenty/dodaj', views.dokumenty_dodaj, name="dokumenty_dodaj"),
    path('dokumenty/edytuj/<int:pk>', views.dokumenty_edytuj, name="dokumenty_edytuj"),
    path('dokumenty/usun/<int:pk>', views.dokumenty_usun, name="dokumenty_usun"),
    # Platnosc
    path('platnosc', views.platnosc, name="platnosc"),
    path('platnosc/dodaj', views.platnosc_dodaj, name="platnosc_dodaj"),
    path('platnosc/edytuj/<int:pk>', views.platnosc_edytuj, name="platnosc_edytuj"),
    path('platnosc/usun/<int:pk>', views.platnosc_usun, name="platnosc_usun"),
    # Modele Samochodów
    path('model', views.model, name="model"),
    path('model/dodaj', views.model_dodaj, name="model_dodaj"),
    path('model/edytuj/<int:pk>', views.model_edytuj, name="model_edytuj"),
    path('model/usun/<int:pk>', views.model_usun, name="model_usun"),
    # Marki samochodów
    path('marka', views.marka, name="marka"),
    path('marka/dodaj', views.marka_dodaj, name="marka_dodaj"),
    path('marka/edytuj/<int:pk>', views.marka_edytuj, name="marka_edytuj"),
    path('marka/usun/<int:pk>', views.marka_usun, name="marka_usun"),
    # Kategorie samochodów
    path('samochod_kategoria', views.samochod_kategoria, name="samochod_kategoria"),
    path('samochod_kategoria/dodaj', views.samochod_kategoria_dodaj, name="samochod_kategoria_dodaj"),
    path('samochod_kategoria/edytuj/<int:pk>', views.samochod_kategoria_edytuj, name="samochod_kategoria_edytuj"),
    path('samochod_kategoria/usun/<int:pk>', views.samochod_kategoria_usun, name="samochod_kategoria_usun"),
    # Typ silnika samochodów
    path('samochod_silnik', views.samochod_silnik, name="samochod_silnik"),
    path('samochod_silnik/dodaj', views.samochod_silnik_dodaj, name="samochod_silnik_dodaj"),
    path('samochod_silnik/edytuj/<int:pk>', views.samochod_silnik_edytuj, name="samochod_silnik_edytuj"),
    path('samochod_silnik/usun/<int:pk>', views.samochod_silnik_usun, name="samochod_silnik_usun"),
    # Typ skrzyni biegów samochodu
    path('samochod_skrzynia', views.samochod_skrzynia, name="samochod_skrzynia"),
    path('samochod_skrzynia/dodaj', views.samochod_skrzynia_dodaj, name="samochod_skrzynia_dodaj"),
    path('samochod_skrzynia/edytuj/<int:pk>', views.samochod_skrzynia_edytuj, name="samochod_skrzynia_edytuj"),
    path('samochod_skrzynia/usun/<int:pk>', views.samochod_skrzynia_usun, name="samochod_skrzynia_usun"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
