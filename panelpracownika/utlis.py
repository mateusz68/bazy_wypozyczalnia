from wypozyczalnia.models import *


def calculate_cost(rezerwacja_id):
    rezerwacja = Rezerwacja.objects.get(pk=rezerwacja_id)
    dokument = Dokument.objects.filter(rezerwacja_id=rezerwacja_id, typ=Dokument.DokumentTyp.FAKTURA)
    if len(dokument) == 0:
        return
    dokument = dokument[0]
    ubezpieczenie = Ubezpieczenie.objects.get(pk = rezerwacja.ubezpieczenie_id)
    ubezpieczenie.cena = ubezpieczenie.get_koszt(rezerwacja.calculate_koszt())
    ubezpieczenie.save()
    dokument.kwota = rezerwacja.get_koszt()
    dokument.save()
