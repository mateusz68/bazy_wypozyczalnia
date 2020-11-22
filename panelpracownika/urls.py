from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'panelpracownika'
urlpatterns = [
    # path('', views.home, name='home'),
    #Typ Ubezpieczenia
    path('typ_ubezpieczenia', views.typ_ubezpieczenia, name="typ_ubezpieczenia"),
    path('typ_ubezpieczenia/dodaj', views.typ_ubezpieczenia_dodaj, name="typ_ubezpieczenia_dodaj"),
    path('typ_ubezpieczenia/edytuj/<int:pk>', views.typ_ubezpieczenia_edytuj, name="typ_ubezpieczenia_edytuj"),
    path('typ_ubezpieczenia/usun/<int:pk>', views.typ_ubezpieczenia_usun, name="typ_ubezpieczenia_usun"),
    #Modele Samochodów
    path('model', views.model, name="model"),
    path('model/dodaj', views.model_dodaj, name="dodaj_model"),
    path('model/edytuj/<int:pk>', views.model_edytuj, name="edytuj_model"),
    path('model/usun/<int:pk>', views.model_usun, name="usun_model"),
    #Marki samochodów
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
