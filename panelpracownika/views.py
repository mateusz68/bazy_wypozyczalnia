from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from .filters import RezerwacjaFilter
from accounts.models import Uzytkownik
from wypozyczalnia.models import *
from panelpracownika.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utlis import *


def czy_pracownik(user):
    if user.rola == Uzytkownik.RolaUzytkownika.PRACOWNIK or user.rola == Uzytkownik.RolaUzytkownika.ADMINISTRATOR:
        return True
    return False

# TODO: Poprawić bo nie działa
@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dodaj_platnosc_rezerwacja(request):
    pk = request.GET.get('id')
    if pk is None:
        return redirect('panelpracownika:rezerwacje')
    if request.method == 'POST':
        form = DodajPlatnoscZamownie(request.POST, key=pk)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:rezerwacje')
    else:
        form = DodajPlatnoscZamownie(key=pk)
    return render(request, 'dodaj_form.html',
                  {'form': form, 'title': "Dodaj płatność do rezerwacji", 'target': 'panelpracownika:dodaj_platnosc_rezerwacja'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def rezerwacje(request):
    rezerwacje_lista = Rezerwacja.objects.all().order_by('data_od')
    rezerwacje_filter = RezerwacjaFilter(request.GET, queryset=rezerwacje_lista)
    page = request.GET.get('page', 1)
    paginator = Paginator(rezerwacje_filter.qs, 10)
    try:
        rezerwacje = paginator.page(page)
    except PageNotAnInteger:
        rezerwacje = paginator.page(1)
    except EmptyPage:
        rezerwacje = paginator.page(paginator.num_pages)

    return render(request, 'rezerwacje.html',
              {'filter': rezerwacje_filter, 'elementy': rezerwacje, 'url': request.path, 'title': 'Zarządzaj rezerwacjami'})


# TODO: Poprawić wyświetlanie dokumentów i płatności
@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def rezerwacja_szczegoly(request, pk=None):
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

    return render(request, 'rezerwacja_szczegoly.html',
              {'rezerwacja': rezerwacja, 'dokumenty':dokumenty, 'dokument_platnosc': dokument_platnosc})



@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def rezerwacja_zmien_stan(request, pk=None):
    rezerwacja = get_object_or_404(Rezerwacja, pk=pk)
    if request.method == 'POST':
        form = RezerwacjeZmienStatusForm(request.POST, instance=rezerwacja)
        if form.is_valid():
            form.save()
            if form.cleaned_data.get("status_rezerwacji") == Rezerwacja.StatusRezerwacji.ZAAKCEPTOWANA:
                dokument_temp = Dokument.objects.filter(rezerwacja_id=rezerwacja.id, typ=Dokument.DokumentTyp.KAUCJA)
                print("if zakceptopwana")
                print(dokument_temp)
                if len(dokument_temp) == 0:
                    print("drugi if")
                    dokument = Dokument(typ=Dokument.DokumentTyp.KAUCJA)
                    dokument.kwota = rezerwacja.samochod.kaucja
                    dokument.rezerwacja_id = rezerwacja.id
                    dokument.save()

            if form.cleaned_data.get("status_rezerwacji") == Rezerwacja.StatusRezerwacji.ZAKONCZONA:
                dokument_temp = Dokument.objects.filter(rezerwacja_id=rezerwacja.id, typ=Dokument.DokumentTyp.FAKTURA)
                if(len(dokument_temp) == 0):
                    dokument = Dokument(typ=Dokument.DokumentTyp.FAKTURA)
                    dokument.kwota = rezerwacja.get_koszt()
                    dokument.rezerwacja_id = rezerwacja.id
                    dokument.save()
            print(form.cleaned_data.get("status_rezerwacji"))
            return redirect('panelpracownika:rezerwacje')
    else:
        form = RezerwacjeZmienStatusForm(instance=rezerwacja)
    return render(request, 'edytuj_form.html', {'form': form, 'element': rezerwacja,  'title': "Zmień status rezerwacji", 'target': 'panelpracownika:rezerwacja_zmien_stan'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def rezerwacja_edytuj(request, pk=None):
    rezerwacja = get_object_or_404(Rezerwacja, pk=pk)
    if request.method == 'POST':
        form = RezerwacjaEditForm(request.POST, instance=rezerwacja, key=rezerwacja.id)
        if form.is_valid():
            form.save()
            calculate_cost(rezerwacja.id)
            return redirect('panelpracownika:rezerwacje')
    else:
        form = RezerwacjaEditForm(instance=rezerwacja, key=rezerwacja.id)
    return render(request, 'edytuj_form.html', {'form': form,  'element': rezerwacja, 'title': "Edytuj wybraną rezerwację", 'target': 'panelpracownika:rezerwacja_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def rezerwacja_dodaj(request):
    if request.method == 'POST':
        form = RezerwacjaForm(request.POST)
        if form.is_valid():
            rezerwacja = form.save()
            ubezpieczenie = Ubezpieczenie(cena=100, typ_id=form.cleaned_data.get('typ_ubezpieczenie'))
            ubezpieczenie.save()
            rezerwacja.ubezpieczenie_id = ubezpieczenie.id
            rezerwacja.save()
            ubezpieczenie.numer_polisy = rezerwacja.id
            ubezpieczenie.cena = ubezpieczenie.get_koszt(rezerwacja.calculate_koszt())
            ubezpieczenie.save()
            return redirect('panelpracownika:rezerwacje')
    else:
        form = RezerwacjaForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nową rezerwację", 'target': 'panelpracownika:rezerwacja_dodaj'})



@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def rezerwacje_usun(request, pk=None):
    rezerwacje = get_object_or_404(Rezerwacja, pk=pk)
    if request.method == 'POST':
        form = DokumentDeleteForm(request.POST, instance=rezerwacje)
        if form.is_valid():
            rezerwacje.delete()
            return redirect('panelpracownika:rezerwacje')
    else:
        form = DokumentDeleteForm(instance=rezerwacje)
    return render(request, 'usun_form.html', {'form': form, 'element': rezerwacje, 'title': "Usuń wybraną rezerwację", 'target': 'panelpracownika:rezerwacje_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dokumenty(request):
    dokumenty_lista = Dokument.objects.all().order_by('rezerwacja__data_od')
    page = request.GET.get('page', 1)
    paginator = Paginator(dokumenty_lista, 10)
    try:
        dokumenty = paginator.page(page)
    except PageNotAnInteger:
        dokumenty = paginator.page(1)
    except EmptyPage:
        dokumenty = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': dokumenty, 'url': request.path, 'title': 'Zarządzaj dokumentami'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dokumenty_dodaj(request):
    if request.method == 'POST':
        form = DokumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:dokumenty')
    else:
        form = DokumentForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy dokument", 'target': 'panelpracownika:dokumenty_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dokumenty_edytuj(request, pk=None):
    dokumenty = get_object_or_404(Dokument, pk=pk)
    if request.method == 'POST':
        form = DokumentForm(request.POST, instance=dokumenty)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:dokumenty')
    else:
        form = DokumentForm(instance=dokumenty)
    return render(request, 'edytuj_form.html', {'form': form, 'element': dokumenty,  'title': "Edytuj wybrany dokument", 'target': 'panelpracownika:dokumenty_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dokumenty_usun(request, pk=None):
    dokumenty = get_object_or_404(Dokument, pk=pk)
    if request.method == 'POST':
        form = DokumentDeleteForm(request.POST, instance=dokumenty)
        if form.is_valid():
            dokumenty.delete()
            return redirect('panelpracownika:ubezpieczenie')
    else:
        form = DokumentDeleteForm(instance=dokumenty)
    return render(request, 'usun_form.html', {'form': form, 'element': dokumenty, 'title': "Usuń wybrany dokument", 'target': 'panelpracownika:dokumenty_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dodatkowe_oplaty(request):
    dodatkowe_oplaty_lista = DodatkoweOplaty.objects.all().order_by('dokument__rezerwacja__data_od')
    page = request.GET.get('page', 1)
    paginator = Paginator(dodatkowe_oplaty_lista, 10)
    try:
        dodatkowe_oplaty = paginator.page(page)
    except PageNotAnInteger:
        dodatkowe_oplaty = paginator.page(1)
    except EmptyPage:
        dodatkowe_oplaty = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': dodatkowe_oplaty, 'url': request.path, 'title': 'Zarządzaj dodatkowymi opłatami'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dodatkowe_oplaty_dodaj(request):
    if request.method == 'POST':
        form = DodatkoweOplatyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:dodatkowe_oplaty')
    else:
        form = DodatkoweOplatyForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowe dodatkowe opłaty", 'target': 'panelpracownika:dodatkowe_oplaty_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dodatkowe_oplaty_edytuj(request, pk=None):
    dodatkowe_oplaty = get_object_or_404(DodatkoweOplaty, pk=pk)
    if request.method == 'POST':
        form = DodatkoweOplatyForm(request.POST, instance=dodatkowe_oplaty)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:dodatkowe_oplaty')
    else:
        form = DodatkoweOplatyForm(instance=dodatkowe_oplaty)
    return render(request, 'edytuj_form.html', {'form': form, 'element': dodatkowe_oplaty,  'title': "Edytuj wybrane dodatkowe opłaty", 'target': 'panelpracownika:dodatkowe_oplaty_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def dodatkowe_oplaty_usun(request, pk=None):
    dodatkowe_oplaty = get_object_or_404(DodatkoweOplaty, pk=pk)
    if request.method == 'POST':
        form = DodatkoweOplatyDeleteForm(request.POST, instance=dodatkowe_oplaty)
        if form.is_valid():
            dodatkowe_oplaty.delete()
            return redirect('panelpracownika:ubezpieczenie')
    else:
        form = DodatkoweOplatyDeleteForm(instance=dodatkowe_oplaty)
    return render(request, 'usun_form.html', {'form': form, 'element': dodatkowe_oplaty, 'title': "Usuń wybrane dodatkowe opłaty", 'target': 'panelpracownika:dodatkowe_oplaty_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def platnosc(request):
    platnosci_lista = Platnosc.objects.all().order_by('data')
    page = request.GET.get('page', 1)
    paginator = Paginator(platnosci_lista, 10)
    try:
        platnosc = paginator.page(page)
    except PageNotAnInteger:
        platnosc = paginator.page(1)
    except EmptyPage:
        platnosc = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': platnosc, 'url': request.path, 'title': 'Zarządzaj płatnościami'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def platnosc_dodaj(request):
    if request.method == 'POST':
        form = PlatnoscForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:platnosc')
    else:
        form = PlatnoscForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nową płatność", 'target': 'panelpracownika:platnosc_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def platnosc_edytuj(request, pk=None):
    platnosci = get_object_or_404(Platnosc, pk=pk)
    if request.method == 'POST':
        form = PlatnoscForm(request.POST, instance=platnosci)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:platnosc')
    else:
        form = PlatnoscForm(instance=platnosci)
    return render(request, 'edytuj_form.html', {'form': form, 'element': platnosci,  'title': "Edytuj wybraną płatność", 'target': 'panelpracownika:platnosc_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def platnosc_usun(request, pk=None):
    platnosc = get_object_or_404(Platnosc, pk=pk)
    if request.method == 'POST':
        form = PlatnoscDeleteForm(request.POST, instance=platnosc)
        if form.is_valid():
            platnosc.delete()
            return redirect('panelpracownika:platnosc')
    else:
        form = PlatnoscDeleteForm(instance=platnosc)
    return render(request, 'usun_form.html', {'form': form, 'element': platnosc, 'title': "Usuń wybraną płatność", 'target': 'panelpracownika:platnosc_usun'})



@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def ubezpieczenie(request):
    ubezpieczenie_lista = Ubezpieczenie.objects.all().order_by('numer_polisy')
    page = request.GET.get('page', 1)
    paginator = Paginator(ubezpieczenie_lista, 10)
    try:
        ubezpieczenia = paginator.page(page)
    except PageNotAnInteger:
        ubezpieczenia = paginator.page(1)
    except EmptyPage:
        ubezpieczenia = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': ubezpieczenia, 'url': request.path, 'title': 'Zarządzaj ubezpieczeniami'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def ubezpieczenie_dodaj(request):
    if request.method == 'POST':
        form = UbezpieczenieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:ubezpieczenie')
    else:
        form = UbezpieczenieForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowe ubezpieczenie", 'target': 'panelpracownika:ubezpieczenie_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def ubezpieczenie_edytuj(request, pk=None):
    ubezpieczenie = get_object_or_404(Ubezpieczenie, pk=pk)
    if request.method == 'POST':
        form = UbezpieczenieForm(request.POST, instance=ubezpieczenie)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:ubezpieczenie')
    else:
        form = UbezpieczenieForm(instance=ubezpieczenie)
    return render(request, 'edytuj_form.html', {'form': form, 'element': ubezpieczenie,  'title': "Edytuj wybrane ubezpieczenie", 'target': 'panelpracownika:ubezpieczenie_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def ubezpieczenie_usun(request, pk=None):
    ubezpieczenie = get_object_or_404(Ubezpieczenie, pk=pk)
    if request.method == 'POST':
        form = UbezpieczenieDeleteForm(request.POST, instance=ubezpieczenie)
        if form.is_valid():
            ubezpieczenie.delete()
            return redirect('panelpracownika:ubezpieczenie')
    else:
        form = UbezpieczenieDeleteForm(instance=ubezpieczenie)
    return render(request, 'usun_form.html', {'form': form, 'element': ubezpieczenie, 'title': "Usuń wybrane ubezpieczenie", 'target': 'panelpracownika:ubezpieczenie_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod(request):
    samochody_lista = Samochod.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(samochody_lista, 10)
    try:
        samochody = paginator.page(page)
    except PageNotAnInteger:
        samochody = paginator.page(1)
    except EmptyPage:
        samochody = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': samochody, 'url': request.path, 'title': 'Zarządzaj samochodami'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_dodaj(request):
    if request.method == 'POST':
        form = SamochodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod')
    else:
        form = SamochodForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy samochód", 'target': 'panelpracownika:samochod_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_edytuj(request, pk=None):
    samochod = get_object_or_404(Samochod, pk=pk)
    if request.method == 'POST':
        form = SamochodForm(request.POST, instance=samochod)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod')
    else:
        form = SamochodForm(instance=samochod)
    return render(request, 'edytuj_form.html', {'form': form, 'element': samochod,  'title': "Edytuj wybrany samochód", 'target': 'panelpracownika:samochod_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_usun(request, pk=None):
    samochod = get_object_or_404(Samochod, pk=pk)
    if request.method == 'POST':
        form = SamochodDeleteForm(request.POST, instance=samochod)
        if form.is_valid():
            samochod.delete()
            return redirect('panelpracownika:samochod')
    else:
        form = SamochodDeleteForm(instance=samochod)
    return render(request, 'usun_form.html', {'form': form, 'element': samochod, 'title': "Usuń wybrany samochód", 'target': 'panelpracownika:samochod_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def typ_ubezpieczenia(request):
    typ_ubezpieczenia_lista = TypUbezpieczenia.objects.all().order_by('variant')
    page = request.GET.get('page', 1)
    paginator = Paginator(typ_ubezpieczenia_lista, 10)
    try:
        typ_ubezpieczenia = paginator.page(page)
    except PageNotAnInteger:
        typ_ubezpieczenia = paginator.page(1)
    except EmptyPage:
        typ_ubezpieczenia = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': typ_ubezpieczenia, 'url': request.path, 'title': 'Zarządzaj typami ubezpieczeń'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def typ_ubezpieczenia_dodaj(request):
    if request.method == 'POST':
        form = UbezpieczenieTypForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:typ_ubezpieczenia_dodaj')
    else:
        form = UbezpieczenieTypForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy typ ubezpieczenia", 'target': 'panelpracownika:typ_ubezpieczenia_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def typ_ubezpieczenia_edytuj(request, pk=None):
    typ = get_object_or_404(TypUbezpieczenia, pk=pk)
    if request.method == 'POST':
        form = UbezpieczenieTypForm(request.POST, instance=typ)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:typ_ubezpieczenia')
    else:
        form = UbezpieczenieTypForm(instance=typ)
    return render(request, 'edytuj_form.html', {'form': form, 'element': typ,  'title': "Edytuj wybrany typ ubezpieczenia", 'target': 'panelpracownika:typ_ubezpieczenia_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def typ_ubezpieczenia_usun(request, pk=None):
    typ = get_object_or_404(TypUbezpieczenia, pk=pk)
    if request.method == 'POST':
        form = UbezpieczenieTypDeleteForm(request.POST, instance=typ)
        if form.is_valid():
            typ.delete()
            return redirect('panelpracownika:typ_ubezpieczenia')
    else:
        form = UbezpieczenieTypDeleteForm(instance=typ)
    return render(request, 'usun_form.html', {'form': form, 'element': typ, 'title': "Usuń wybrany typ ubezpieczenia", 'target': 'panelpracownika:ubezpieczenie_typ_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def model(request):
    modele_lista = SamochodModel.objects.all().order_by('nazwa')
    page = request.GET.get('page', 1)
    paginator = Paginator(modele_lista, 10)
    try:
        modele = paginator.page(page)
    except PageNotAnInteger:
        modele = paginator.page(1)
    except EmptyPage:
        modele = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
              {'elementy': modele, 'url': request.path, 'title': 'Zarządzaj modelami samochodów'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def model_dodaj(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:model')
    else:
        form = ModelForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy model samochodu", 'target': 'panelpracownika:dodaj_model'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def model_edytuj(request, pk=None):
    model = get_object_or_404(SamochodModel, pk=pk)
    if request.method == 'POST':
        form = ModelForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:model')
    else:
        form = ModelForm(instance=model)
    return render(request, 'edytuj_form.html', {'form': form, 'element': model, 'title': "Edytuj wybrany model samochodu", 'target': 'panelpracownika:edytuj_model'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def model_usun(request, pk=None):
    model = get_object_or_404(SamochodModel, pk=pk)
    if request.method == 'POST':
        form = ModelDeleteForm(request.POST, instance=model)
        if form.is_valid():
            model.delete()
            return redirect('panelpracownika:model')
    else:
        form = ModelDeleteForm(instance=model)
    return render(request, 'usun_form.html', {'form': form, 'element': model, 'title': "Usuń wybrany model samochodu", 'target': 'panelpracownika:usun_model'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def marka(request):
    marki_lista = SamochodMarka.objects.all().order_by('nazwa')
    page = request.GET.get('page', 1)
    paginator = Paginator(marki_lista, 10)
    try:
        marki = paginator.page(page)
    except PageNotAnInteger:
        marki = paginator.page(1)
    except EmptyPage:
        marki = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
                  {'elementy': marki, 'url': request.path, 'title': 'Zarządzaj markami samochodów'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def marka_dodaj(request):
    if request.method == 'POST':
        form = MarkaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:marka')
    else:
        form = MarkaForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nową markę samochodu", 'target': 'panelpracownika:marka_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def marka_edytuj(request, pk=None):
    marka = get_object_or_404(SamochodMarka, pk=pk)
    if request.method == 'POST':
        form = MarkaForm(request.POST, instance=marka)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:marka')
    else:
        form = MarkaForm(instance=marka)
    return render(request, 'edytuj_form.html', {'form': form, 'element': marka, 'title': "Edytuj wybraną markę samochodu", 'target': 'panelpracownika:marka_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def marka_usun(request, pk=None):
    marka = get_object_or_404(SamochodMarka, pk=pk)
    if request.method == 'POST':
        form = MarkaDeleteForm(request.POST, instance=marka)
        if form.is_valid():
            marka.delete()
            return redirect('panelpracownika:marka')
    else:
        form = MarkaDeleteForm(instance=marka)
    return render(request, 'usun_form.html', {'form': form, 'element': marka, 'title': "Usuń wybraną markę samochodu", 'target': 'panelpracownika:marka_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_kategoria(request):
    kategoria_lista = SamochodKategoria.objects.all().order_by('nazwa')
    page = request.GET.get('page', 1)
    paginator = Paginator(kategoria_lista, 10)
    try:
        kategorie = paginator.page(page)
    except PageNotAnInteger:
        kategorie = paginator.page(1)
    except EmptyPage:
        kategorie = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
                  {'elementy': kategorie, 'url': request.path, 'title': 'Zarządzaj kategoriami samochodów'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_kategoria_dodaj(request):
    if request.method == 'POST':
        form = KategoriaSamochoduForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_kategoria')
    else:
        form = KategoriaSamochoduForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nową kategorię samochodu", 'target': 'panelpracownika:samochod_kategoria_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_kategoria_edytuj(request, pk=None):
    samochod_kategoria = get_object_or_404(SamochodKategoria, pk=pk)
    if request.method == 'POST':
        form = KategoriaSamochoduForm(request.POST, instance=samochod_kategoria)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_kategoria')
    else:
        form = KategoriaSamochoduForm(instance=samochod_kategoria)
    return render(request, 'edytuj_form.html', {'form': form, 'element': samochod_kategoria, 'title': "Edytuj wybraną kategorię samochodu", 'target': 'panelpracownika:samochod_kategoria_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_kategoria_usun(request, pk=None):
    samochod_kategoria = get_object_or_404(SamochodKategoria, pk=pk)
    if request.method == 'POST':
        form = KategoriaSamochoduDeleteForm(request.POST, instance=samochod_kategoria)
        if form.is_valid():
            samochod_kategoria.delete()
            return redirect('panelpracownika:samochod_kategoria')
    else:
        form = KategoriaSamochoduDeleteForm(instance=samochod_kategoria)
    return render(request, 'usun_form.html', {'form': form, 'element': samochod_kategoria, 'title': "Usuń wybraną kategorię samochodu", 'target': 'panelpracownika:samochod_kategoria_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_silnik(request):
    silnik_lista = SamochodSilnik.objects.all().order_by('nazwa')
    page = request.GET.get('page', 1)
    paginator = Paginator(silnik_lista, 10)
    try:
        silniki = paginator.page(page)
    except PageNotAnInteger:
        silniki = paginator.page(1)
    except EmptyPage:
        silniki = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
                  {'elementy': silniki, 'url': request.path, 'title': 'Zarządzaj typami silników samochodów'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_silnik_dodaj(request):
    if request.method == 'POST':
        form = SilnikSamochodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_silnik')
    else:
        form = SilnikSamochodForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy rodzaj silnika samochodu", 'target': 'panelpracownika:samochod_silnik_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_silnik_edytuj(request, pk=None):
    samochod_silnik = get_object_or_404(SamochodSilnik, pk=pk)
    if request.method == 'POST':
        form = SilnikSamochodForm(request.POST, instance=samochod_silnik)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_silnik')
    else:
        form = SilnikSamochodForm(instance=samochod_silnik)
    return render(request, 'edytuj_form.html', {'form': form, 'element': samochod_silnik, 'title': "Edytuj wybrany rodzaj silnika samochodu samochodu", 'target': 'panelpracownika:samochod_silnik_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_silnik_usun(request, pk=None):
    samochod_silnik = get_object_or_404(SamochodSilnik, pk=pk)
    if request.method == 'POST':
        form = SilnikSamochodDeleteForm(request.POST, instance=samochod_silnik)
        if form.is_valid():
            samochod_silnik.delete()
            return redirect('panelpracownika:samochod_silnik')
    else:
        form = SilnikSamochodDeleteForm(instance=samochod_silnik)
    return render(request, 'usun_form.html', {'form': form, 'element': samochod_silnik, 'title': "Usuń wybrany rodzaj silnika", 'target': 'panelpracownika:samochod_silnik_usun'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_skrzynia(request):
    skrzynia_lista = SamochodSkrzynia.objects.all().order_by('nazwa')
    page = request.GET.get('page', 1)
    paginator = Paginator(skrzynia_lista, 10)
    try:
        skrzynie = paginator.page(page)
    except PageNotAnInteger:
        skrzynie = paginator.page(1)
    except EmptyPage:
        skrzynie = paginator.page(paginator.num_pages)

    return render(request, 'lista_strony.html',
                  {'elementy': skrzynie, 'url': request.path, 'title': 'Zarządzaj typami skrzyń biegów samochodów'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_skrzynia_dodaj(request):
    if request.method == 'POST':
        form = SkrzyniaSamochodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_skrzynia')
    else:
        form = SkrzyniaSamochodForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy rodzaj skrzyni biegów", 'target': 'panelpracownika:samochod_skrzynia_dodaj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_skrzynia_edytuj(request, pk=None):
    samochod_skrzynia = get_object_or_404(SamochodSkrzynia, pk=pk)
    if request.method == 'POST':
        form = SkrzyniaSamochodForm(request.POST, instance=samochod_skrzynia)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_skrzynia')
    else:
        form = SkrzyniaSamochodForm(instance=samochod_skrzynia)
    return render(request, 'edytuj_form.html', {'form': form, 'element': samochod_skrzynia, 'title': "Edytuj wybrany rodzaj skrzyni biegów samochodu", 'target': 'panelpracownika:samochod_skrzynia_edytuj'})


@login_required()
@user_passes_test(czy_pracownik, login_url='wypozyczalnia:brak_dostepu')
def samochod_skrzynia_usun(request, pk=None):
    samochod_skrzynia = get_object_or_404(SamochodSkrzynia, pk=pk)
    if request.method == 'POST':
        form = SkrzyniaSamochodDeleteForm(request.POST, instance=samochod_skrzynia)
        if form.is_valid():
            samochod_skrzynia.delete()
            return redirect('panelpracownika:samochod_skrzynia')
    else:
        form = SkrzyniaSamochodDeleteForm(instance=samochod_skrzynia)
    return render(request, 'usun_form.html', {'form': form, 'element': samochod_skrzynia, 'title': "Usuń wybrany typ skrzyni biegów", 'target': 'panelpracownika:samochod_skrzynia_usun'})

