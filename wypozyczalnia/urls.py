from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from . import views

app_name = 'wypozyczalnia'
urlpatterns = [
    path('', views.index, name='index'),
    path('brak_dostepu', views.brak_dostepu, name='brak_dostepu'),
    path('samochody/szczegoly/<int:pk>', views.szczczegoly_samochodu, name="szczegoly_samochodu"),
    path('samochody/rezerwuj', views.rezerwuj_samochod, name="rezerwuj_samochod"),
    path('samochody', views.samochody_lista, name="lista_samochody"),
    path('kontakt', views.kontakt, name="kontakt"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += [
#         path(r'^media/(?P<patch>.*)$', serve, {
#             'document_root':settings.MEDIA_ROOT,
#         }),
#     ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)