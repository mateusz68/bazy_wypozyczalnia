from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import Uzytkownik
from wypozyczalnia.models import *
from panelpracownika.forms import *


def typ_ubezpieczenia(request):
    typ_ubezpieczenia = TypUbezpieczenia.objects.all();
    return render(request, 'element_list.html',
              {'elementy': typ_ubezpieczenia, 'url': request.path, 'title': 'Zarządzaj typami ubezpiczenia'})


def typ_ubezpieczenia_dodaj(request):
    if request.method == 'POST':
        form = UbezpieczenieTypForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:typ_ubezpieczenia_dodaj')
    else:
        form = UbezpieczenieTypForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy typ ubezpieczenia", 'target': 'panelpracownika:typ_ubezpieczenia_dodaj'})


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


def model(request):
    modele = SamochodModel.objects.all()
    return render(request, 'element_list.html', {'elementy': modele, 'url': request.path, 'title': 'Zarządzaj modelami samochodów' })


def model_dodaj(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:model')
    else:
        form = ModelForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy model samochodu", 'target': 'panelpracownika:dodaj_model'})


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


def marka(request):
    marki = SamochodMarka.objects.all()
    return render(request, 'element_list.html', {'elementy': marki, 'url': request.path, 'title': 'Zarządzaj markami samochodów' })


def marka_dodaj(request):
    if request.method == 'POST':
        form = MarkaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:marka')
    else:
        form = MarkaForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nową markę samochodu", 'target': 'panelpracownika:marka_dodaj'})


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


def samochod_kategoria(request):
    kategoria = SamochodKategoria.objects.all()
    return render(request, 'element_list.html', {'elementy': kategoria, 'url': request.path, 'title': 'Zarządzaj kategoriami samochodów' })


def samochod_kategoria_dodaj(request):
    if request.method == 'POST':
        form = KategoriaSamochoduForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_kategoria')
    else:
        form = KategoriaSamochoduForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nową kategorię samochodu", 'target': 'panelpracownika:samochod_kategoria_dodaj'})


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


def samochod_silnik(request):
    silnik = SamochodSilnik.objects.all()
    return render(request, 'element_list.html', {'elementy': silnik, 'url': request.path, 'title': 'Zarządzaj rodzajami silników samochodów' })


def samochod_silnik_dodaj(request):
    if request.method == 'POST':
        form = SilnikSamochodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_silnik')
    else:
        form = SilnikSamochodForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy rodzaj silnika samochodu", 'target': 'panelpracownika:samochod_silnik_dodaj'})


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


def samochod_skrzynia(request):
    skrzynia = SamochodSkrzynia.objects.all()
    return render(request, 'element_list.html', {'elementy': skrzynia, 'url': request.path, 'title': 'Zarządzaj rodzajami skrzyń biegów samochodów' })


def samochod_skrzynia_dodaj(request):
    if request.method == 'POST':
        form = SkrzyniaSamochodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panelpracownika:samochod_skrzynia')
    else:
        form = SkrzyniaSamochodForm()
    return render(request, 'dodaj_form.html', {'form': form, 'title': "Dodaj nowy rodzaj skrzyni biegów", 'target': 'panelpracownika:samochod_skrzynia_dodaj'})


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

