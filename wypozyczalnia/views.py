from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Uzytkownik
from wypozyczalnia.models import *
from wypozyczalnia.forms import *
from django.contrib import messages
from django.contrib import messages


def index(request):
    najnowsze_samochody = Samochod.objects.all().order_by('id')[:5]
    return render(request, 'index.html', {'elementy': najnowsze_samochody})


def brak_dostepu(request):
    return render(request, 'brak_dostepu.html')


def kontakt(request):
    return render(request, 'kontakt.html')


def szczczegoly_samochodu(request, pk=None):
    samochod = get_object_or_404(Samochod, pk=pk)
    rezerwacje = Rezerwacja.objects.filter(samochod_id=pk)
    return render(request, 'szczegoly_samochod.html', {'samochod': samochod, 'rezerwacje': rezerwacje})


def rezerwuj_samochod(request):
    uzytkownik = get_object_or_404(Uzytkownik, pk=request.user.id)
    pk = request.GET.get('id')
    print(request.GET)
    print(pk)
    pk = 1
    if pk is None:
        return redirect('wypozyczalnia:index')
    samochod = get_object_or_404(Samochod, pk=pk)
    rezerwacje = Rezerwacja.objects.filter(samochod_id=pk)
    print("test")
    print(pk)
    print(request.method)
    # if request.method == 'POST':
    #     form = RezerwacjaUserForm(request.POST, key=pk, user=uzytkownik)
    #     print("post")
    #     if form.is_valid():
    #         form.save()
    #         print("test")
    #         return redirect('wypozyczalnia:index')
    # else:
    #     form = RezerwacjaUserForm(key=pk, user=uzytkownik)
    # return render(request, 'rezerwacja_form.html',
    #               {'form': form, 'samochod': samochod, 'rezerwacje': rezerwacje, 'title': "Dodaj płatność do rezerwacji",
    #                'target': 'wypozyczalnia:rezerwuj_samochod'})

    if request.method == 'POST':
        form = RezerwacjaUserForm(request.POST, key=pk)
        print("post hej")
        if form.is_valid():
            # print(form)
            # form.save()
            # print("test")
            temp = form.cleaned_data
            temp_rez = Rezerwacja()
            temp_rez.uzytkownik = uzytkownik
            ubezpieczenie = Ubezpieczenie(cena=100, typ_id=form.cleaned_data.get('typ_ubezpieczenie'))
            # ubezpieczenie.save()
            temp_rez.ubezpieczenie_id = ubezpieczenie.id
            temp_rez.uwagi = form.cleaned_data.get('uwagi')
            temp_rez.data_od = form.cleaned_data.get('data_od')
            temp_rez.data_do = form.cleaned_data.get('data_do')
            temp_rez.samochod_id = samochod.id
            # temp_rez.save()
            print(temp)
            messages.success(request, 'Profile details updated.')

            # return redirect('wypozyczalnia:index')
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
