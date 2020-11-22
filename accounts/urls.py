from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='logowanie'),
    path('register/', views.register_view, name='rejestracja'),
    path('logout/', views.logout_view, name='wyloguj'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)