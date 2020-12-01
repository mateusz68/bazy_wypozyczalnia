from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Uzytkownik
from wypozyczalnia.models import *
from wypozyczalnia.forms import *
from django.contrib import messages
from django.contrib import messages
from .filters import *


def index(request):
    najnowsze_samochody = Samochod.objects.all().order_by('id')[:5]
    return render(request, 'index.html', {'elementy': najnowsze_samochody})


def brak_dostepu(request):
    return render(request, 'brak_dostepu.html')


def kontakt(request):
    return render(request, 'kontakt.html')


def udana_rezerwacja(request):
    return render(request, 'udana_rezerwacja.html')


def szczczegoly_samochodu(request, pk=None):
    samochod = get_object_or_404(Samochod, pk=pk)
    rezerwacje = Rezerwacja.objects.filter(samochod_id=pk)
    return render(request, 'szczegoly_samochod.html', {'samochod': samochod, 'rezerwacje': rezerwacje})


def rezerwuj_samochod(request):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    pk = request.GET.get('id')
    if pk is None:
        return redirect('wypozyczalnia:index')
    samochod = get_object_or_404(Samochod, pk=pk)
    rezerwacje = Rezerwacja.objects.filter(samochod_id=pk)

    if request.method == 'POST':
        form = RezerwacjaUserForm(request.POST, key=pk)
        if form.is_valid():
            temp_rez = Rezerwacja()
            temp_rez.uzytkownik = uzytkownik
            ubezpieczenie = Ubezpieczenie(cena=100, typ_id=form.cleaned_data.get('typ_ubezpieczenie'))
            ubezpieczenie.save()
            temp_rez.ubezpieczenie_id = ubezpieczenie.id
            temp_rez.uwagi = form.cleaned_data.get('uwagi')
            temp_rez.data_od = form.cleaned_data.get('data_od')
            temp_rez.data_do = form.cleaned_data.get('data_do')
            temp_rez.samochod_id = samochod.id
            temp_rez.save()
            ubezpieczenie.numer_polisy = temp_rez.id
            ubezpieczenie.cena = ubezpieczenie.get_koszt(temp_rez.calculate_koszt())
            ubezpieczenie.save()
            return redirect('wypozyczalnia:udana_rezerwacja')
    else:

        form = RezerwacjaUserForm(key=pk)
    return render(request, 'rezerwacja_form.html',
                  {'form': form, 'samochod': samochod, 'rezerwacje': rezerwacje, 'title': "Dodaj płatność do rezerwacji",
                   'target': 'wypozyczalnia:rezerwuj_samochod'})


def samochody_lista(request):
    samochody_lista = Samochod.objects.filter(status_samochodu=Samochod.StatusSamochod.DOSTEPNY)
    samochody_filter = SamochodFilter(request.GET, queryset=samochody_lista)

    page = request.GET.get('page', 1)
    paginator = Paginator(samochody_filter.qs, 10)
    try:
        samochody = paginator.page(page)
    except PageNotAnInteger:
        samochody = paginator.page(1)
    except EmptyPage:
        samochody = paginator.page(paginator.num_pages)

    return render(request, 'samochody_list.html',
                  {'filter': samochody_filter, 'elementy': samochody, 'url': request.path, 'title': 'Zarządzaj rezerwacjami'})

