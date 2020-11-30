from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from accounts.models import Uzytkownik
from .forms import *


def zmien_haslo(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'zmien_haslo.html', {
        'form': form
    })


def zmien_dane(request):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    if uzytkownik.czy_firma:
        if request.method == 'POST':
            form = ZmienDaneFirma(request.POST, instance=uzytkownik)
            if form.is_valid():
                form.save()
                return redirect('paneluzytkownika:zmien_dane')
        else:
            form = ZmienDaneFirma(instance=uzytkownik)
        return render(request, 'zmien_dane.html',
                      {'form': form, 'element': uzytkownik, 'title': "Edytuj wybrany dokument",
                       'target': 'paneluzytkownika:zmien_dane'})
    else:
        if request.method == 'POST':
            form = ZmienDanePrywatna(request.POST, instance=uzytkownik)
            if form.is_valid():
                form.save()
                return redirect('paneluzytkownika:zmien_dane')
        else:
            form = ZmienDanePrywatna(instance=uzytkownik)
        return render(request, 'zmien_dane.html',
                      {'form': form, 'element': uzytkownik,  'title': "Edytuj wybrany dokument",
                       'target': 'paneluzytkownika:zmien_dane'})


def lista_rezerwacji_uzytk(request):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    rezerwacje_lista = Rezerwacja.objects.filter(uzytkownik_id=uzytkownik.id).order_by('data_od')
    page = request.GET.get('page', 1)
    paginator = Paginator(rezerwacje_lista, 10)
    try:
        rezerwacje = paginator.page(page)
    except PageNotAnInteger:
        rezerwacje = paginator.page(1)
    except EmptyPage:
        rezerwacje = paginator.page(paginator.num_pages)

    return render(request, 'lista_rezerwacji.html',
                  {'elementy': rezerwacje, 'url': request.path})

def szczegoly_rezerwacji_uztk(request, pk=None):
    rezerwacja = get_object_or_404(Rezerwacja, pk=pk)
    dokumenty = Dokument.objects.filter(rezerwacja_id=pk)

    dokument_platnosc = []
    for dokument in dokumenty:
        platnosci = Platnosc.objects.filter(dokument_id=dokument.id)
        suma = 0
        for platnosc in platnosci:
            suma += platnosc.wysokosc

        temp = {
            'dokument': dokument,
            'platnosci': platnosci,
            'wplacono': suma
        }
        dokument_platnosc.append(temp)

    return render(request, 'rezerwacja_szczegoly_uzytk.html',
                  {'rezerwacja': rezerwacja, 'dokumenty': dokumenty, 'dokument_platnosc': dokument_platnosc})




