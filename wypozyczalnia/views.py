from django.shortcuts import render, get_object_or_404
from accounts.models import Uzytkownik
from wypozyczalnia.models import TypUbezpieczenia

def index(request):
    return render(request, 'index.html')

