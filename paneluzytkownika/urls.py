from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from . import views

app_name = 'paneluzytkownika'
urlpatterns = [
    # path('brak_dostepu', views.brak_dostepu, name='brak_dostepu'),
    path('zmien_haslo', views.zmien_haslo, name='zmien_haslo'),
    path('zmien_dane', views.zmien_dane, name='zmien_dane'),
    path('rezerwacje', views.lista_rezerwacji_uzytk, name='lista_rezerwacji_uzytk'),
    path('rezerwacje/szczegoly/<int:pk>', views.szczegoly_rezerwacji_uztk, name='szczegoly_rezerwacji_uztk'),
    path('rezerwacje/anuluj/<int:pk>', views.rezerwacja_anuluj, name='rezerwacja_anuluj'),
    path('rezerwacje/dokument/faktura/<int:pk>', views.faktura_generuj_pdf, name='faktura_generuj_pdf'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
