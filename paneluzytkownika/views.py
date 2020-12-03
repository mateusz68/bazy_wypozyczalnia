from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.template.loader import get_template, render_to_string

from .utils import render_to_pdf
from accounts.models import Uzytkownik
from .forms import *


@login_required()
def rezerwacja_anuluj(request, pk=None):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    rezerwacja = get_object_or_404(Rezerwacja, pk=pk)
    if uzytkownik != rezerwacja.uzytkownik:
        return redirect('paneluzytkownika:lista_rezerwacji_uzytk')

    if rezerwacja.status_rezerwacji == Rezerwacja.StatusRezerwacji.WERYFIKACJA or rezerwacja.status_rezerwacji == Rezerwacja.StatusRezerwacji.ZAAKCEPTOWANA:
        if request.method == 'POST':
            form = AnulujRezerwacje(request.POST, instance=rezerwacja)
            if form.is_valid():
                rezerwacja.status_rezerwacji = Rezerwacja.StatusRezerwacji.ANULOWANA
                rezerwacja.save()
                return redirect('paneluzytkownika:lista_rezerwacji_uzytk')
        else:
            form = AnulujRezerwacje(instance=rezerwacja)
        return render(request, 'anuluj_rezerwacja.html',
                      {'form': form, 'element': rezerwacja, 'title': "Anuluj wybraną rezerwację",
                       'target': 'paneluzytkownika:rezerwacja_anuluj'})

    return redirect('paneluzytkownika:lista_rezerwacji_uzytk')


@login_required()
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


@login_required()
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


@login_required()
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


@login_required()
def szczegoly_rezerwacji_uztk(request, pk=None):
    rezerwacja = get_object_or_404(Rezerwacja, pk=pk)
    dokumenty = Dokument.objects.filter(rezerwacja_id=pk)

    dokument_platnosc = []
    for dokument in dokumenty:
        platnosci = Platnosc.objects.filter(dokument_id=dokument.id)
        dodatki = DodatkoweOplaty.objects.filter(dokument_id=dokument.id)
        suma = 0
        koszt = dokument.kwota
        if dokument.typ == Dokument.DokumentTyp.FAKTURA:
            koszt = koszt + dokument.rezerwacja.ubezpieczenie.cena
        for platnosc in platnosci:
            suma += platnosc.wysokosc
        for dodatek in dodatki:
            koszt += dodatek.wysokosc
        temp = {
            'dokument': dokument,
            'platnosci': platnosci,
            'wplacono': suma,
            'koszt': koszt
        }
        dokument_platnosc.append(temp)

    return render(request, 'rezerwacja_szczegoly_uzytk.html',
                  {'rezerwacja': rezerwacja, 'dokumenty': dokumenty, 'dokument_platnosc': dokument_platnosc})


@login_required()
def faktura_generuj_pdf(request, pk=None):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    dokument = get_object_or_404(Dokument, pk = pk)
    dodatki = DodatkoweOplaty.objects.filter(dokument_id=dokument.id)
    if dokument.typ != Dokument.DokumentTyp.FAKTURA:
        return redirect('wypozyczalnia:index')
    if dokument.rezerwacja.uzytkownik != uzytkownik:
        return redirect('wypozyczalnia:index')
    suma = dokument.kwota + dokument.rezerwacja.ubezpieczenie.cena
    for d in dodatki:
        suma = suma + d.wysokosc
    context = {
        "id": dokument.rezerwacja.id,
        "uzytkownik": uzytkownik,
        "samochod_koszt": dokument.kwota,
        "samochod": dokument.rezerwacja.samochod.model,
        "ubezpieczenie": dokument.rezerwacja.ubezpieczenie.typ.variant,
        "ubezpieczenie_koszt": dokument.rezerwacja.ubezpieczenie.cena,
        "dodatki": dodatki,
        "suma": suma,
    }
    pdf = render_to_pdf('pdf/faktura.html', context)
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)


@login_required()
def kaucja_generuj_pdf(request, pk=None):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    dokument = get_object_or_404(Dokument, pk = pk)
    dodatki = DodatkoweOplaty.objects.filter(dokument_id=dokument.id)
    if dokument.typ != Dokument.DokumentTyp.KAUCJA:
        return redirect('wypozyczalnia:index')
    if dokument.rezerwacja.uzytkownik != uzytkownik:
        return redirect('wypozyczalnia:index')
    suma = dokument.kwota
    for d in dodatki:
        suma = suma + d.wysokosc
    context = {
        "id": dokument.rezerwacja.id,
        "uzytkownik": uzytkownik,
        "samochod": dokument.rezerwacja.samochod.model,
        "samochod_koszt": dokument.kwota,
        "dodatki": dodatki,
        "suma": suma,
    }
    pdf = render_to_pdf('pdf/kaucja.html', context)
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)
