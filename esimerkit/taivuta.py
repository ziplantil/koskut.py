
from argparse import ArgumentParser
import string

import koskut

parser = ArgumentParser()

parser.add_argument("sana")
parser.add_argument("taivutusluokka", type=int)
parser.add_argument("astevaihtelu", type=str, nargs="?", default="")
parser.add_argument("vokaalisointu", type=str, nargs="?", choices=("", "a", "ä"), default="")
parser.add_argument("-v", "--vokaali", type=str, nargs="?", default="")
parser.add_argument("--ikaalinen", action="store_true", default=False)
parser.add_argument("--meri", action="store_true", default=False)
parser.add_argument("--aika", action="store_true", default=False)
parser.add_argument("--lyhenne", action="store_true", default=False)

args = parser.parse_args()


def taivuta_nimisanaa(nimisana):
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
        if args.ikaalinen and luku == koskut.Luku.MONIKKO:
            continue
        print(string.capwords(sija.name.replace("_", "-")).ljust(20), end="")
        print(luku.name.title().ljust(10), end="")
        print(nimisana.taivuta1(sija, luku).ljust(25), end="")
        if sija == koskut.Sija.KEINONTO:
            print("")
        else:
            print(nimisana.taivuta1(sija, luku, omistus=koskut.Omistusliite.NSA))


def taivuta_teonsanaa(teonsana):
    ALUKSET = [
        koskut.Alus.YKSIKKÖ_1, koskut.Alus.YKSIKKÖ_2, koskut.Alus.YKSIKKÖ_3,
        koskut.Alus.MONIKKO_1, koskut.Alus.MONIKKO_2, koskut.Alus.MONIKKO_3,
        koskut.Alus.TEITITTELY, koskut.Alus.TEKIJÄTÖN
    ]

    def koko_muoto(alus, aikamuoto, tapaluokka, kieltomuoto):
        alku = " ".join(koskut.Teonsana.liiton_alkuosa(alus, aikamuoto, tapaluokka, kieltomuoto))
        pääsana = teonsana.taivuta_tekijällinen1(alus, aikamuoto, tapaluokka, kieltomuoto)
        return (alku + " " + pääsana).strip()


    def aluksellinen_muoto(alus, aikamuoto, tapaluokka):
        print(koko_muoto(alus, aikamuoto, tapaluokka, False).ljust(30), end = "")
        print(koko_muoto(alus, aikamuoto, tapaluokka, True).ljust(30), end = "")
        if aikamuoto == koskut.Aikamuoto.KESTÄMÄ:
            aikamuoto = koskut.Aikamuoto.PÄÄTTYMÄ
        elif aikamuoto == koskut.Aikamuoto.KERTOMA:
            aikamuoto = koskut.Aikamuoto.ENTISPÄÄTTYMÄ
        print(koko_muoto(alus, aikamuoto, tapaluokka, False).ljust(35), end = "")
        print(koko_muoto(alus, aikamuoto, tapaluokka, True))


    def alukselliset_muodot(aikamuoto, tapaluokka):
        for alus in ALUKSET:
            if alus != koskut.Alus.YKSIKKÖ_1 or tapaluokka != koskut.Tapaluokka.KÄSKYTAPA:
                aluksellinen_muoto(alus, aikamuoto, tapaluokka)
        print("")

    def nimitapa(nimitapa, omistusmuodot):
        if omistusmuodot is False:
            print(teonsana.taivuta_nimitapa1(nimitapa))
        elif omistusmuodot is None:
            print(teonsana.taivuta_nimitapa1(nimitapa).ljust(30), end="")
            print(teonsana.taivuta_nimitapa1(nimitapa, omistus=koskut.Omistusliite.NI).ljust(30), end="")
            print(teonsana.taivuta_nimitapa1(nimitapa, omistus=koskut.Omistusliite.NSA))
        elif omistusmuodot is True:
            print(teonsana.taivuta_nimitapa1(nimitapa, omistus=koskut.Omistusliite.NI).ljust(30), end="")
            print(teonsana.taivuta_nimitapa1(nimitapa, omistus=koskut.Omistusliite.MME).ljust(30), end="")
            print(teonsana.taivuta_nimitapa1(nimitapa, omistus=koskut.Omistusliite.NSA))

    def taivuta_nimisanaa(nimisana):
        print(nimisana.taivuta1(koskut.Sija.NIMENTÖ).ljust(30), end="")
        print(nimisana.taivuta1(koskut.Sija.OMANTO).ljust(30), end="")
        print(nimisana.taivuta1(koskut.Sija.OSANTO))

    def nimitapa_johda(nimitapa):
        taivuta_nimisanaa(teonsana.johda_nimitapa(nimitapa))

    def laatutapa_johda(nimitapa):
        taivuta_nimisanaa(teonsana.johda_laatutapa(nimitapa))


    alukselliset_muodot(koskut.Aikamuoto.KESTÄMÄ, koskut.Tapaluokka.TOSITAPA)
    alukselliset_muodot(koskut.Aikamuoto.KERTOMA, koskut.Tapaluokka.TOSITAPA)
    alukselliset_muodot(koskut.Aikamuoto.KESTÄMÄ, koskut.Tapaluokka.EHTOTAPA)
    alukselliset_muodot(koskut.Aikamuoto.KESTÄMÄ, koskut.Tapaluokka.KÄSKYTAPA)
    alukselliset_muodot(koskut.Aikamuoto.KESTÄMÄ, koskut.Tapaluokka.MAHTOTAPA)

    nimitapa(koskut.Nimitapa.A, False)
    nimitapa(koskut.Nimitapa.AKSE, True)
    nimitapa(koskut.Nimitapa.ESSA, None)
    nimitapa(koskut.Nimitapa.TAESSA, False)
    nimitapa(koskut.Nimitapa.EN, False)
    nimitapa(koskut.Nimitapa.MASSA, False)
    nimitapa(koskut.Nimitapa.MASTA, False)
    nimitapa(koskut.Nimitapa.MAAN, False)
    nimitapa(koskut.Nimitapa.MALLA, False)
    nimitapa(koskut.Nimitapa.MATTA, False)
    nimitapa(koskut.Nimitapa.MAN, False)
    nimitapa(koskut.Nimitapa.TAMAN, False)
    nimitapa_johda(koskut.Nimitapa.MINEN)
    nimitapa(koskut.Nimitapa.MAISILLA, True)
    print("")

    laatutapa_johda(koskut.Laatutapa.VA)
    laatutapa_johda(koskut.Laatutapa.TAVA)
    laatutapa_johda(koskut.Laatutapa.NUT)
    laatutapa_johda(koskut.Laatutapa.TTU)
    laatutapa_johda(koskut.Laatutapa.MA)
    laatutapa_johda(koskut.Laatutapa.MATON)
    print("")


if args.taivutusluokka < 52:
    taivuta_nimisanaa(koskut.Nimisana(sana=args.sana,
                            luokka=args.taivutusluokka,
                            aste=args.astevaihtelu or None,
                            sointu=args.vokaalisointu or None,
                            loppuvokaali=args.vokaali or None,
                            vain_yksikkö=args.ikaalinen,
                            pakota_alisteiset_sijat_monikkoon=args.ikaalinen,
                            meri=args.meri,
                            aika=args.aika,
                            lyhenne=args.lyhenne))
else:
    taivuta_teonsanaa(koskut.Teonsana(sana=args.sana,
                            luokka=args.taivutusluokka,
                            aste=args.astevaihtelu or None,
                            sointu=args.vokaalisointu or None))
