from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import Uzytkownik
from wypozyczalnia.models import TypUbezpieczenia
from panelpracownika.forms import UbezpieczenieTypForm, UbezpieczenieTypDeleteForm


def typ_ubezpieczenia(request):
    current_user = request.user.email
    uzytkownik = get_object_or_404(Uzytkownik, email=current_user)
    typ_ubezpieczenia = TypUbezpieczenia.objects.all();
    return render(request, 'typ_ubezpieczenia.html', {'typ_ubezpieczenia': typ_ubezpieczenia, })


def dodaj_typ_ubezpieczenia(request):
    if request.method == 'POST':
        form = UbezpieczenieTypForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:dodaj_typ_ubezpieczenia')
    else:
        form = UbezpieczenieTypForm()
    return render(request, 'typ_ubezpieczenia_dodaj.html', {'form': form})


def edytuj_typ_ubezpieczenia(request, pk=None):
    typ = get_object_or_404(TypUbezpieczenia, pk=pk)
    if request.method == 'POST':
        form = UbezpieczenieTypForm(request.POST, instance=typ)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:edytuj_typ_ubezpieczenia')
    else:
        form = UbezpieczenieTypForm(instance=typ)
    return render(request, 'typ_ubezpieczenia_edytuj.html', {'form': form, 'typ': typ})


def usun_typ_ubezpieczenia(request, pk=None):
    typ = get_object_or_404(TypUbezpieczenia, pk=pk)
    if request.method == 'POST':
        form = UbezpieczenieTypDeleteForm(request.POST, instance=typ)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:dodaj_typ_ubezpieczenia')
    else:
        form = UbezpieczenieTypDeleteForm(instance=typ)
    return render(request, 'typ_ubezpieczenia_usun.html', {'form': form, 'typ': typ})