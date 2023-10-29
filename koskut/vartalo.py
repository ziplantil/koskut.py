
import re

from .vokaali import VOKAALIT, DIFTONGIT
from .astevaihtelu import Astevaihtelu


L = "\u0011"    # loppuvokaali
V = "\u0012"    # vahva aste
H = "\u0013"    # heikko aste
K = "\u0014"    # loppukonsonantti
D = "\u0015"    # diftongi (ie, uo, yö)
P = "\u0016"    # edeltävän lyhyen vokaalin pidennys, toteutettu erikseen (ei punojassa)
HY = "\u0018"   # heittomerkki yksikköön
HM = "\u0019"   # heittomerkki monikkoon
A = "\u001c"    # A/Ä vokaalisoinnun mukaan
O = "\u001d"    # O/Ö vokaalisoinnun mukaan
U = "\u001e"    # U/Y vokaalisoinnun mukaan


HEITTOMERKIT = ("'", "\u2019")
HEITTOMERKKI = "'"
assert HEITTOMERKKI in HEITTOMERKIT


DIFTONGISOI = {"e": "ie", "o": "uo", "ö": "yö"}


def vartalon_punoja(aste: Astevaihtelu | None, etinen: bool, vokaali: str | None, konsonantti: str | None,
                    heittomerkki_yksikköön: bool, heittomerkki_monikkoon: bool):
    """
    Luo vartalon punojan, jonka voi myöhemmin antaa puno_vartalo:lle.

    :param aste: astevaihtelu. jos sanassa on sellainen
    :param etinen: onko sanassa etinen vokaalisointu vai ei
    :param vokaali: sanan loppuvokaali, jos se tunnetaan (ja jos sillä on merkitystä)
    :param konsonantti: sanavartalon loppukonsonantti, jos se tunnetaan (ja jos sillä on merkitystä)
    :param heittomerkki_yksikköön: laitetaanko heittomerkki yksikköön
    :param heittomerkki_monikkoon: laitetaanko heittomerkki monikkoon
    :returns: punoja, jonka voi antaa puno_vartalo:lle.
    """

    return str.maketrans({
        L: vokaali or "",
        V: aste.vahva if aste else "",
        H: aste.heikko if aste else "",
        K: konsonantti or "",
        HY: heittomerkki_yksikköön and HEITTOMERKKI or "",
        HM: heittomerkki_monikkoon and HEITTOMERKKI or "",
        D: DIFTONGISOI.get(vokaali, ""),
        A: "ä" if etinen else "a",
        O: "ö" if etinen else "o",
        U: "y" if etinen else "u",
    })


def puno_vartalo(vartalo: str, punoja: dict) -> str:
    """
    Punoo vartalon, eli muuttaa erikoismerkit varsinaisiksi merkeiksi.

    :param vartalo: punottava vartalo/pääte
    :param punoja: aiemmin vartalon_punoja:lta saatu punoja
    :returns: punottu vartalo
    """

    return vartalo.translate(punoja)


def liestä_vartalo(sana: str, vartalo: str,
                   aste: Astevaihtelu | None,
                   vokaali: str | None = None,
                   konsonantti: str | None = None) -> tuple[str, str | None, str | None]:
    """
    Liestää vartalon, eli purkaa sanasta sen vartalon tietyn päätteen perusteella.

    :param sana: muoto, josta liestetään
    :param vartalo: liestettävä vartalo/pääte
    :param aste: sanan astevaihtelu, jos sillä on sellainen
    :returns: liestetty sanavartalo, loppuvokaali ja loppukonsonantti
    """

    def vaadi(ehto, virhe):
        if not ehto:
            raise ValueError(virhe)

    vokaali, konsonantti = None, None
    for merke in reversed(vartalo):
        if merke == A:    # A/Ä vokaalisoinnun mukaisesti
            vaadi(any(sana.endswith(c) for c in "aä"), "A/Ä vaaditaan")
            sana = sana[:-1]
        elif merke == O:  # O/Ö vokaalisoinnun mukaisesti
            vaadi(any(sana.endswith(c) for c in "oö"), "O/Ö vaaditaan")
            sana = sana[:-1]
        elif merke == U:  # U/Y vokaalisoinnun mukaisesti
            vaadi(any(sana.endswith(c) for c in "uy"), "U/Y vaaditaan")
            sana = sana[:-1]

        elif merke == H:  # heikko aste
            if aste:
                heikko = aste.heikko
                vaadi(sana.endswith(heikko), "heikko aste vaaditaan")
                sana = sana[:len(sana) - len(heikko)]
        elif merke == V:  # vahva aste
            if aste:
                vahva = aste.vahva
                vaadi(sana.endswith(vahva), "vahva aste vaaditaan")
                sana = sana[:len(sana) - len(vahva)]

        elif merke == L:  # loppuvokaali
            if vokaali is not None:
                vaadi(sana.endswith(vokaali), "vokaali vaaditaan")
                sana = sana[:-1]
            else:
                sana, vokaali = sana[:-1], sana[-1]
                vaadi(vokaali in VOKAALIT, "vokaali vaaditaan")
        elif merke == K:  # loppukonsonantti
            if konsonantti is not None:
                vaadi(sana.endswith(konsonantti), "konsonantti vaaditaan")
                sana = sana[:-1]
            else:
                sana, konsonantti = sana[:-1], sana[-1]
                vaadi(konsonantti in "klnprst", "konsonantti vaaditaan")

        elif merke == D:  # loppudiftongi
            assert vokaali is None
            sana, diftongin_alku, vokaali = sana[:-2], sana[-2], sana[-1]
            vaadi(vokaali in "eoö", "väljenevä diftongi vaaditaan")
            vaadi(diftongin_alku == DIFTONGISOI[vokaali][0], "väljenevä diftongi vaaditaan")

        elif merke == HY or merke == HM:  # heittomerkki
            sana = sana.rstrip(HEITTOMERKIT)

        elif merke == P:  # edeltävän lyhyen vokaalin pidennys
            if sana[-1] == sana[-2]:
                sana = sana[:-1]

        else:
            vaadi(sana.endswith(merke), "tietty merkki vaaditaan")
            sana = sana[:-1]

    return sana, vokaali, konsonantti


def onko_etinen(sana: str) -> bool:
    """
    Palauttaa, onko sanassa etinen vokaalisointu vai ei.
    Jos sanassa on pelkästään välivokaaleita, se katsotaan etiseksi.

    :param sana: sana tai sanavartalo
    :returns: onko sanassa etinen vokaalisointu vai ei
    """

    for merkki in reversed(sana):
        if merkki.lower() in "aou":
            return False
        if merkki.lower() in "äöy":
            return True
    # sana on etinen, jos siinä on pelkkiä välivokaaleita
    return True


__all__ = ["vartalon_punoja", "puno_vartalo", "liestä_vartalo", "onko_etinen"]
