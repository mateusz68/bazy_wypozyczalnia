from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('logowanie', views.login_view, name='logowanie'),
    path('rejestracja', views.register_view, name='rejestracja'),
    path('rejestracja/firma', views.register_firma, name='register_firma'),
    path('rejestracja/uzytkownik', views.register_pry, name='register_pry'),
    path('wyloguj', views.logout_view, name='wyloguj'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)