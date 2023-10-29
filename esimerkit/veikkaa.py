
from argparse import ArgumentParser
import string

import koskut

parser = ArgumentParser()

parser.add_argument("laji", type=str, choices=[
    "yleissana", "vierassana", "paikannimi", "vieras_paikannimi",
    "etunimi", "vieras_etunimi", "sukunimi", "vieras_sukunimi"
])
parser.add_argument("sana")

args = parser.parse_args()


VAIN_YKSIKKÖ = {koskut.Nimilaji.PAIKANNIMI, koskut.Nimilaji.VIERAS_PAIKANNIMI}


def taivuta_nimisanaa(nimisana, laji):
    MUODOT = [
        (koskut.Sija.NIMENTÖ, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.OMANTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.OSANTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.SISÄOLENTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.SISÄERONTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.SISÄTULENTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.ULKO_OLENTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.ULKOERONTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.ULKOTULENTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.OLENTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.TULENTO, koskut.Luku.YKSIKKÖ),
        (koskut.Sija.VAJANTO, koskut.Luku.YKSIKKÖ),

        (koskut.Sija.NIMENTÖ, koskut.Luku.MONIKKO),
        (koskut.Sija.OMANTO, koskut.Luku.MONIKKO),
        (koskut.Sija.OSANTO, koskut.Luku.MONIKKO),
        (koskut.Sija.SISÄOLENTO, koskut.Luku.MONIKKO),
        (koskut.Sija.SISÄERONTO, koskut.Luku.MONIKKO),
        (koskut.Sija.SISÄTULENTO, koskut.Luku.MONIKKO),
        (koskut.Sija.ULKO_OLENTO, koskut.Luku.MONIKKO),
        (koskut.Sija.ULKOERONTO, koskut.Luku.MONIKKO),
        (koskut.Sija.ULKOTULENTO, koskut.Luku.MONIKKO),
        (koskut.Sija.OLENTO, koskut.Luku.MONIKKO),
        (koskut.Sija.TULENTO, koskut.Luku.MONIKKO),
        (koskut.Sija.VAJANTO, koskut.Luku.MONIKKO),
        (koskut.Sija.KEINONTO, koskut.Luku.MONIKKO),
        (koskut.Sija.SEURANTO, koskut.Luku.MONIKKO),
    ]
    for sija, luku in MUODOT:
        if laji in VAIN_YKSIKKÖ and luku == koskut.Luku.MONIKKO:
            continue
        print(string.capwords(sija.name.replace("_", "-")).ljust(20), end="")
        print(luku.name.title().ljust(10), end="")
        print(nimisana.taivuta1(sija, luku).ljust(25), end="")
        if sija == koskut.Sija.KEINONTO:
            print("")
        else:
            print(nimisana.taivuta1(sija, luku, omistus=koskut.Omistusliite.NSA))


laji = getattr(koskut.Nimilaji, args.laji.upper())
veikkain = koskut.Taivutusveikkain(args.sana, laji, vain_yksikkö=laji in VAIN_YKSIKKÖ)

for sija, luku, vaihtoehdot in veikkain.vaihtoehdot():
    print(sija.name, luku.name)
    for i, vaihtoehto in enumerate(vaihtoehdot):
        print("{}) {}".format(i + 1, vaihtoehto))

    while True:
        syöte = input()
        try:
            syöte = int(syöte)
        except ValueError:
            print("Vastaa numerolla!")
            continue
        if syöte <= 0 or syöte > len(vaihtoehdot):
            print("Numeron pitää olla yksi vaihtoehdoista!")
            continue

        veikkain.valitse(vaihtoehdot[syöte - 1])
        break

nimisana = veikkain.tulos()
print("")
print(nimisana.kotus())
taivuta_nimisanaa(nimisana, laji)
