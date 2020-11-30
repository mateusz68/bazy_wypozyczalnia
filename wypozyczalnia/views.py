from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Uzytkownik
from wypozyczalnia.models import *
from wypozyczalnia.forms import *


def index(request):
    return render(request, 'index.html')


def brak_dostepu(request):
    return render(request, 'brak_dostepu.html')


def szczczegoly_samochodu(request, pk=None):
    samochod = get_object_or_404(Samochod, pk=pk)
    rezerwacje = Rezerwacja.objects.filter(samochod_id=pk)
    return render(request, 'szczegoly_samochod.html', {'samochod': samochod, 'rezerwacje': rezerwacje})


def rezerwuj_samochod(request):
    pk = request.GET.get('id')
    if pk is None:
        return redirect('wypozyczalnia:index')
    samochod = get_object_or_404(Samochod, pk=pk)
    rezerwacje = Rezerwacja.objects.filter(samochod_id=pk)
    if request.method == 'POST':
        form = RezerwacjaUserForm(request.POST, key=pk)
        if form.is_valid():
            form.save()
            return redirect('wypozyczalnia:index')
    else:
        form = RezerwacjaUserForm(key=pk)
    return render(request, 'rezerwacja_form.html',
                  {'form': form, 'samochod': samochod, 'rezerwacje': rezerwacje, 'title': "Dodaj płatność do rezerwacji",
                   'target': 'wypozyczalnia:rezerwuj_samochod'})

def samochody_lista(request):
    samochody_lista = Samochod.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(samochody_lista, 10)
    try:
        samochody = paginator.page(page)
    except PageNotAnInteger:
        samochody = paginator.page(1)
    except EmptyPage:
        samochody = paginator.page(paginator.num_pages)

    return render(request, 'samochody_list.html',
                  {'elementy': samochody, 'url': request.path, 'title': 'Zarządzaj rezerwacjami'})
