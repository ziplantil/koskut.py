
from enum import Enum, auto
from typing import Callable, Literal

from .astevaihtelu import Astevaihtelu
from .nimisana import Nimisana, Sija, Omistusliite, OMISTUSLIITTEET
from .vartalo import L, V, H, K, D, P, HY, A, O, U, liestä_vartalo, onko_etinen, puno_vartalo, vartalon_punoja
from .vokaali import VOKAALIT, DIFTONGIT


class Alus(Enum):
    YKSIKKÖ_1 = 1
    YKSIKKO_1 = 1
    MINÄ = 1

    YKSIKKÖ_2 = 2
    YKSIKKO_2 = 2
    SINÄ = 2

    YKSIKKÖ_3 = 3
    YKSIKKO_3 = 3
    HÄN = 3

    MONIKKO_1 = 4
    ME = 4

    MONIKKO_2 = 5
    TE = 5

    MONIKKO_3 = 6
    HE = 6

    TEKIJÄTÖN = 7
    TEKIJATON = 7
    PASSIIVI = 7

    YKSIKKÖ_2_KOHTELIAS = 8
    YKSIKKO_2_KOHTELIAS = 8
    TEITITTELY = 8


class Aikamuoto(Enum):
    KESTÄMÄ = 0
    PREESENS = 0

    KERTOMA = 1
    IMPERFEKTI = 1

    PÄÄTTYMÄ = 2
    PERFEKTI = 2

    ENTISPÄÄTTYMÄ = 3
    PLUSKVAMPERFEKTI = 3


class Tapaluokka(Enum):
    TOSITAPA = 0
    INDIKATIIVI = 0

    EHTOTAPA = 1
    KONDITIONAALI = 1

    KÄSKYTAPA = 2
    IMPERATIIVI = 2

    MAHTOTAPA = 3
    POTENTIAALI = 3


class Nimitapa(Enum):
    A = 0
    AKSE = 1
    ESSA = 2
    TAESSA = 3
    EN = 4
    MASSA = 5
    MASTA = 6
    MAAN = 7
    MALLA = 8
    MATTA = 9
    MAN = 10
    TAMAN = 11
    MINEN = 12
    MAISILLA = 13


class Laatutapa(Enum):
    VA = 0
    TAVA = 1
    NUT = 2
    TTU = 3
    MA = 4
    MATON = 5


Subjekti = Alus
Modus = Tapaluokka
Infinitiivi = Nimitapa
Partisiippi = Laatutapa


def _vartalo_parametri_luetteloksi(arvo: str | list[str]) -> list[str]:
    if not isinstance(arvo, list):
        return [arvo]
    return arvo


class _Vartalosto():
    def __init__(self,
                 n_a: str | list[str],      # A-nimitavan vartalo
                 n_e: str | list[str],      # E-nimitavan vartalo
                 k_v: str | list[str],      # vahva kertomavartalo
                 k_h: str | list[str],      # heikko kertomavartalo
                 k_t: str | list[str],      # tekijätön kertomavartalo
                 s_v: str | list[str],      # vahva kestämävartalo
                 s_h: str | list[str],      # heikko kestämävartalo
                 s_t: str | list[str],      # tekijätön kestämävartalo
                 t_e: str | list[str],      # ehtotavan vartalo
                 t_k: str | list[str],      # käskytavan vartalo
                 t_m: str | list[str],      # mahtotavan vartalo
                 ):
        self.n_a = _vartalo_parametri_luetteloksi(n_a)
        self.n_e = _vartalo_parametri_luetteloksi(n_e)
        self.k_v = _vartalo_parametri_luetteloksi(k_v)
        self.k_h = _vartalo_parametri_luetteloksi(k_h)
        self.k_t = _vartalo_parametri_luetteloksi(k_t)
        self.s_v = _vartalo_parametri_luetteloksi(s_v)
        self.s_h = _vartalo_parametri_luetteloksi(s_h)
        self.s_t = _vartalo_parametri_luetteloksi(s_t)
        self.t_e = _vartalo_parametri_luetteloksi(t_e)
        self.t_k = _vartalo_parametri_luetteloksi(t_k)
        self.t_m = _vartalo_parametri_luetteloksi(t_m)

    def periydy(self,
                n_a: str | list[str] | None = None,
                n_e: str | list[str] | None = None,
                k_v: str | list[str] | None = None,
                k_h: str | list[str] | None = None,
                k_t: str | list[str] | None = None,
                s_v: str | list[str] | None = None,
                s_h: str | list[str] | None = None,
                s_t: str | list[str] | None = None,
                t_e: str | list[str] | None = None,
                t_k: str | list[str] | None = None,
                t_m: str | list[str] | None = None):
        return _Vartalosto(
            n_a=n_a or self.n_a,
            n_e=n_e or self.n_e,
            k_v=k_v or self.k_v,
            k_h=k_h or self.k_h,
            k_t=k_t or self.k_t,
            s_v=s_v or self.s_v,
            s_h=s_h or self.s_h,
            s_t=s_t or self.s_t,
            t_e=t_e or self.t_e,
            t_k=t_k or self.t_k,
            t_m=t_m or self.t_m,
        )

    def kaikki_päätteet(self):
        return [
            *self.n_a,
            *self.n_e,
            *self.k_v,
            *self.k_h,
            *self.k_t,
            *self.s_v,
            *self.s_h,
            *self.s_t,
            *self.t_e,
            *self.t_k,
            *self.t_m,
        ]


KONSONANTIT = {"h", "j", "k", "l", "m", "n", "r", "p", "s", "t", "v"}

KIELTOVERBI = {
    Alus.YKSIKKÖ_1: "en",
    Alus.YKSIKKÖ_2: "et",
    Alus.YKSIKKÖ_3: "ei",
    Alus.MONIKKO_1: "emme",
    Alus.MONIKKO_2: "ette",
    Alus.MONIKKO_3: "eivät",
    Alus.TEKIJÄTÖN: "ei",
}

KÄSKY_KIELTOVERBI = {
    Alus.YKSIKKÖ_2: "älä",
    Alus.YKSIKKÖ_3: "älköön",
    Alus.MONIKKO_1: "älkäämme",
    Alus.MONIKKO_2: "älkää",
    Alus.MONIKKO_3: "älkööt",
    Alus.TEKIJÄTÖN: "älköön",
}


OLLA_MUODOT = {
    (Alus.YKSIKKÖ_1, Aikamuoto.KESTÄMÄ, False):    "olen",
    (Alus.YKSIKKÖ_2, Aikamuoto.KESTÄMÄ, False):    "olet",
    (Alus.YKSIKKÖ_3, Aikamuoto.KESTÄMÄ, False):    "on",
    (Alus.MONIKKO_1, Aikamuoto.KESTÄMÄ, False):    "olemme",
    (Alus.MONIKKO_2, Aikamuoto.KESTÄMÄ, False):    "olette",
    (Alus.MONIKKO_3, Aikamuoto.KESTÄMÄ, False):    "ovat",
    (Alus.TEKIJÄTÖN, Aikamuoto.KESTÄMÄ, False):    "on",

    (Alus.YKSIKKÖ_1, Aikamuoto.KESTÄMÄ, True):     "ole",
    (Alus.YKSIKKÖ_2, Aikamuoto.KESTÄMÄ, True):     "ole",
    (Alus.YKSIKKÖ_3, Aikamuoto.KESTÄMÄ, True):     "ole",
    (Alus.MONIKKO_1, Aikamuoto.KESTÄMÄ, True):     "ole",
    (Alus.MONIKKO_2, Aikamuoto.KESTÄMÄ, True):     "ole",
    (Alus.MONIKKO_3, Aikamuoto.KESTÄMÄ, True):     "ole",
    (Alus.TEKIJÄTÖN, Aikamuoto.KESTÄMÄ, True):     "ole",

    (Alus.YKSIKKÖ_1, Aikamuoto.KERTOMA, False):    "olin",
    (Alus.YKSIKKÖ_2, Aikamuoto.KERTOMA, False):    "olit",
    (Alus.YKSIKKÖ_3, Aikamuoto.KERTOMA, False):    "oli",
    (Alus.MONIKKO_1, Aikamuoto.KERTOMA, False):    "olimme",
    (Alus.MONIKKO_2, Aikamuoto.KERTOMA, False):    "olitte",
    (Alus.MONIKKO_3, Aikamuoto.KERTOMA, False):    "olivat",
    (Alus.TEKIJÄTÖN, Aikamuoto.KERTOMA, False):    "oli",

    (Alus.YKSIKKÖ_1, Aikamuoto.KERTOMA, True):     "ollut",
    (Alus.YKSIKKÖ_2, Aikamuoto.KERTOMA, True):     "ollut",
    (Alus.YKSIKKÖ_3, Aikamuoto.KERTOMA, True):     "ollut",
    (Alus.MONIKKO_1, Aikamuoto.KERTOMA, True):     "olleet",
    (Alus.MONIKKO_2, Aikamuoto.KERTOMA, True):     "olleet",
    (Alus.MONIKKO_3, Aikamuoto.KERTOMA, True):     "olleet",
    (Alus.TEKIJÄTÖN, Aikamuoto.KERTOMA, True):     "ollut",

    (Alus.YKSIKKÖ_1, Tapaluokka.EHTOTAPA, False):  "olisin",
    (Alus.YKSIKKÖ_2, Tapaluokka.EHTOTAPA, False):  "olisit",
    (Alus.YKSIKKÖ_3, Tapaluokka.EHTOTAPA, False):  "olisi",
    (Alus.MONIKKO_1, Tapaluokka.EHTOTAPA, False):  "olisimme",
    (Alus.MONIKKO_2, Tapaluokka.EHTOTAPA, False):  "olisitte",
    (Alus.MONIKKO_3, Tapaluokka.EHTOTAPA, False):  "olisivat",
    (Alus.TEKIJÄTÖN, Tapaluokka.EHTOTAPA, False):  "olisi",

    (Alus.YKSIKKÖ_1, Tapaluokka.EHTOTAPA, True):   "olisi",
    (Alus.YKSIKKÖ_2, Tapaluokka.EHTOTAPA, True):   "olisi",
    (Alus.YKSIKKÖ_3, Tapaluokka.EHTOTAPA, True):   "olisi",
    (Alus.MONIKKO_1, Tapaluokka.EHTOTAPA, True):   "olisi",
    (Alus.MONIKKO_2, Tapaluokka.EHTOTAPA, True):   "olisi",
    (Alus.MONIKKO_3, Tapaluokka.EHTOTAPA, True):   "olisi",
    (Alus.TEKIJÄTÖN, Tapaluokka.EHTOTAPA, True):   "olisi",

    (Alus.YKSIKKÖ_2, Tapaluokka.KÄSKYTAPA, False): "ole",
    (Alus.YKSIKKÖ_3, Tapaluokka.KÄSKYTAPA, False): "olkoon",
    (Alus.MONIKKO_1, Tapaluokka.KÄSKYTAPA, False): "olkaamme",
    (Alus.MONIKKO_2, Tapaluokka.KÄSKYTAPA, False): "olkaa",
    (Alus.MONIKKO_3, Tapaluokka.KÄSKYTAPA, False): "olkoot",
    (Alus.TEKIJÄTÖN, Tapaluokka.KÄSKYTAPA, False): "olkoon",

    (Alus.YKSIKKÖ_2, Tapaluokka.KÄSKYTAPA, True):  "ole",
    (Alus.YKSIKKÖ_3, Tapaluokka.KÄSKYTAPA, True):  "olko",
    (Alus.MONIKKO_1, Tapaluokka.KÄSKYTAPA, True):  "olko",
    (Alus.MONIKKO_2, Tapaluokka.KÄSKYTAPA, True):  "olko",
    (Alus.MONIKKO_3, Tapaluokka.KÄSKYTAPA, True):  "olko",
    (Alus.TEKIJÄTÖN, Tapaluokka.KÄSKYTAPA, True):  "olko",

    (Alus.YKSIKKÖ_1, Tapaluokka.MAHTOTAPA, False): "lienen",
    (Alus.YKSIKKÖ_2, Tapaluokka.MAHTOTAPA, False): "lienet",
    (Alus.YKSIKKÖ_3, Tapaluokka.MAHTOTAPA, False): "lienee",
    (Alus.MONIKKO_1, Tapaluokka.MAHTOTAPA, False): "lienemme",
    (Alus.MONIKKO_2, Tapaluokka.MAHTOTAPA, False): "lienette",
    (Alus.MONIKKO_3, Tapaluokka.MAHTOTAPA, False): "lienevät",
    (Alus.TEKIJÄTÖN, Tapaluokka.MAHTOTAPA, False): "lienee",

    (Alus.YKSIKKÖ_1, Tapaluokka.MAHTOTAPA, True):  "liene",
    (Alus.YKSIKKÖ_2, Tapaluokka.MAHTOTAPA, True):  "liene",
    (Alus.YKSIKKÖ_3, Tapaluokka.MAHTOTAPA, True):  "liene",
    (Alus.MONIKKO_1, Tapaluokka.MAHTOTAPA, True):  "liene",
    (Alus.MONIKKO_2, Tapaluokka.MAHTOTAPA, True):  "liene",
    (Alus.MONIKKO_3, Tapaluokka.MAHTOTAPA, True):  "liene",
    (Alus.TEKIJÄTÖN, Tapaluokka.MAHTOTAPA, True):  "liene",
}


MUOTOPÄÄTTEET_ALUKSET = {
    (Alus.YKSIKKÖ_1, Aikamuoto.KESTÄMÄ, False):    ("k_h", "n"),
    (Alus.YKSIKKÖ_2, Aikamuoto.KESTÄMÄ, False):    ("k_h", "t"),
    (Alus.YKSIKKÖ_3, Aikamuoto.KESTÄMÄ, False):    ("k_v", f"{P}"),
    (Alus.MONIKKO_1, Aikamuoto.KESTÄMÄ, False):    ("k_h", "mme"),
    (Alus.MONIKKO_2, Aikamuoto.KESTÄMÄ, False):    ("k_h", "tte"),
    (Alus.MONIKKO_3, Aikamuoto.KESTÄMÄ, False):    ("k_v", f"v{A}t"),
    (Alus.TEKIJÄTÖN, Aikamuoto.KESTÄMÄ, False):    ("k_t", f"{A}{A}n"),

    (           ..., Aikamuoto.KESTÄMÄ, True):     ("k_h", ""),
    (Alus.TEKIJÄTÖN, Aikamuoto.KESTÄMÄ, True):     ("k_t", f"{A}"),

    (Alus.YKSIKKÖ_1, Aikamuoto.KERTOMA, False):    ("s_h", "n"),
    (Alus.YKSIKKÖ_2, Aikamuoto.KERTOMA, False):    ("s_h", "t"),
    (Alus.YKSIKKÖ_3, Aikamuoto.KERTOMA, False):    ("s_v", ""),
    (Alus.MONIKKO_1, Aikamuoto.KERTOMA, False):    ("s_h", "mme"),
    (Alus.MONIKKO_2, Aikamuoto.KERTOMA, False):    ("s_h", "tte"),
    (Alus.MONIKKO_3, Aikamuoto.KERTOMA, False):    ("s_v", f"v{A}t"),
    (Alus.TEKIJÄTÖN, Aikamuoto.KERTOMA, False):    ("s_t", "iin"),

    (Alus.YKSIKKÖ_1, Aikamuoto.KERTOMA, True):     ("t_m", f"{U}t"),
    (Alus.YKSIKKÖ_2, Aikamuoto.KERTOMA, True):     ("t_m", f"{U}t"),
    (Alus.YKSIKKÖ_3, Aikamuoto.KERTOMA, True):     ("t_m", f"{U}t"),
    (Alus.MONIKKO_1, Aikamuoto.KERTOMA, True):     ("t_m", f"eet"),
    (Alus.MONIKKO_2, Aikamuoto.KERTOMA, True):     ("t_m", f"eet"),
    (Alus.MONIKKO_3, Aikamuoto.KERTOMA, True):     ("t_m", f"eet"),
    (Alus.TEKIJÄTÖN, Aikamuoto.KERTOMA, True):     ("s_t", f"{U}"),

    (Alus.YKSIKKÖ_1, Tapaluokka.EHTOTAPA, False):  ("t_e", "sin"),
    (Alus.YKSIKKÖ_2, Tapaluokka.EHTOTAPA, False):  ("t_e", "sit"),
    (Alus.YKSIKKÖ_3, Tapaluokka.EHTOTAPA, False):  ("t_e", "si"),
    (Alus.MONIKKO_1, Tapaluokka.EHTOTAPA, False):  ("t_e", "simme"),
    (Alus.MONIKKO_2, Tapaluokka.EHTOTAPA, False):  ("t_e", "sitte"),
    (Alus.MONIKKO_3, Tapaluokka.EHTOTAPA, False):  ("t_e", f"siv{A}t"),
    (Alus.TEKIJÄTÖN, Tapaluokka.EHTOTAPA, False):  ("s_t", f"{A}isiin"),

    (           ..., Tapaluokka.EHTOTAPA, True):   ("t_e", "si"),
    (Alus.TEKIJÄTÖN, Tapaluokka.EHTOTAPA, True):   ("s_t", f"{A}isi"),

    (Alus.YKSIKKÖ_2, Tapaluokka.KÄSKYTAPA, False): ("k_h", ""),
    (Alus.YKSIKKÖ_3, Tapaluokka.KÄSKYTAPA, False): ("t_k", f"{O}{O}n"),
    (Alus.MONIKKO_1, Tapaluokka.KÄSKYTAPA, False): ("t_k", f"{A}{A}mme"),
    (Alus.MONIKKO_2, Tapaluokka.KÄSKYTAPA, False): ("t_k", f"{A}{A}"),
    (Alus.MONIKKO_3, Tapaluokka.KÄSKYTAPA, False): ("t_k", f"{O}{O}t"),
    (Alus.TEKIJÄTÖN, Tapaluokka.KÄSKYTAPA, False): ("s_t", f"{A}k{O}{O}n"),

    (Alus.YKSIKKÖ_2, Tapaluokka.KÄSKYTAPA, True):  ("k_h", ""),
    (           ..., Tapaluokka.KÄSKYTAPA, True):  ("t_k", f"{O}"),
    (Alus.TEKIJÄTÖN, Tapaluokka.KÄSKYTAPA, True):  ("s_t", f"{A}k{O}"),

    (Alus.YKSIKKÖ_1, Tapaluokka.MAHTOTAPA, False): ("t_m", "en"),
    (Alus.YKSIKKÖ_2, Tapaluokka.MAHTOTAPA, False): ("t_m", "et"),
    (Alus.YKSIKKÖ_3, Tapaluokka.MAHTOTAPA, False): ("t_m", "ee"),
    (Alus.MONIKKO_1, Tapaluokka.MAHTOTAPA, False): ("t_m", "emme"),
    (Alus.MONIKKO_2, Tapaluokka.MAHTOTAPA, False): ("t_m", "ette"),
    (Alus.MONIKKO_3, Tapaluokka.MAHTOTAPA, False): ("t_m", f"ev{A}t"),
    (Alus.TEKIJÄTÖN, Tapaluokka.MAHTOTAPA, False): ("s_t", f"{A}neen"),

    (           ..., Tapaluokka.MAHTOTAPA, True):  ("t_m", "e"),
    (Alus.TEKIJÄTÖN, Tapaluokka.MAHTOTAPA, True):  ("s_t", f"{A}ne"),
}

MUOTOPÄÄTTEET_ALUKSETTOMAT = {
    Nimitapa.A:                 ("n_a", f"{A}", False),
    Nimitapa.AKSE:              ("n_a", f"{A}kse", True),
    Nimitapa.ESSA:              ("n_e", f"ess{A}", None),
    Nimitapa.TAESSA:            ("s_t", f"{A}ess{A}", False),
    Nimitapa.EN:                ("n_e", "en", False),
    Nimitapa.MASSA:             ("k_v", f"m{A}ss{A}", False),
    Nimitapa.MASTA:             ("k_v", f"m{A}st{A}", False),
    Nimitapa.MAAN:              ("k_v", f"m{A}{A}n", False),
    Nimitapa.MALLA:             ("k_v", f"m{A}ll{A}", False),
    Nimitapa.MATTA:             ("k_v", f"m{A}tt{A}", False),
    Nimitapa.MAN:               ("k_v", f"m{A}n", False),
    Nimitapa.TAMAN:             ("s_t", f"{A}m{A}n", False),
    Nimitapa.MINEN:             ("k_v", "minen", False),
    Nimitapa.MAISILLA:          ("k_v", f"m{A}isill{A}", True),

    Laatutapa.VA:               ("k_v", f"v{A}", False),
    Laatutapa.TAVA:             ("s_t", f"{A}v{A}", False),
    Laatutapa.NUT:              ("t_m", f"{U}t", False),
    Laatutapa.TTU:              ("s_t", f"{U}", False),
    Laatutapa.MA:               ("k_v", f"m{A}", False),
    Laatutapa.MATON:            ("k_v", f"m{A}t{O}n", False),
}

TAIVUTUSJOHDOKSET = {
    Nimitapa.MINEN:             (38, None),
    Laatutapa.VA:               (10, None),
    Laatutapa.TAVA:             (10, None),
    Laatutapa.NUT:              (47, None),
    Laatutapa.TTU:              (1, ...),
    Laatutapa.MA:               (10, None),
    Laatutapa.MATON:            (34, "C"),
}

_LUOKAT = [
    (52, _Vartalosto(
            n_a=f"{V}{L}", n_e=f"{V}{L}",
            k_v=f"{V}{L}", k_h=f"{H}{HY}{L}", k_t=f"{H}{HY}{L}t",
            s_v=f"{V}{L}i", s_h=f"{H}{HY}{L}i", s_t=f"{H}{HY}{L}tt",
            t_e=f"{V}{L}i", t_k=f"{V}{L}k", t_m=f"{V}{L}n")),
    (53, _Vartalosto(
            n_a=f"{V}{A}", n_e=f"{V}{A}",
            k_v=f"{V}{A}", k_h=f"{H}{A}", k_t=f"{H}et",
            s_v=f"{V}i", s_h=f"{H}i", s_t=f"{H}ett",
            t_e=f"{V}{A}i", t_k=f"{V}{A}k", t_m=f"{V}{A}n")),
    (54, _Vartalosto(
            n_a=f"{V}{A}", n_e=f"{V}{A}",
            k_v=f"{V}{A}", k_h=f"{H}{A}", k_t=f"{H}et",
            s_v=f"{K}si", s_h=f"{K}si", s_t=f"{H}ett",
            t_e=f"{V}{A}i", t_k=f"{V}{A}k", t_m=f"{V}{A}n")),
    (55, _Vartalosto(
            n_a=f"{V}{A}", n_e=f"{V}{A}",
            k_v=f"{V}{A}", k_h=f"{H}{A}", k_t=f"{H}et",
            s_v=[f"{V}i", f"{K}si"], s_h=[f"{H}i", f"{K}si"], s_t=f"{H}ett",
            t_e=f"{V}{A}i", t_k=f"{V}{A}k", t_m=f"{V}{A}n")),
    (56, _Vartalosto(
            n_a=f"{V}{A}", n_e=f"{V}{A}",
            k_v=f"{V}{A}", k_h=f"{H}{A}", k_t=f"{H}et",
            s_v=f"{V}{O}i", s_h=f"{H}{O}i", s_t=f"{H}ett",
            t_e=f"{V}{A}i", t_k=f"{V}{A}k", t_m=f"{V}{A}n")),
    (57, _Vartalosto(
            n_a=f"{V}{A}", n_e=f"{V}{A}",
            k_v=f"{V}{A}", k_h=f"{H}{A}", k_t=f"{H}et",
            s_v=[f"{K}si", f"{V}{O}i"], s_h=[f"{K}si", f"{H}{O}i"], s_t=f"{H}ett",
            t_e=f"{V}{A}i", t_k=f"{V}{A}k", t_m=f"{V}{A}n")),
    (58, _Vartalosto(
            n_a=f"{V}e", n_e=f"{V}i",
            k_v=f"{V}e", k_h=f"{H}e", k_t=f"{H}et",
            s_v=f"{V}i", s_h=f"{H}i", s_t=f"{H}ett",
            t_e=f"{V}i", t_k=f"{V}ek", t_m=f"{V}en")),
    (59, _Vartalosto(
            n_a=f"{V}e", n_e=f"{V}i",
            k_v=f"{V}e", k_h=f"{H}e", k_t=f"{H}et",
            s_v=f"{K}si", s_h=f"{K}si", s_t=f"{H}ett",
            t_e=f"{V}i", t_k=f"{V}ek", t_m=f"{V}en")),
    (60, _Vartalosto(
            n_a=f"h{V}e", n_e=f"h{V}i",
            k_v=f"h{V}e", k_h=f"h{H}e", k_t=f"h{H}et",
            s_v=[f"h{V}i", "ksi"], s_h=[f"h{H}i", "ksi"], s_t=f"h{H}ett",
            t_e=f"h{V}i", t_k=f"h{V}ek", t_m=f"h{V}en")),
    (61, _Vartalosto(
            n_a=f"{V}i", n_e=f"{V}i",
            k_v=f"{V}i", k_h=f"{H}{HY}i", k_t=f"{H}{HY}it",
            s_v=f"{V}i", s_h=f"{H}{HY}i", s_t=f"{H}{HY}itt",
            t_e=f"{V}i", t_k=f"{V}ik", t_m=f"{V}in")),
    (62, _Vartalosto(
            n_a="d", n_e="d",
            k_v="", k_h="", k_t="d",
            s_v="", s_h="", s_t="t",
            t_e="", t_k="k", t_m="n")),
    (63, _Vartalosto(
            n_a=f"{L}d", n_e=f"{L}d",
            k_v=f"{L}", k_h=f"{L}", k_t=f"{L}d",
            s_v="i", s_h="i", s_t=f"{L}t",
            t_e="i", t_k=f"{L}k", t_m=f"{L}n")),
    (64, _Vartalosto(
            n_a=f"{D}d", n_e=f"{D}d",
            k_v=f"{D}", k_h=f"{D}", k_t=f"{D}d",
            s_v=f"{L}i", s_h=f"{L}i", s_t=f"{D}t",
            t_e=f"{L}i", t_k=f"{D}k", t_m=f"{D}n")),
    (65, _Vartalosto(
            n_a=f"{U}d", n_e=f"{U}d",
            k_v=f"{U}", k_h=f"{U}", k_t=f"{U}d",
            s_v="vi", s_h="vi", s_t=f"{U}t",
            t_e="vi", t_k=f"{U}k", t_m=f"{U}n")),
    (66, _Vartalosto(
            n_a=f"{H}{L}st", n_e=f"{H}{L}st",
            k_v=f"{V}{L}se", k_h=f"{V}{L}se", k_t=f"{H}{L}st",
            s_v=f"{V}{L}si", s_h=f"{V}{L}si", s_t=f"{H}{L}st",
            t_e=f"{V}{L}si", t_k=f"{H}{L}sk", t_m=f"{H}{L}ss")),
    (67, _Vartalosto(
            n_a=f"{K}{K}", n_e=f"{K}{K}",
            k_v=f"{K}e", k_h=f"{K}e", k_t=f"{K}{K}",
            s_v=f"{K}i", s_h=f"{K}i", s_t=f"{K}t",
            t_e=f"{K}i", t_k=f"{K}k", t_m=f"{K}{K}")),
    (68, _Vartalosto(
            n_a="d", n_e="d",
            k_v=["", "tse"], k_h=["", "tse"], k_t="d",
            s_v=["", "tsi"], s_h=["", "tsi"], s_t="t",
            t_e="", t_k="k", t_m="n")),
    (69, _Vartalosto(
            n_a="t", n_e="t",
            k_v="tse", k_h="tse", k_t="t",
            s_v="tsi", s_h="tsi", s_t="tt",
            t_e="tsi", t_k="tk", t_m="nn")),
    (70, _Vartalosto(
            n_a="st", n_e="st",
            k_v="kse", k_h="kse", k_t="st",
            s_v="ksi", s_h="ksi", s_t="st",
            t_e="ksi", t_k="sk", t_m="ss")),
    (71, _Vartalosto(
            n_a="hd", n_e="hd",
            k_v="ke", k_h="e", k_t="hd",
            s_v="ki", s_h="i", s_t="ht",
            t_e="ki", t_k="hk", t_m="hn")),
    (72, _Vartalosto(
            n_a=f"{H}{L}t", n_e=f"{H}{L}t",
            k_v=f"{V}{L}ne", k_h=f"{V}{L}ne", k_t=f"{H}{L}t",
            s_v=f"{V}{L}ni", s_h=f"{V}{L}ni", s_t=f"{H}{L}tt",
            t_e=f"{V}{L}ni", t_k=f"{H}{L}tk", t_m=f"{H}{L}nn")),
    (73, _Vartalosto(
            n_a=f"{H}{A}t", n_e=f"{H}{A}t",
            k_v=f"{V}{A}{A}", k_h=f"{V}{A}{A}", k_t=f"{H}{A}t",
            s_v=f"{V}{A}si", s_h=f"{V}{A}si", s_t=f"{H}{A}tt",
            t_e=f"{V}{A}i", t_k=f"{H}{A}tk", t_m=f"{H}{A}nn")),
    (74, _Vartalosto(
            n_a=f"{H}{L}t", n_e=f"{H}{L}t",
            k_v=f"{V}{L}{A}", k_h=f"{V}{L}{A}", k_t=f"{H}{L}t",
            s_v=f"{V}{L}si", s_h=f"{V}{L}si", s_t=f"{H}{L}tt",
            t_e=[f"{V}{L}{A}i", f"{V}{L}i"], t_k=f"{H}{L}tk", t_m=f"{H}{L}nn")),
    (75, _Vartalosto(
            n_a=f"{H}{L}t", n_e=f"{H}{L}t",
            k_v=f"{V}{L}{A}", k_h=f"{V}{L}{A}", k_t=f"{H}{L}t",
            s_v=f"{V}{L}si", s_h=f"{V}{L}si", s_t=f"{H}{L}tt",
            t_e=f"{V}{L}{A}i", t_k=f"{H}{L}tk", t_m=f"{H}{L}nn")),
    (76, _Vartalosto(
            n_a=f"{V}{A}", n_e=f"{V}{A}",
            k_v=f"{V}{A}", k_h=f"{H}{A}", k_t=f"{H}et",
            s_v=f"{K}si", s_h=f"{K}si", s_t=f"{H}ett",
            t_e=f"{V}{A}i", t_k=f"{V}{A}k", t_m=[f"nn", f"{V}{A}n"])),
]

_LUOKAT_NUMEROITTAIN = {numero: vartalosto for numero, vartalosto in _LUOKAT}


def _pidennys(vartalo: str) -> str:
    if vartalo and vartalo[-1] in VOKAALIT:
        if any(vartalo.endswith(d) for d in DIFTONGIT) and not any(vartalo[:-1].endswith(d) for d in DIFTONGIT):
            return vartalo
        vartalo += vartalo[-1]
    return vartalo 


def _liestä_teonsanan_vartalo(sana: str, vartalosto: _Vartalosto,
                              aste: Astevaihtelu | None) -> tuple[str, str | None, str | None]:
    päätteet = [x + f"{A}" for x in vartalosto.n_a]

    vartalo, vokaali, konsonantti = None, None, None
    for pääte in päätteet:
        try:
            vartalo, vokaali, konsonantti = liestä_vartalo(sana, pääte, aste)
        except ValueError:
            pass

    if vartalo is None:
        raise ValueError("sana ei vastaa kyseistä taivutustyyppiä")

    return vartalo, vokaali, konsonantti


def _muoto1(muodot: list[str]):
    if not len(muodot):
        raise ValueError("sanalla ei ole annettua muotoa")
    return muodot[0]


class Teonsana():
    def __init__(self, sana: str, luokka: int,
                 aste: Astevaihtelu | str | tuple[str, str] | None = None,
                 sointu: Literal["A", "a", "Ä", "ä"] | None = None):
        """
        Teonsana eli verbi, jota voi taivuttaa teonsanojen taivutuskaavojen mukaisesti.

        :param sana: sanan perusmuoto (A-nimitapa eli A-infinitiivi, eli 'sanakirjamuoto')
        :param luokka: Kielitoimiston sanakirjan mukainen taivutusluokka (52-76)
        :param aste: sanan astevaihtelu: joko Astevaihtelu-olio, monikko jossa on vahva ja heikko aste, Kielitoimiston sanakirjan astevaihtelutunnus (A-M) tai tyhjä, jos sanassa ei ole astevaihtelua
        :param sointu: sanan vokaalisointu, kannattaa aina määrittää itse
        :returns: taivutettava teonsana
        :raises ValueError: jos taivutusluokka tai astevaihtelu on kelpaamaton, tai jos sanan perusmuoto ei vaikuta sopivan taivutusluokkaan
        """

        try:
            _vartalosto = _LUOKAT_NUMEROITTAIN[luokka]
        except KeyError:
            raise ValueError(f"tuntematon taivutusluokka {luokka}")

        # astevaihtelut
        if isinstance(aste, str):
            if len(aste) != 1:
                raise ValueError(f"tuntematon astevaihtelutyyppi {aste}")
            try:
                aste = getattr(Astevaihtelu, "KOTUS_" + aste.upper())
            except AttributeError:
                raise ValueError(f"tuntematon astevaihtelutyyppi {aste}")
        elif isinstance(aste, tuple):
            aste = Astevaihtelu(aste)

        self._vartalo, self._vokaali, self._konsonantti = _liestä_teonsanan_vartalo(sana, _vartalosto, aste)
        self._luokka = luokka
        self._päätteet = _vartalosto
        self._aste = aste
        self._etinen = onko_etinen(sointu or sana)

        # taivutusluokkakohtaiset tarkistukset
        kelpaa = True
        if self._luokka in {54, 55, 57}:
            if not self._aste or not self._aste.vahva.endswith("t"):
                kelpaa = False
        elif self._luokka == 59:
            if not self._aste or len(self._aste.vahva) >= 2 and not self._aste.vahva.endswith("t"):
                kelpaa = False
        elif self._luokka in {60, 76}:
            if self._aste and self._aste.vahva != "t":
                kelpaa = False
        elif self._aste:
            if not any(H in pääte or V in pääte for pääte in self._päätteet.kaikki_päätteet()):
                kelpaa = False

        if not kelpaa:
            raise ValueError(f"astevaihtelu {aste} ei sovi yhteen taivutusluokan {luokka} kanssa")

        # loppukonsonantti monelle tyypeistä
        if self._aste and self._aste.vahva[-1] == "t" and not self._konsonantti:
            self._konsonantti = self._aste.heikko[:-1]

        # taivutusluokkakohtaiset poikkeukset
        heittomerkki = False

        # 52 (sanoa)
        if self._luokka == 52:
            if self._aste and self._aste.heikko == "" and self._vartalo.endswith(self._vokaali):
                heittomerkki = True

        # 61 (sallia)
        elif self._luokka == 61:
            if self._aste and self._aste.heikko == "" and self._vartalo.endswith("i"):
                heittomerkki = True

        if not any(L in pääte for pääte in self._päätteet.kaikki_päätteet()):
            self._vokaali = None
        if not any(K in pääte for pääte in self._päätteet.kaikki_päätteet()):
            self._konsonantti = None

        self._heittomerkki = heittomerkki
        self._punoja = vartalon_punoja(self._aste, self._etinen, self._vokaali, self._konsonantti, heittomerkki, heittomerkki)


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
        """Palauttaa taivutuksen koskut-C-kirjaston muodossa: vartalo ja kt_verbtaiv-tunnus."""
        
        if self._vokaali:
            vokaali = "iaoueäöy".find(self._vokaali)
        else:
            vokaali = 0

        if self._luokka in {52, 61}:
            heitto = int(self._heittomerkki)
        elif self._luokka == 67:
            heitto = {"l": 0, "n": 1, "r": 2}[self._konsonantti]
        else:
            heitto = 0

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
        else:
            aste = 0

        if self._luokka not in range(52, 78):
            raise ValueError("ei voida esittää C-Koskuen muodossa")

        luokka = self._luokka
        # C-Koskuen vaatimat astevaihtelut
        if luokka in {60, 76}:
            assert aste == 6
        elif luokka == 71:
            assert aste == 0
            aste = 4
        elif luokka in {54, 55, 57}:
            assert aste in {6, 9, 10, 11}
        elif luokka == 59:
            assert aste in {9, 10, 11}

        # C-Koskuen vaatimat loppuvokaalit
        if luokka in {61, 62}:
            vokaali = 0  # i
        elif luokka in {58, 59, 60, 68, 69, 70, 71}:
            vokaali = 4  # e
        elif luokka in {53, 54, 55, 56, 57, 73, 76, 77}:
            vokaali = 5 if self._etinen else 1  # Ä/A

        luokka -= 51
        tunnus = (((1 if self._etinen else 0) << 15)
               | (heitto << 13)
               | (luokka << 8)
               | (aste << 3) | vokaali)

        return self._vartalo, tunnus


    def taivuta_tekijällinen(self, alus: Alus,
                             aikamuoto: Aikamuoto,
                             tapaluokka: Tapaluokka,
                             kieltomuoto: bool = False):
        """
        Taivuttaa teonsanaa valitussa tekijällisessä eli aktiivimuodossa.
        Liittomuodoista palautetaan vain loppuosa, esim. kieltomuotoon ei kuulu sanan "ei" muotoa, vaan esim. "olla" => "ole" ("ei ole").
        Sama pätee myös aikamuotoihin, kuten "tehdä" => "tehnyt" ("on tehnyt").

        :param alus: alus/subjekti eli tekijä/persoona
        :param aikamuoto: aikamuoto
        :param tapaluokka: tapaluokka
        :param kieltomuoto: palautetaanko kieltomuoto
        :returns: luettelo taivutusmuodoista, jokseekseenkin yleisyysjärjestyksessä taivutusluokan sanoille
        :raises ValueError: tuntematon alus, aikamuoto tai tapaluokka
        """

        # vain tositavalla on nämä aikamuodot
        if (tapaluokka != Tapaluokka.TOSITAPA
                and (aikamuoto == Aikamuoto.KERTOMA or aikamuoto == Aikamuoto.ENTISPÄÄTTYMÄ)):
            return []

        if tapaluokka == Tapaluokka.KÄSKYTAPA and alus == Alus.YKSIKKÖ_1:
            return []

        # palauta nimitapa, koska nämä ovat liittomuotoja
        if (aikamuoto == Aikamuoto.PÄÄTTYMÄ
                or aikamuoto == Aikamuoto.ENTISPÄÄTTYMÄ):
            return self.taivuta_tekijällinen(alus, Aikamuoto.KERTOMA, Tapaluokka.TOSITAPA, True)

        teitittely = False
        if alus == Alus.TEITITTELY:
            alus = Alus.MONIKKO_2
            teitittely = True

        if kieltomuoto and (alus != Alus.TEKIJÄTÖN and
                            aikamuoto != Aikamuoto.KERTOMA and
                            (alus != Alus.YKSIKKÖ_2 or tapaluokka != Tapaluokka.KÄSKYTAPA)):
            alus_avain = ...
        else:
            alus_avain = alus

        if kieltomuoto and teitittely and alus_avain is not ...:
            alus_avain = Alus.YKSIKKÖ_3

        if tapaluokka == Tapaluokka.TOSITAPA:
            avain = (alus_avain, aikamuoto, kieltomuoto)
        else:
            avain = (alus_avain, tapaluokka, kieltomuoto)

        vartalo, lisäpääte = MUOTOPÄÄTTEET_ALUKSET[avain]
        päätteet = getattr(self._päätteet, vartalo)
        tulokset = [self._vartalo + puno_vartalo(pääte + lisäpääte, self._punoja) for pääte in päätteet]
        if lisäpääte.endswith(P):
            tulokset = [_pidennys(tulos[:-1]) for tulos in tulokset]
        return tulokset

    taivuta_tekijallinen = taivuta_tekijällinen
    taivuta_aktiivi = taivuta_tekijällinen


    def taivuta_nimitapa(self, nimitapa: Nimitapa, omistus: Omistusliite | None = None):
        """
        Taivuttaa teonsanaa valitussa nimitavassa eli infinitiivissä.

        :param nimitapa: nimitapa/infinitiivi
        :param omistus: omistusliite, jos muotoon sellainen kuuluu
        :returns: luettelo taivutusmuodoista, jokseekseenkin yleisyysjärjestyksessä taivutusluokan sanoille
        :raises ValueError: tuntematon nimitapa
        """

        vartalo, lisäpääte, omistettava = MUOTOPÄÄTTEET_ALUKSETTOMAT[nimitapa]
        if omistettava is False and omistus:
            return []
        elif omistettava is True and not omistus:
            return []

        päätteet = getattr(self._päätteet, vartalo)
        muodot = []

        if omistus:
            try:
                omistaja = OMISTUSLIITTEET[omistus]
            except AttributeError:
                raise ValueError(f"tuntematon omistusliite {omistus}")
        else:
            omistaja = ""

        for pääte in päätteet:
            if omistus == Omistusliite.NSA:
                muoto = self._vartalo + puno_vartalo(pääte + lisäpääte, self._punoja)
                muodot.append(muoto + muoto[-1] + "n")
            muodot.append(self._vartalo + puno_vartalo(pääte + lisäpääte + omistaja, self._punoja))

        return muodot

    taivuta_infinitiivi = taivuta_nimitapa


    def johda_nimitapa(self, nimitapa: Nimitapa):
        """
        Johtaa teonsanan nimitavasta (infinitiivistä) nimisanan (nominin).

        :param nimitapa: nimitapa/infinitiivi
        :returns: nimisanaolio, tai None jos annettua nimitapaa ei voi taivuttaa
        """

        vartalo, lisäpääte, omistettava = MUOTOPÄÄTTEET_ALUKSETTOMAT[nimitapa]
        if nimitapa not in TAIVUTUSJOHDOKSET:
            return None

        päätteet = getattr(self._päätteet, vartalo)
        perusmuoto = self._vartalo + puno_vartalo(päätteet[0] + lisäpääte, self._punoja) 
        luokka, aste = TAIVUTUSJOHDOKSET[nimitapa]
        assert aste is not ...
        return Nimisana(perusmuoto, luokka=luokka, aste=aste, sointu="ä" if self._etinen else "a")

    johda_infinitiivi = johda_nimitapa


    def johda_laatutapa(self, laatutapa: Laatutapa):
        """
        Johtaa teonsanan laatutavasta (partisiipista) nimisanan (nominin).

        :param laatutapa: laatutapa/partisiippi
        :returns: nimisanaolio, tai None jos annettua laatutapaa ei voi taivuttaa
        """

        vartalo, lisäpääte, omistettava = MUOTOPÄÄTTEET_ALUKSETTOMAT[laatutapa]
        if laatutapa not in TAIVUTUSJOHDOKSET:
            return None

        päätteet = getattr(self._päätteet, vartalo)
        perusmuoto = self._vartalo + puno_vartalo(päätteet[0] + lisäpääte, self._punoja) 
        luokka, aste = TAIVUTUSJOHDOKSET[laatutapa]

        if aste is ...: # tunnista
            käytävä = perusmuoto
            loppukonsonantit = ""
            while käytävä and käytävä[-1] in VOKAALIT:
                käytävä = käytävä[:-1]
            while käytävä and käytävä[-1] in KONSONANTIT:
                loppukonsonantit += käytävä[-1]
                käytävä = käytävä[:-1]
            loppukonsonantit = loppukonsonantit[:-3:-1]
            aste = Astevaihtelu.hae_vahvalla(loppukonsonantit)
            if not aste and len(loppukonsonantit) > 1 and loppukonsonantit[0] in {"h", "j", "l", "n", "r"}:
                aste = Astevaihtelu.hae_vahvalla(loppukonsonantit[-1])

        return Nimisana(perusmuoto, luokka=luokka, aste=aste, sointu="ä" if self._etinen else "a")

    johda_partisiippi = johda_laatutapa


    def taivuta_tekijällinen1(self, alus: Alus,
                              aikamuoto: Aikamuoto,
                              tapaluokka: Tapaluokka,
                              kieltomuoto: bool = False):
        """
        Taivuttaa teonsanaa valitussa tekijällisessä eli aktiivimuodossa, ja palauttaa vain yhden muodon.
        Liittomuodoista palautetaan vain loppuosa, esim. kieltomuotoon ei kuulu sanan "ei" muotoa, vaan esim. "olla" => "ole" ("ei ole").
        Sama pätee myös aikamuotoihin, kuten "tehdä" => "tehnyt" ("on tehnyt").

        :param alus: alus/subjekti eli tekijä/persoona
        :param aikamuoto: aikamuoto
        :param tapaluokka: tapaluokka
        :returns: taivutettu sanamuoto
        :raises ValueError: tuntematon alus, aikamuoto tai tapaluokka, tai jos sanalla ei ole pyydettyä muotoa
        """

        return _muoto1(self.taivuta_tekijällinen(alus, aikamuoto, tapaluokka, kieltomuoto))

    taivuta_tekijallinen1 = taivuta_tekijällinen1
    taivuta_aktiivi1 = taivuta_tekijällinen1


    def taivuta_nimitapa1(self, nimitapa: Nimitapa, omistus: Omistusliite | None = None):
        """
        Taivuttaa teonsanaa valitussa nimitavassa eli infinitiivissä, ja palauttaa vain yhden muodon.

        :param nimitapa: nimitapa/infinitiivi
        :param omistus: omistusliite, jos muotoon sellainen kuuluu
        :returns: taivutettu sanamuoto
        :raises ValueError: tuntematon nimitapa, tai jos sanalla ei ole pyydettyä muotoa
        """

        return _muoto1(self.taivuta_nimitapa(nimitapa, omistus))

    taivuta_infinitiivi1 = taivuta_nimitapa1


    @staticmethod
    def koskuesta(vartalo: str, tunnus: int):
        """
        Luo C-Koskuen vartalon ja tunnuksen pohjalta teonsanan.

        :param sana: sanan vartalo Koskuen muodossa
        :param tunnus: kt_verbtaiv-tunnus
        :returns: taivutettava teonsana
        """

        etinen = bool(tunnus >> 15)
        heitto = (tunnus >> 13) & 3
        luokka = (tunnus >> 8) & 63
        aste = (tunnus >> 3) & 31
        vokaali = tunnus & 7
        konsonantti = None

        luokka += 51

        if luokka not in range(52, 78):
            raise ValueError("annettu tunnus ei ole kelvollinen kt_verbtaiv-tunnus")

        if luokka == 67:
            konsonantti = "lnrl"[heitto]
            heitto = False
        elif luokka in {52, 61}:
            heitto = bool(heitto)
        else:
            heitto = False

        if luokka in {71}:
            aste = 0

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

        vartalosto = _LUOKAT_NUMEROITTAIN[luokka]
        punoja = vartalon_punoja(aste, etinen, vokaali, konsonantti, heitto, heitto)
        sana = vartalo + puno_vartalo(vartalosto.n_a[0] + A, punoja)

        return Teonsana(sana=sana, luokka=luokka, aste=aste,
                        sointu="ä" if etinen else "a")


    @staticmethod
    def liiton_alkuosa(alus: Alus, aikamuoto: Aikamuoto,
                       tapaluokka: Tapaluokka, kieltomuoto: bool = False):
        """
        Taivuttaa teonsanaliittomuodon alkusanat, esim. "ei", "ei ole", "olimme".

        :param alus: alus/subjekti eli tekijä/persoona
        :param aikamuoto: aikamuoto
        :param tapaluokka: tapaluokka
        :param kieltomuoto: palautetaanko kieltomuoto
        :returns: luettelo liittomuodon sanoista ennen varsinaista pääsanaa
        """
        sanat = []

        teitittely = False
        if alus == Alus.TEITITTELY:
            alus = Alus.MONIKKO_2
            teitittely = True

        if tapaluokka == Tapaluokka.KÄSKYTAPA and alus == Alus.YKSIKKÖ_1:
            return []

        if kieltomuoto:
            if tapaluokka == Tapaluokka.KÄSKYTAPA:
                sanat.append(KÄSKY_KIELTOVERBI[alus])
            else:
                sanat.append(KIELTOVERBI[alus])

        if aikamuoto == Aikamuoto.PÄÄTTYMÄ:
            aikamuoto = Aikamuoto.KESTÄMÄ
        elif aikamuoto == Aikamuoto.ENTISPÄÄTTYMÄ:
            aikamuoto = Aikamuoto.KERTOMA
        else:
            return sanat

        if aikamuoto == Aikamuoto.KERTOMA and tapaluokka != Tapaluokka.TOSITAPA:
            return []

        olla_alus = Alus.YKSIKKÖ_2 if teitittely and kieltomuoto else alus
        if tapaluokka == Tapaluokka.TOSITAPA:
            sanat.append(OLLA_MUODOT[(olla_alus, aikamuoto, kieltomuoto)])
        else:
            sanat.append(OLLA_MUODOT[(olla_alus, tapaluokka, kieltomuoto)])

        return sanat


Verbi = Teonsana


__all__ = ["Taivutusmuoto", "Verbi", "Alus", "Aikamuoto", "Tapaluokka", "Nimitapa", "Laatutapa",
           "Subjekti", "Modus", "Infinitiivi", "Partisiippi"]
