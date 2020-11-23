from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'wypozyczalnia'
urlpatterns = [
    path('', views.index, name='index'),
    path('brak_dostepu', views.brak_dostepu, name='brak_dostepu')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)