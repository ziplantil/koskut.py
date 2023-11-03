
from enum import Enum, auto
import re
from typing import Callable, Literal

from .astevaihtelu import Astevaihtelu
from .vartalo import L, V, H, K, A, O, U, D, HY, HM, HEITTOMERKKI, liestä_vartalo, onko_etinen, puno_vartalo, vartalon_punoja
from .vokaali import VOKAALIT, DIFTONGIT


class Luku(Enum):
    YKSIKKÖ = 0
    MONIKKO = 1

    YKSIKKO = 0

    YKS = 0
    MON = 1


class Sija(Enum):
    NIMENTÖ = 0
    NIMENTO = 0
    NOMINATIIVI = 0

    OMANTO = 1
    GENETIIVI = 1

    OSANTO = 2
    PARTITIIVI = 2

    SISÄOLENTO = 3
    SISAOLENTO = 3
    INESSIIVI = 3

    SISÄERONTO = 4
    SISAERONTO = 4
    ELATIIVI = 4

    SISÄTULENTO = 5
    SISATULENTO = 5
    ILLATIIVI = 5

    ULKO_OLENTO = 6
    ADESSIIVI = 6

    ULKOERONTO = 7
    ABLATIIVI = 7

    ULKOTULENTO = 8
    ALLATIIVI = 8

    OLENTO = 9
    YLEISOLENTO = 9
    ESSIIVI = 9

    TULENTO = 10
    YLEISTULENTO = 10
    TRANSLATIIVI = 10

    VAJANTO = 11
    ABESSIIVI = 11

    KEINONTO = 12
    INSTRUKTIIVI = 12

    SEURANTO = 13
    KOMITATIIVI = 13


class Omistusliite(Enum):
    NI = 1
    YKSIKKÖ_1 = 1
    YKSIKKO_1 = 1
    YKS_1 = 1
    MINUN = 1

    SI = 2
    YKSIKKÖ_2 = 2
    YKSIKKO_2 = 2
    YKS_2 = 2
    SINUN = 2

    NSA = 3
    YKSIKKÖ_3 = 3
    YKSIKKO_3 = 3
    YKS_3 = 3
    MONIKKO_3 = 3
    MON_3 = 3
    HÄNEN = 3
    HEIDÄN = 3

    MME = 4
    MONIKKO_1 = 4
    MON_1 = 4
    MEIDÄN = 4

    NNE = 5
    MONIKKO_2 = 5
    MON_2 = 5
    TEIDÄN = 5


def _vartalo_parametri_luetteloksi(arvo: str | list[str]) -> list[str]:
    if not isinstance(arvo, list):
        return [arvo]
    return arvo


class _Vartalosto():
    def __init__(self,
                 yks: str | list[str],      # (heikko) yksikkövartalo
                 yks_v: str | list[str],    # (vahva) yksikkövartalo
                 yks_n: str | list[str],    # yksikön nimennön/nominatiivin vartalo
                 yks_s: str | list[str],    # yksikön osannon/partitiivin vartalo
                 yks_t: str | list[str],    # yksikön sisätulennon/illatiivin vartalo
                 mon: str | list[str],      # (heikko) monikkovartalo
                 mon_v: str | list[str],    # (vahva) monikkovartalo
                 mon_o: str | list[str],    # monikon omannon/genetiivin vartalo
                 mon_s: str | list[str],    # monikon osannon/partitiivin vartalo
                 mon_t: str | list[str],    # monikon sisätulennon/illatiivin vartalo
                 ):
        self.yks = _vartalo_parametri_luetteloksi(yks)
        self.yks_v = _vartalo_parametri_luetteloksi(yks_v)
        self.yks_n = _vartalo_parametri_luetteloksi(yks_n)
        self.yks_s = _vartalo_parametri_luetteloksi(yks_s)
        self.yks_t = _vartalo_parametri_luetteloksi(yks_t)
        self.mon = _vartalo_parametri_luetteloksi(mon)
        self.mon_v = _vartalo_parametri_luetteloksi(mon_v)
        self.mon_o = _vartalo_parametri_luetteloksi(mon_o)
        self.mon_s = _vartalo_parametri_luetteloksi(mon_s)
        self.mon_t = _vartalo_parametri_luetteloksi(mon_t)

    def periydy(self,
                yks: str | list[str] | None = None,
                yks_v: str | list[str] | None = None,
                yks_n: str | list[str] | None = None,
                yks_s: str | list[str] | None = None,
                yks_t: str | list[str] | None = None,
                mon: str | list[str] | None = None,
                mon_v: str | list[str] | None = None,
                mon_o: str | list[str] | None = None,
                mon_s: str | list[str] | None = None,
                mon_t: str | list[str] | None = None):
        return _Vartalosto(
            yks = yks or self.yks,
            yks_v = yks_v or self.yks_v,
            yks_n = yks_n or self.yks_n,
            yks_s = yks_s or self.yks_s,
            yks_t = yks_t or self.yks_t,
            mon = mon or self.mon,
            mon_v = mon_v or self.mon_v,
            mon_o = mon_o or self.mon_o,
            mon_s = mon_s or self.mon_s,
            mon_t = mon_t or self.mon_t,
        )

    def kaikki_päätteet(self):
        return [
            *self.yks,
            *self.yks_v,
            *self.yks_n,
            *self.yks_s,
            *self.yks_t,
            *self.mon,
            *self.mon_v,
            *self.mon_o,
            *self.mon_s,
            *self.mon_t,
        ]


SIJAN_VARTALOT_YKS = {
    Sija.NIMENTÖ: "yks_n",
    Sija.OMANTO: "yks",
    Sija.OSANTO: "yks_s",
    Sija.SISÄOLENTO: "yks",
    Sija.SISÄERONTO: "yks",
    Sija.SISÄTULENTO: "yks_t",
    Sija.ULKO_OLENTO: "yks",
    Sija.ULKOERONTO: "yks",
    Sija.ULKOTULENTO: "yks",
    Sija.OLENTO: "yks_v",
    Sija.TULENTO: "yks",
    Sija.VAJANTO: "yks",
}

SIJAN_VARTALOT_MON = {
    Sija.NIMENTÖ: "yks",
    Sija.OMANTO: "mon_o",
    Sija.OSANTO: "mon_s",
    Sija.SISÄOLENTO: "mon",
    Sija.SISÄERONTO: "mon",
    Sija.SISÄTULENTO: "mon_t",
    Sija.ULKO_OLENTO: "mon",
    Sija.ULKOERONTO: "mon",
    Sija.ULKOTULENTO: "mon",
    Sija.OLENTO: "mon_v",
    Sija.TULENTO: "mon",
    Sija.VAJANTO: "mon",
    Sija.KEINONTO: "mon",
    Sija.SEURANTO: "mon_v",
}

SIJAPÄÄTTEET = {
    Sija.NIMENTÖ: "",
    Sija.OMANTO: "n",
    Sija.OSANTO: f"{A}",
    Sija.SISÄOLENTO: f"ss{A}",
    Sija.SISÄERONTO: f"st{A}",
    Sija.SISÄTULENTO: f"n",
    Sija.ULKO_OLENTO: f"ll{A}",
    Sija.ULKOERONTO: f"lt{A}",
    Sija.ULKOTULENTO: "lle",
    Sija.OLENTO: f"n{A}",
    Sija.TULENTO: "ksi",
    Sija.VAJANTO: f"tt{A}",
    Sija.KEINONTO: "n",
    Sija.SEURANTO: "ne",
}

OMISTUSLIITTEET = {
    Omistusliite.NI: "ni",
    Omistusliite.SI: "si",
    Omistusliite.NSA: f"ns{A}",
    Omistusliite.MME: "mme",
    Omistusliite.NNE: "nne",
}

_LUOKAT = [
    (1, _Vartalosto(
            yks=f"{H}{HY}{L}",  yks_v=f"{V}{L}",  yks_n=f"{V}{L}",   yks_s=f"{V}{L}",  yks_t=f"{V}{L}{L}",
            mon=f"{H}{HM}{L}i", mon_v=f"{V}{L}i", mon_o=f"{V}{L}je", mon_s=f"{V}{L}j", mon_t=f"{V}{L}ihi")),
    (2, _Vartalosto(
            yks=f"{L}",  yks_v=f"{L}",  yks_n=f"{L}",   yks_s=f"{L}",              yks_t=f"{L}{L}",
            mon=f"{L}i", mon_v=f"{L}i", mon_o=f"{L}je", mon_s=[f"{L}j", f"{L}it"], mon_t=f"{L}ihi")),
    (3, _Vartalosto(
            yks=f"{L}",  yks_v=f"{L}",  yks_n=f"{L}",                  yks_s=f"{L}t",  yks_t=f"{L}{L}",
            mon=f"{L}i", mon_v=f"{L}i", mon_o=[f"{L}ide", f"{L}itte"], mon_s=f"{L}it", mon_t=f"{L}ihi")),
    (4, _Vartalosto(
            yks=f"{H}{HY}{L}",  yks_v=f"{V}{L}",  yks_n=f"{V}{L}",   yks_s=f"{V}{L}",  yks_t=f"{V}{L}{L}",
            mon=f"{H}{HM}{L}i", mon_v=f"{V}{L}i", mon_s=[f"{V}{L}j", f"{H}{L}it"],     mon_t=f"{V}{L}ihi",
                                mon_o=[f"{V}{L}je", f"{H}{L}ide", f"{H}{L}itte"])),
    (5, _Vartalosto(
            yks=f"{H}i",  yks_v=f"{V}i",  yks_n=f"{V}i",  yks_s=f"{V}i",  yks_t=f"{V}ii",
            mon=f"{H}ei", mon_v=f"{V}ei", mon_o=f"{V}ie", mon_s=f"{V}ej", mon_t=f"{V}eihi")),
    (6, _Vartalosto(
            yks="i",  yks_v="i",  yks_n="i",                     yks_s="i",           yks_t="ii",
            mon="ei", mon_v="ei", mon_o=["ie", "eide", "eitte"], mon_s=["eit", "ej"], mon_t="eihi")),
    (7, _Vartalosto(
            yks=f"{H}e",     yks_v=f"{V}e", yks_n=f"{V}i",  yks_s=f"{V}e", yks_t=f"{V}ee",
            mon=f"{H}{HM}i", mon_v=f"{V}i", mon_o=f"{V}ie", mon_s=f"{V}i", mon_t=f"{V}ii")),
    (8, _Vartalosto(
            yks=f"{H}e",  yks_v=f"{V}e",  yks_n=f"{V}e",   yks_s=f"{V}e",  yks_t=f"{V}ee",
            mon=f"{H}ei", mon_v=f"{V}ei", mon_o=f"{V}eje", mon_s=f"{V}ej", mon_t=f"{V}eihi")),
    (9, _Vartalosto(
            yks=f"{H}{HY}{A}",  yks_v=f"{V}{A}",  yks_n=f"{V}{A}",   yks_s=f"{V}{A}",  yks_t=f"{V}{A}{A}",
            mon=f"{H}{O}i",     mon_v=f"{V}{O}i", mon_o=f"{V}{O}je", mon_s=f"{V}{O}j", mon_t=f"{V}{O}ihi")),
    (10, _Vartalosto(
            yks=f"{H}{HY}{A}",  yks_v=f"{V}{A}", yks_n=f"{V}{A}", yks_s=f"{V}{A}", yks_t=f"{V}{A}{A}",
            mon=f"{H}{HM}i",    mon_v=f"{V}i",   mon_o=f"{V}ie",  mon_s=f"{V}i",   mon_t=f"{V}ii")),
    (11, _Vartalosto(
            yks=f"{A}",         yks_v=f"{A}",         yks_n=f"{A}",            yks_s=f"{A}",          yks_t=f"{A}{A}",
            mon=["i", f"{O}i"], mon_v=["i", f"{O}i"], mon_o=["ie", f"{O}ide"], mon_s=["i", f"{O}it"], mon_t=["ii", f"{O}ihi"])),
    (12, _Vartalosto(
            yks=f"{A}",  yks_v=f"{A}",  yks_n=f"{A}",                  yks_s=f"{A}",   yks_t=f"{A}{A}",
            mon=f"{O}i", mon_v=f"{O}i", mon_o=[f"{O}ide", f"{O}itte"], mon_s=f"{O}it", mon_t=f"{O}ihi")),
    (13, _Vartalosto(
            yks=f"{A}",  yks_v=f"{A}",  yks_n=f"{A}",                  yks_s=f"{A}",              yks_t=f"{A}{A}",
            mon=f"{O}i", mon_v=f"{O}i", mon_o=[f"{O}ide", f"{O}itte"], mon_s=[f"{O}it", f"{O}j"], mon_t=f"{O}ihi")),
    (14, _Vartalosto(
            yks=f"{H}{A}",  yks_v=f"{V}{A}",  yks_n=f"{V}{A}",                                  yks_s=f"{V}{A}",                 yks_t=f"{V}{A}{A}",
            mon=f"{H}{O}i", mon_v=f"{V}{O}i", mon_o=[f"{H}{O}ide", f"{H}{O}itte", f"{V}{O}je"], mon_s=[f"{H}{O}it", f"{V}{O}j"], mon_t=[f"{V}{O}ihi", f"{H}{O}ihi"])),
    (15, _Vartalosto(
            yks=f"{A}", yks_v=f"{A}", yks_n=f"{A}", yks_s=[f"{A}", f"{A}t"], yks_t=f"{A}{A}",
            mon="i",    mon_v="i",    mon_o="ide",  mon_s="it",              mon_t=["isii", "ihi"])),
    (16, _Vartalosto(
            yks=f"{H}{A}",  yks_v=f"{V}{A}", yks_n=f"{V}i",  yks_s=f"{V}{A}", yks_t=f"{V}{A}{A}",
            mon=f"{H}i",    mon_v=f"{V}i",   mon_o=f"{V}ie", mon_s=f"{V}i",   mon_t=f"{V}ii")),
    (17, _Vartalosto(
            yks=f"{L}", yks_v=f"{L}", yks_n=f"{L}", yks_s=f"{L}t", yks_t=f"{L}see",
            mon="i",    mon_v="i",    mon_o="ide",  mon_s="it",    mon_t="isii")),
    (18, _Vartalosto(
            yks=f"{L}", yks_v=f"{L}", yks_n=f"{L}", yks_s=f"{L}t", yks_t=f"{L}h{L}",
            mon="i",    mon_v="i",    mon_o="ide",  mon_s="it",    mon_t="ihi")),
    (19, _Vartalosto(
            yks=f"{D}",  yks_v=f"{D}",  yks_n=f"{D}",    yks_s=f"{D}t",  yks_t=f"{D}h{L}",
            mon=f"{L}i", mon_v=f"{L}i", mon_o=f"{L}ide", mon_s=f"{L}it", mon_t=f"{L}ihi")),
    (20, _Vartalosto(
            yks=f"{L}", yks_v=f"{L}", yks_n=f"{L}", yks_s=f"{L}t", yks_t=[f"{L}h{L}", f"{L}see"],
            mon="i",    mon_v="i",    mon_o="ide",  mon_s="it",    mon_t=["ihi", "isii"])),
    (21, _Vartalosto(
            yks="",  yks_v="",  yks_n="",    yks_s="t",  yks_t=f"h{L}",
            mon="i", mon_v="i", mon_o="ide", mon_s="it", mon_t="ihi")),
    (22, _Vartalosto(
            yks=HEITTOMERKKI,       yks_v=HEITTOMERKKI,       yks_n="",                   yks_s=HEITTOMERKKI + "t",  yks_t=HEITTOMERKKI + f"h{L}",
            mon=HEITTOMERKKI + "i", mon_v=HEITTOMERKKI + "i", mon_o=HEITTOMERKKI + "ide", mon_s=HEITTOMERKKI + "it", mon_t=HEITTOMERKKI + "ihi")),
    (23, _Vartalosto(
            yks="e", yks_v="e", yks_n="i",  yks_s="t", yks_t="ee",
            mon="i", mon_v="i", mon_o="ie", mon_s="i", mon_t="ii")),
    (24, _Vartalosto(
            yks="e", yks_v="e", yks_n="i",          yks_s="t", yks_t="ee",
            mon="i", mon_v="i", mon_o=["ie", "te"], mon_s="i", mon_t="ii")),
    (25, _Vartalosto(
            yks="me", yks_v="me", yks_n="mi",           yks_s=["nt", "me"], yks_t="mee",
            mon="mi", mon_v="mi", mon_o=["mie", "nte"], mon_s="mi",         mon_t="mii")),
    (26, _Vartalosto(
            yks="e", yks_v="e", yks_n="i",          yks_s="t", yks_t="ee",
            mon="i", mon_v="i", mon_o=["te", "ie"], mon_s="i", mon_t="ii")),
    (27, _Vartalosto(
            yks="de", yks_v="te", yks_n="si",           yks_s="tt", yks_t="tee",
            mon="si", mon_v="si", mon_o=["sie", "tte"], mon_s="si", mon_t="sii")),
    (28, _Vartalosto(
            yks=f"{H}e",  yks_v=f"{V}e",  yks_n=f"{K}si",              yks_s=f"{V}t",  yks_t=f"{V}ee",
            mon=f"{K}si", mon_v=f"{K}si", mon_o=[f"{K}sie", f"{V}te"], mon_s=f"{K}si", mon_t=f"{K}sii")),
    (29, _Vartalosto(
            yks=f"{K}se", yks_v=f"{K}se", yks_n=f"{K}si",           yks_s="st",     yks_t=f"{K}see",
            mon=f"{K}si", mon_v=f"{K}si", mon_o=["ste", f"{K}sie"], mon_s=f"{K}si", mon_t=f"{K}sii")),
    (30, _Vartalosto(
            yks="tse", yks_v="tse", yks_n="tsi",           yks_s="st",  yks_t="tsee",
            mon="tsi", mon_v="tsi", mon_o=["tsie", "ste"], mon_s="tsi", mon_t="tsii")),
    (31, _Vartalosto(
            yks="hde", yks_v="hte", yks_n="ksi",  yks_s="ht",  yks_t="htee",
            mon="ksi", mon_v="ksi", mon_o="ksie", mon_s="ksi", mon_t="ksii")),
    (32, _Vartalosto(
            yks=f"{V}{L}{K}e", yks_v=f"{V}{L}{K}e", yks_n=f"{H}{L}{K}",                     yks_s=f"{H}{L}{K}t", yks_t=f"{V}{L}{K}ee",
            mon=f"{V}{L}{K}i", mon_v=f"{V}{L}{K}i", mon_o=[f"{V}{L}{K}ie", f"{H}{L}{K}te"], mon_s=f"{V}{L}{K}i", mon_t=f"{V}{L}{K}ii")),
    (33, _Vartalosto(
            yks=f"{V}{L}me", yks_v=f"{V}{L}me", yks_n=f"{H}{L}n",                   yks_s=f"{H}{L}nt", yks_t=f"{V}{L}mee",
            mon=f"{V}{L}mi", mon_v=f"{V}{L}mi", mon_o=[f"{V}{L}mie", f"{H}{L}nte"], mon_s=f"{V}{L}mi", mon_t=f"{V}{L}mii")),
    (34, _Vartalosto(
            yks=f"{V}{L}m{A}", yks_v=f"{V}{L}m{A}", yks_n=f"{H}{L}n",                   yks_s=f"{H}{L}nt", yks_t=f"{V}{L}m{A}{A}",
            mon=f"{V}{L}mi",   mon_v=f"{V}{L}mi",   mon_o=[f"{V}{L}mie", f"{H}{L}nte"], mon_s=f"{V}{L}mi", mon_t=f"{V}{L}mii")),
    (35, _Vartalosto(
            yks=f"{V}{L}m{A}", yks_v=f"{V}{L}m{A}", yks_n=f"{H}{L}n",                   yks_s=f"{H}{L}nt", yks_t=f"{V}{L}m{A}{A}",
            mon=f"{V}{L}mi",   mon_v=f"{V}{L}mi",   mon_o=[f"{V}{L}mie", f"{H}{L}nte"], mon_s=f"{V}{L}mi", mon_t=f"{V}{L}mii")),
    (36, _Vartalosto(
            yks=f"imm{A}", yks_v=f"imp{A}", yks_n=f"in",             yks_s="int",  yks_t=f"imp{A}{A}",
            mon="immi",    mon_v="impi",    mon_o=["impie", "inte"], mon_s="impi", mon_t="impii")),
    (37, _Vartalosto(
            yks=f"mm{A}", yks_v=f"mp{A}", yks_n=f"n",            yks_s=["nt", f"mp{A}"], yks_t=f"mp{A}{A}",
            mon="mmi",    mon_v="mpi",    mon_o=["mpie", "nte"], mon_s="mpi",            mon_t="mpii")),
    (38, _Vartalosto(
            yks="se", yks_v="se", yks_n="nen",          yks_s="st", yks_t="see",
            mon="si", mon_v="si", mon_o=["ste", "sie"], mon_s="si", mon_t="sii")),
    (39, _Vartalosto(
            yks="kse", yks_v="kse", yks_n="s",             yks_s="st",  yks_t="ksee",
            mon="ksi", mon_v="ksi", mon_o=["ste", "ksie"], mon_s="ksi", mon_t="ksii")),
    (40, _Vartalosto(
            yks="de",  yks_v="te",  yks_n="s",    yks_s="tt",  yks_t="tee",
            mon="ksi", mon_v="ksi", mon_o="ksie", mon_s="ksi", mon_t="ksii")),
    (41, _Vartalosto(
            yks=f"{V}{L}{L}", yks_v=f"{V}{L}{L}", yks_n=f"{H}{L}s",                    yks_s=f"{H}{L}st", yks_t=f"{V}{L}{L}see",
            mon=f"{V}{L}i",   mon_v=f"{V}{L}i",   mon_o=[f"{V}{L}ide", f"{V}{L}itte"], mon_s=f"{V}{L}it", mon_t=f"{V}{L}isii")),
    (42, _Vartalosto(
            yks="he", yks_v="he", yks_n="s",            yks_s="st", yks_t="hee",
            mon="hi", mon_v="hi", mon_o=["ste", "hie"], mon_s="hi", mon_t="hii")),
    (43, _Vartalosto(
            yks=f"{V}{L}e", yks_v=f"{V}{L}e", yks_n=f"{H}{L}t",   yks_s=f"{H}{L}tt", yks_t=f"{V}{L}ee",
            mon=f"{V}{L}i", mon_v=f"{V}{L}i", mon_o=f"{V}{L}ide", mon_s=f"{V}{L}it", mon_t=[f"{V}{L}isii", f"{V}{L}ihi"])),
    (44, _Vartalosto(
            yks=f"{V}{L}{L}", yks_v=f"{V}{L}{L}", yks_n=f"{H}{L}t",   yks_s=f"{H}{L}tt", yks_t=f"{V}{L}{L}see",
            mon=f"{V}{L}i",   mon_v=f"{V}{L}i",   mon_o=f"{V}{L}ide", mon_s=f"{V}{L}it", mon_t=[f"{V}{L}isii", f"{V}{L}ihi"])),
    (45, _Vartalosto(
            yks="nne", yks_v="nte", yks_n="s",    yks_s="tt",  yks_t="ntee",
            mon="nsi", mon_v="nsi", mon_o="nsie", mon_s="nsi", mon_t="nsii")),
    (46, _Vartalosto(
            yks="nne", yks_v="nte", yks_n="t",    yks_s="tt",  yks_t="ntee",
            mon="nsi", mon_v="nsi", mon_o="nsie", mon_s="nsi", mon_t="nsii")),
    (47, _Vartalosto(
            yks="ee", yks_v="ee", yks_n=f"{U}t",            yks_s=f"{U}tt", yks_t="eesee",
            mon="ei", mon_v="ei", mon_o=["eide", "eitte"],  mon_s="eit",    mon_t="eisii")),
    (48, _Vartalosto(
            yks=f"{V}{L}{L}", yks_v=f"{V}{L}{L}", yks_n=f"{H}{L}",    yks_s=f"{H}{L}tt", yks_t=f"{V}{L}{L}see",
            mon=f"{V}{L}i",   mon_v=f"{V}{L}i",   mon_o=f"{V}{L}ide", mon_s=f"{V}{L}it", mon_t=[f"{V}{L}isii", f"{V}{L}ihi"])),
    (49, _Vartalosto(
            yks=f"{V}{L}{K}{L}{L}", yks_v=f"{V}{L}{K}{L}{L}", yks_n=f"{H}{L}{K}",       yks_s=f"{H}{L}{K}t",     yks_t=f"{V}{L}{K}{L}{L}see",
            mon=f"{V}{L}{K}{L}i",   mon_v=f"{V}{L}{K}{L}i",   mon_o=f"{V}{L}{K}{L}ide", mon_s=f"{V}{L}{K}{L}it", mon_t=[f"{V}{L}{K}{L}isii", f"{V}{L}{K}{L}ihi"])),
]

_LUOKAT_NUMEROITTAIN = {numero: vartalosto for numero, vartalosto in _LUOKAT}
_risti_ilman_i = _LUOKAT_NUMEROITTAIN[5].periydy(yks_n=f"{H}")
_paperi_ilman_i = _LUOKAT_NUMEROITTAIN[6].periydy(yks_n=f"{H}")

_risti_lyhenne = _Vartalosto(
            yks=":",   yks_v=":",   yks_n="",    yks_s=":",   yks_t=":i",
            mon=":ei", mon_v=":ei", mon_o=":ie", mon_s=":ej", mon_t=":eihi")
_kala_lyhenne = _Vartalosto(
            yks=":",      yks_v=":",      yks_n="",        yks_s=":",      yks_t=f":{A}{A}",
            mon=f":{O}i", mon_v=f":{O}i", mon_o=f":{O}je", mon_s=f":{O}i", mon_t=f":{O}ihi")
_koira_lyhenne = _Vartalosto(
            yks=":",  yks_v=":",  yks_n="",    yks_s=":",  yks_t=f":{A}{A}",
            mon=":i", mon_v=":i", mon_o=":ie", mon_s=":i", mon_t=":ii")
_maa_lyhenne = _Vartalosto(
            yks=":",  yks_v=":",  yks_n="",     yks_s=f":t", yks_t=f":h{L}",
            mon=":i", mon_v=":i", mon_o=":ide", mon_s=":it", mon_t=":ihi")

_LYHENNELUOKAT_NUMEROITTAIN = {
    5: _risti_lyhenne,
    9: _kala_lyhenne,
    10: _koira_lyhenne,
    18: _maa_lyhenne
}

# yksittäisten kirjainten taivutukset, loppuvokaalit ja vokaalisoinnut
_KIRJAINTEN_TAIVUTUKSET = {
    "a": (18, "a", "a"),
    "b": (18, "e", "ä"),
    "c": (18, "e", "ä"),
    "d": (18, "e", "ä"),
    "e": (18, "e", "ä"),
    "f": (10, None, "ä"),
    "g": (18, "e", "ä"),
    "h": (18, "o", "a"),
    "i": (18, "i", "ä"),
    "j": (18, "i", "ä"),
    "k": (18, "o", "a"),
    "l": (10, None, "ä"),
    "m": (10, None, "ä"),
    "n": (10, None, "ä"),
    "o": (18, "o", "a"),
    "p": (18, "e", "ä"),
    "q": (18, "u", "a"),
    "r": (10, None, "ä"),
    "s": (10, None, "ä"),
    "š": (10, None, "ä"),
    "t": (18, "e", "ä"),
    "u": (18, "u", "a"),
    "v": (18, "e", "ä"),
    "w": (18, "e", "ä"),
    "x": (10, None, "ä"),
    "y": (18, "y", "ä"),
    "z": (9, None, "a"),
    "ž": (9, None, "a"),
    "ä": (18, "ä", "ä"),
    "ö": (18, "ö", "ä"),
    ...: (10, None, "a")
}


def _liestä_nimisanan_vartalo(sana: str, vartalosto: _Vartalosto,
                              aste: Astevaihtelu | None,
                              vokaali: str | None,
                              konsonantti: str | None,
                              monikko: bool) -> tuple[str, str | None, str | None]:
    if monikko:
        päätteet = [x + "t" for x in vartalosto.yks]
    else:
        päätteet = vartalosto.yks_n

    vartalo, vokaali2 = None, None
    for pääte in päätteet:
        try:
            vartalo, vokaali2, konsonantti = liestä_vartalo(sana, pääte, aste)
        except ValueError:
            pass

    if vartalo is None:
        raise ValueError("sana ei vastaa kyseistä taivutustyyppiä")

    if vokaali is not None and vokaali2 is not None and vokaali != vokaali2:
        raise ValueError(f"annettu loppuvokaali {vokaali} on eri kuin sanasta tunnistettu {vokaali2}")

    if vokaali is None:
        vokaali = vokaali2

    return vartalo, vokaali, konsonantti


def _liitä(alku: str, loppu: str, suo: bool, aika: bool):
    if suo and alku[-1:] == loppu[:1]:
        return alku + "-" + loppu
    if aika and alku[-1:] == "i" and loppu[0] in VOKAALIT:
        return alku[:-1] + "j" + loppu
    return alku + loppu


DIFTONGISOI = {"ee": "ie", "oo": "uo", "öö": "yö"}


# laskee mieluummin yläkanttiin
def _tavuja(sana: str) -> int:
    return len(re.findall(r"(?:^[^aeiouyäö]*(ie|uo|yö|[aeio]u|[äeiö]y)|[aeouyäö]i|(?:[aeio]u|[äeiö]y)(?=[aeiouyäö]|[bcdfghjklmnpqrsštvwxzž][aeiouyäö])|aa|ee|ii|oo|uu|yy|ää|öö|([aeiouyäö]))", sana))


class Nimisana():
    def __init__(self, sana: str, luokka: int,
                 aste: Astevaihtelu | str | tuple[str, str] | None = None,
                 loppuvokaali: str | None = None,
                 sointu: Literal["A", "a", "Ä", "ä"] | None = None,
                 vain_yksikkö: bool = False,
                 vain_yksikko: bool = False,
                 vain_monikko: bool = False,
                 pakota_alisteiset_sijat_monikkoon: bool = False,
                 meri: bool = False,
                 aika: bool = False,
                 lyhenne: bool = False):
        """
        Nimisana eli nomini, jota voi taivuttaa nimisanojen taivutuskaavojen mukaisesti.

        :param sana: sanan perusmuoto (nimennön eli nominatiivin yksikkö, tai monikko jos sanalla ei ole yksikköä)
        :param luokka: Kielitoimiston sanakirjan mukainen taivutusluokka (1-49)
        :param aste: sanan astevaihtelu: joko Astevaihtelu-olio, monikko jossa on vahva ja heikko aste, Kielitoimiston sanakirjan astevaihtelutunnus (A-M) tai tyhjä, jos sanassa ei ole astevaihtelua. jos luokka vaatii astevaihtelun eikä sitä anneta, se voidaan päätellä
        :param loppuvokaali: sanan loppuvokaali. usein tunnistetaan automaattisesti, mutta täytyy määrittää tyypeille 21, 22 (joita käytetään vain vierassanoille)
        :param sointu: sanan vokaalisointu, kannattaa aina määrittää itse
        :param vain_yksikkö: jos sanalla on vain yksikkömuodot
        :param vain_monikko: jos sanalla on vain monikkomuodot
        :param pakota_alisteiset_sijat_monikkoon: pakotetaanko alisteiset eli obliikvisijat monikkoon (esim. Ikaalinen -> Ikaalisissa). vaatii, että vain_yksikkö annetaan, ja olettaa, että taivuta.lle annetaan aina yksikkö luvuksi
        :param meri: tapaus meri/veri: partitiivin yksikkö päättyy A:han, vaikka sana olisi muuten etinen
        :param aika: tapaus aika/poika: heikolla asteella vartalon viimeinen i korvataan j:llä
        :param lyhenne: käytetäänkö lyhennetaivutusta (toimii vain osalle luokista)
        :returns: taivutettava nimisana
        :raises ValueError: jos taivutusluokka tai astevaihtelu on kelpaamaton, tai jos sanan perusmuoto ei vaikuta sopivan taivutusluokkaan
        """

        if lyhenne:
            try:
                _vartalosto = _LYHENNELUOKAT_NUMEROITTAIN[luokka]
            except KeyError:
                raise ValueError(f"tuntematon lyhennetaivutusluokka {luokka}")
            if aste:
                raise ValueError("lyhenteissä ei voi olla astevaihtelua")
            if _vartalosto is _maa_lyhenne and not loppuvokaali:
                loppuvokaali = "e"
        else:
            try:
                _vartalosto = _LUOKAT_NUMEROITTAIN[luokka]
            except KeyError:
                raise ValueError(f"tuntematon taivutusluokka {luokka}")
            
        # i:ttömät vartalostot ovat poikkeustapauksia
        if luokka == 5 and not sana.endswith("i"):
            _vartalosto = _risti_ilman_i
        elif luokka == 6 and not sana.endswith("i"):
            _vartalosto = _paperi_ilman_i

        vain_yksikkö = vain_yksikkö or vain_yksikko
        if vain_yksikkö and vain_monikko:
            raise ValueError("sanalla ei voi samaan aikaan olla vain yksikköä ja vain monikkoa")

        if pakota_alisteiset_sijat_monikkoon and not vain_yksikkö:
            raise ValueError("pakota_alisteiset_sijat_monikkoon vaatii vain_yksikkö-asetuksen")

        # astevaihtelut
        if isinstance(aste, str):
            if len(aste) != 1:
                raise ValueError(f"tuntematon astevaihtelutyyppi {aste}")
            try:
                aste = getattr(Astevaihtelu, "KOTUS_" + aste.upper())
            except AttributeError:
                raise ValueError(f"tuntematon astevaihtelutyyppi {aste}")
        elif isinstance(aste, tuple):
            aste = Astevaihtelu.hae(aste)

        self._etinen = onko_etinen(sointu or sana)

        if aika and (luokka not in {9, 10} or not aste or aste.heikko != "" or self._etinen):
            raise ValueError("aika vaatii taivutusluokan 9 tai 10, astevaihtelun D (k : ) ja takavokaalit")
        if meri and luokka not in {24, 26}:
            raise ValueError("meri vaatii taivutusluokan 24 tai 26")
        if pakota_alisteiset_sijat_monikkoon and luokka != 38:
            raise ValueError("pakota_alisteiset_sijat_monikkoon vaatii taivutusluokan 38")

        self._vartalo, self._vokaali, self._konsonantti = _liestä_nimisanan_vartalo(sana, _vartalosto, aste, loppuvokaali, None, vain_monikko)
        self._luokka = luokka
        self._päätteet = _vartalosto
        self._aste = aste
        self._yksikkö = not vain_monikko
        self._monikko = not vain_yksikkö
        self._meri = meri
        self._aika = aika
        self._pakota_alisteiset_sijat_monikkoon = pakota_alisteiset_sijat_monikkoon
        self._lyhenne = lyhenne

        # loppukonsonantti joillekin tyypeistä
        if self._aste and self._aste.vahva[-1] == "t" and not self._konsonantti:
            self._konsonantti = self._aste.heikko[:-1]
        elif not self._aste and self._luokka == 28:
            if self._konsonantti == "l":
                self._aste = Astevaihtelu.LT_LL
            elif self._konsonantti == "n":
                self._aste = Astevaihtelu.NT_NN
            elif self._konsonantti == "r":
                self._aste = Astevaihtelu.RT_RR

        # taivutusluokkakohtaiset tarkistukset
        kelpaa = True
        if self._luokka in {4, 14}:
            if not self._aste or len(self._aste.vahva) < 2:
                kelpaa = False
        elif self._luokka == 16:
            if not self._aste or self._aste.vahva != "mp" or self._aste.heikko != "mm":
                kelpaa = False
        elif self._luokka == 28:
            if not self._aste or len(self._aste.vahva) == 1 or self._aste.vahva[-1:] != "t":
                kelpaa = False
        elif self._luokka == 34:
            if self._aste and self._aste.vahva != "tt":
                kelpaa = False
        elif self._aste:
            if not any(H in pääte or V in pääte for pääte in self._päätteet.kaikki_päätteet()):
                kelpaa = False

        if not kelpaa:
            raise ValueError(f"astevaihtelu {aste} ei sovi yhteen taivutusluokan {luokka} kanssa")

        # taivutusluokkakohtaiset poikkeukset
        heittomerkki_yksikköön = False
        heittomerkki_monikkoon = False

        if self._aste and self._aste.heikko == "":
            # 1 (valo)
            if self._luokka == 1:
                if self._vartalo.endswith(self._vokaali):
                    heittomerkki_monikkoon = True
                    if any(self._vartalo.endswith(d) for d in DIFTONGIT):
                        heittomerkki_yksikköön = True

            # 7 (ovi)
            elif self._luokka == 7:
                if self._vartalo.endswith("i"):
                    heittomerkki_monikkoon = True

            # 9 (kala)
            elif self._luokka == 9:
                if self._vartalo.endswith("aa") or self._vartalo.endswith("ää"):
                     heittomerkki_yksikköön = True

            # 10 (koira)
            elif self._luokka == 10:
                if self._vartalo.endswith("aa") or self._vartalo.endswith("ää"):
                    heittomerkki_yksikköön = True
                if self._vartalo.endswith("i"):
                    heittomerkki_monikkoon = True

        self._heittomerkki_yksikköön = heittomerkki_yksikköön
        self._heittomerkki_monikkoon = heittomerkki_monikkoon

        # 19 (suo)
        self._diftongisoi = self._luokka == 19
        if self._diftongisoi:
            self._vartalo = self._vartalo.rstrip("-")

        if not any(L in pääte for pääte in self._päätteet.kaikki_päätteet()):
            self._vokaali = None
        if not any(K in pääte for pääte in self._päätteet.kaikki_päätteet()):
            self._konsonantti = None

        self._punoja = vartalon_punoja(self._aste, self._etinen, self._vokaali, self._konsonantti,
                                       heittomerkki_yksikköön, heittomerkki_monikkoon)


    def kotus(self):
        """Palauttaa taivutusluokan Kielitoimiston sanakirjan ilmaisemassa muodossa."""
        tulos = str(self._luokka)
        if self._aste:
            tulos += "*"
            if self._aste.kotus:
                tulos += self._aste.kotus
        return tulos


    def astevaihtelu(self):
        """Palauttaa sanan astevaihtelun, jos sillä on sellainen."""
        return self._aste


    def loppuvokaali(self):
        """Palauttaa sanan loppuvokaalin, jos taivutusluokalla on erillinen loppuvokaali."""
        if any(L in pääte for pääte in self._päätteet.kaikki_päätteet()):
            return self._vokaali
        else:
            return None


    def loppukonsonantti(self):
        """Palauttaa sanan loppukonsonantin, jos taivutusluokalla on erillinen loppukonsonantti."""
        if any(K in pääte for pääte in self._päätteet.kaikki_päätteet()):
            return self._konsonantti
        else:
            return None


    def sointu(self):
        """Palauttaa vokaalisoinnun mukaisen A-äänteen, joko a tai ä."""
        return "ä" if self._etinen else "a"


    def koskut(self):
        """Palauttaa taivutuksen koskut-C-kirjaston muodossa: vartalo ja kt_nomtaiv-tunnus."""
        
        if self._vokaali:
            vokaali = "iaoueäöy".find(self._vokaali)
        else:
            vokaali = 0

        if self._luokka in {1, 9, 10}:
            heitto = self._heittomerkki_yksikköön
        elif self._luokka == 38:
            heitto = self._pakota_alisteiset_sijat_monikkoon
        else:
            heitto = self._heittomerkki_monikkoon

        aste = self._aste
        if aste:
            if aste.vahva == "gg" and aste.heikko == "g":
                aste = 28
            elif aste.vahva == "bb" and aste.heikko == "b":
                aste = 29
            elif aste.vahva == "dd" and aste.heikko == "d":
                aste = 30
            elif not aste.kotus:
                raise ValueError("ei voida esittää C-koskuen muodossa")
            else:
                aste = ord(self._aste.kotus) - ord("A") + 1
                if aste not in range(1, 14):
                    raise ValueError("ei voida esittää C-koskuen muodossa")
        elif (self._pakota_alisteiset_sijat_monikkoon
                or self._vartalosto is _risti_ilman_i
                or self._vartalosto is _paperi_ilman_i):
            aste = 31
        else:
            aste = 0

        if self._luokka not in range(1, 50):
            raise ValueError("ei voida esittää C-Koskuen muodossa")

        luokka = self._luokka
        # C-Koskuen vaatimat astevaihtelut
        if luokka == 16:
            assert aste == 8
        elif luokka in {27, 40}:
            assert aste == 0
            aste = 6
        elif luokka == 28:
            assert aste in {9, 10, 11}
        elif luokka == 34:
            assert aste in {0, 3}
        elif luokka in {36, 37}:
            assert aste == 0
            aste = 8
        elif luokka in {45, 46}:
            assert aste == 0
            aste = 10

        # C-Koskuen vaatimat loppuvokaalit
        if luokka in {5, 6}:
            vokaali = 0  # i
        elif luokka in {7, 8, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                        38, 39, 40, 42, 45, 46}:
            vokaali = 4  # e
        elif luokka in {9, 10} and ((self._heittomerkki_monikkoon and self._etinen) or (self._aika and not self._etinen)):
            vokaali = 0  # i
        elif luokka in {9, 10, 11, 12, 13, 14, 15, 16, 36, 37, 44}:
            vokaali = 5 if self._etinen else 1  # Ä/A
        elif luokka == 34:
            vokaali = 6 if self._etinen else 2  # Ö/O
        elif luokka == 47:
            vokaali = 7 if self._etinen else 3  # Y/U
        elif luokka in {32, 49}:
            # sekavampi, ks. C-Koskuen tiedot
            if self._konsonantti == "l":
                vokaali = 0
            elif self._konsonantti == "n":
                vokaali = 1
            elif self._konsonantti == "r":
                vokaali = 2
            else:
                raise ValueError("ei voida esittää C-Koskuen muodossa")
            if self._vokaali in {"a", "ä"}:
                pass
            elif self._vokaali == "e":
                vokaali |= 4
            else:
                raise ValueError("ei voida esittää C-Koskuen muodossa")

        if self._lyhenne:
            if luokka == 10:
                luokka = 62
            elif luokka == 18:
                luokka = 63
            else:
                raise ValueError("ei voida esittää C-Koskuen muodossa")

        tunnus = (((1 if self._etinen else 0) << 15)
               | ((1 if heitto else 0) << 14)
               | (luokka << 8)
               | (aste << 3) | vokaali)

        return self._vartalo, tunnus


    def taivuta(self, sija: Sija,
                      luku: Luku | None = None,
                      omistus: Omistusliite | None = None):
        """
        Taivuttaa nimisanaa valitussa sijamuodossa, luvussa ja mahdollisesti lisää omistusliitteen.

        :param sija: sijamuoto
        :param luku: yksikkö tai monikko
        :param omistus: omistusliite, jos sanassa kuuluu olla sellainen
        :returns: luettelo taivutusmuodoista, jokseekseenkin yleisyysjärjestyksessä taivutusluokan sanoille
        :raises ValueError: tuntematon sija, luku tai omistusliite
        """
        if luku is None:
            luku = Luku.MONIKKO if not self._yksikkö else Luku.YKSIKKÖ

        if luku == Luku.YKSIKKÖ and not self._yksikkö:
            return []
        elif luku == Luku.MONIKKO and not self._monikko:
            return []

        if self._pakota_alisteiset_sijat_monikkoon:
            luku = Luku.MONIKKO if sija != Sija.NIMENTÖ else Luku.YKSIKKÖ

        if omistus:
            try:
                omistaja = OMISTUSLIITTEET[omistus]
            except AttributeError:
                raise ValueError(f"tuntematon omistusliite {omistus}")
        else:
            omistaja = ""

        if omistus and sija == Sija.KEINONTO:
            return []

        sijapääte = ""
        lyhyt_liite = omistus == Omistusliite.NSA and not (sija == Sija.NIMENTÖ or sija == Sija.OMANTO)
        if omistus and (sija == Sija.NIMENTÖ
                    or (luku == Luku.YKSIKKÖ and sija == Sija.OMANTO)):
            # omistusmuoto yks./mon. nom. + yks. gen. on aina vahva
            päätteet = self._päätteet.yks_v
        
        else:
            try:
                if luku == Luku.MONIKKO:
                    sijan_vartalo = SIJAN_VARTALOT_MON[sija]
                else:
                    sijan_vartalo = SIJAN_VARTALOT_YKS[sija]
                
                if luku == Luku.MONIKKO and sija == Sija.NIMENTÖ:
                    sijapääte = "t"
                else:
                    sijapääte = SIJAPÄÄTTEET[sija]
            except AttributeError:
                if sija in SIJAN_VARTALOT_MON:
                    return []
                raise ValueError(f"tuntematon sija {sija}")
            päätteet = getattr(self._päätteet, sijan_vartalo)

            # -n- + OMISTUSLIITE => -0- + OMISTUSLIITE
            if omistaja:
                if sija == Sija.TULENTO and sijapääte.endswith("i"):
                    # translatiivi omistusmuodoissa -ksi > -kse-
                    sijapääte = sijapääte[:-1] + "e"
                else:
                    sijapääte = sijapääte.rstrip("n")

            if self._meri and sija == Sija.OSANTO and luku == Luku.YKSIKKÖ:
                sijapääte = sijapääte.replace(A, "a")

        muodot = []
        for pääte in päätteet:
            if lyhyt_liite:
                omistukseton_muoto = _liitä(self._vartalo, puno_vartalo(pääte + sijapääte, self._punoja), self._diftongisoi, self._aika)
                if len(omistukseton_muoto) > 2 and omistukseton_muoto[-1] in "aäe" and omistukseton_muoto[-2] != omistukseton_muoto[-1]:
                    muodot.append(omistukseton_muoto + omistukseton_muoto[-1] + "n")
            muodot.append(_liitä(self._vartalo, puno_vartalo(pääte + sijapääte + omistaja, self._punoja), self._diftongisoi, self._aika))

        return muodot


    def taivuta1(self, sija: Sija,
                       luku: Luku | None = None,
                       omistus: Omistusliite | None = None):
        """
        Taivuttaa nimisanaa valitussa sijamuodossa, luvussa ja mahdollisesti lisää omistusliitteen, ja palauttaa vain yhden muodon.

        :param sija: sijamuoto
        :param luku: yksikkö tai monikko
        :param omistus: omistusliite, jos sanassa kuuluu olla sellainen
        :returns: taivutettu sanamuoto
        :raises ValueError: tuntematon sija, luku tai omistusliite, tai jos sanalla ei ole pyydettyä muotoa
        """
        muodot = self.taivuta(sija, luku, omistus)
        if not len(muodot):
            raise ValueError("sanalla ei ole annettua muotoa")
        return muodot[0]


    @staticmethod
    def koskuesta(vartalo: str, tunnus: int):
        """
        Luo C-Koskuen vartalon ja tunnuksen pohjalta nimisanan.

        :param sana: sanan vartalo Koskuen muodossa
        :param tunnus: kt_nomtaiv-tunnus
        :returns: taivutettava nimisana
        """

        etinen = bool(tunnus >> 15)
        heitto = bool((tunnus >> 14) & 1)
        luokka = (tunnus >> 8) & 63
        aste = (tunnus >> 3) & 31
        vokaali = tunnus & 7
        konsonantti = None

        pakota_alisteiset_sijat_monikkoon = False
        meri = False
        aika = False
        lyhenne = False
        ei_i = False

        if luokka not in range(1, 50):
            if luokka == 62:
                luokka = 10
                lyhenne = True
            elif luokka == 63:
                luokka = 18
                lyhenne = True
            else:
                raise ValueError("annettu tunnus ei ole kelvollinen kt_nomtaiv-tunnus")

        if luokka in {32, 49}:
            konsonantti = "lnrl"[vokaali & 3]
            vokaali = 4 if vokaali >= 4 else (5 if etinen else 1)

        elif luokka in {5, 6}:
            if aste == 31:
                ei_i = True
                aste = 0

        elif luokka in {24, 26}:
            if aste == 31:
                meri = True
                aste = 0

        elif luokka in {9, 10}:
            if vokaali == 0 and not etinen:
                aika = True

        elif luokka in {27, 36, 37, 40, 45, 46}:
            aste = 0

        elif luokka == 38:
            if heitto:
                pakota_alisteiset_sijat_monikkoon = True

        if aste == 28:
            aste = Astevaihtelu.hae("gg", "g")
        elif aste == 29:
            aste = Astevaihtelu.hae("bb", "b")
        elif aste == 30:
            aste = Astevaihtelu.hae("dd", "d")
        elif aste in range(1, 14):
            aste = "ADCDEFGHIJKLM"[aste - 1]
            aste = getattr(Astevaihtelu, "KOTUS_" + aste)
        else:
            aste = None

        vokaali = "iaoueäöy"[vokaali]

        if lyhenne:
            sana = vartalo
        else:
            vartalosto = _LUOKAT_NUMEROITTAIN[luokka]
            punoja = vartalon_punoja(aste, etinen, vokaali, konsonantti, False, False)
            sana = _liitä(vartalo, puno_vartalo(vartalosto.yks_n[0], punoja), False, aika)

        return Nimisana(sana=sana, luokka=luokka, aste=aste, loppuvokaali=vokaali,
                        sointu="ä" if etinen else "a",
                        pakota_alisteiset_sijat_monikkoon=pakota_alisteiset_sijat_monikkoon,
                        meri=meri, aika=aika, lyhenne=lyhenne)


    @staticmethod
    def varataivutus(sana: str,
                     sointu: Literal["A", "a", "Ä", "ä"] | None = None,
                     lyhenne: bool | None = None,
                     vain_yksikkö: bool = False,
                     vain_yksikko: bool = False):
        """
        Palauttaa nimisanan varataivutuksen, eli perustaivutuksen joita voi käyttää esim. vieraskielisille nimille.
        Varataivutus on käytännössä aina väärin suomenkielisille sanoille!

        :param sana: sanan perusmuoto (nimennön eli nominatiivin yksikkö)
        :param sointu: sanan vokaalisointu, kannattaa aina määrittää itse jos on tiedossa
        :param lyhenne: onko sana lyhenne vai ei; jos ei määritellä, päätellään sanan lopusta (loppuuko isoon kirjaimeen vai ei)
        :param vain_yksikkö: onko sanalla vain yksikkömuodot
        :returns: taivutettava nimisana
        """
        if lyhenne is None:
            lyhenne = sana[-1] != sana[-1].lower()
        if not sana:
            lyhenne = True
        vain_yksikkö = vain_yksikkö or vain_yksikko

        etinen = onko_etinen(sointu or sana)

        viimeinen = sana[-1:].lower()        
        if lyhenne:
            luokka, loppuvokaali, sointu = _KIRJAINTEN_TAIVUTUKSET.get(viimeinen, _KIRJAINTEN_TAIVUTUKSET[...])
        else:
            luokka, loppuvokaali, sointu = None, None, None
            if viimeinen in "aeiouyäö" and sana[-2:-1] in "aeiouyäö":
                if sana[-2:-1] == viimeinen:
                    luokka = 18
                    loppuvokaali = viimeinen
                elif viimeinen in "ouyö":
                    luokka = 3
                    loppuvokaali = viimeinen
                elif viimeinen in "ie":
                    luokka = 20
                    loppuvokaali = viimeinen

            if not luokka:
                if viimeinen in "ouyö":
                    luokka = 1
                    loppuvokaali = viimeinen
                elif viimeinen == "e":
                    luokka = 8
                elif viimeinen == "ä":
                    luokka = 10
                    sointu = "ä"
                elif viimeinen == "a":
                    if _tavuja(sana) > 2:
                        luokka = 12
                    elif re.match("^[^aeiouyäö][ouyö]", sana):
                        luokka = 10
                    else:
                        luokka = 9
                    sointu = "a"
                else:  # i ja konsonantit
                    luokka = 6 if _tavuja(sana) > 2 else 5

        try:
            return Nimisana(sana=sana, luokka=luokka, aste=None, loppuvokaali=loppuvokaali, sointu=sointu, lyhenne=lyhenne, vain_yksikkö=vain_yksikkö)
        except ValueError:
            if lyhenne:
                raise
            return Nimisana.varataivutus(sana, sointu=sointu, lyhenne=True, vain_yksikkö=vain_yksikkö)


Nomini = Nimisana


__all__ = ["Nimisana", "Nomini", "Luku", "Sija", "Omistusliite"]
