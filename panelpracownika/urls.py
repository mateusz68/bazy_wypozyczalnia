from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'panelpracownika'
urlpatterns = [
    # path('', views.home, name='home'),
    path('typ_ubezpieczenia', views.typ_ubezpieczenia, name="typ_ubezpieczenia"),
    path('typ_ubezpieczenia/dodaj', views.dodaj_typ_ubezpieczenia, name="dodaj_typ_ubezpieczenia"),
    path('typ_ubezpieczenia/edytuj/<int:pk>', views.edytuj_typ_ubezpieczenia, name="edytuj_typ_ubezpieczenia"),
    path('typ_ubezpieczenia/usun/<int:pk>', views.usun_typ_ubezpieczenia, name="usun_typ_ubezpieczenia")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
