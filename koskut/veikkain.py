
from collections import OrderedDict
from enum import Enum
from typing import Iterable

from .astevaihtelu import Astevaihtelu
from .nimisana import Sija, Luku, Nimisana, _tavuja, _LUOKAT
from .vartalo import V, H, L
from .vokaali import VOKAALIT


class Nimilaji(Enum):
    YLEISSANA = 0
    VIERASSANA = 1
    PAIKANNIMI = 2
    VIERAS_PAIKANNIMI = 3
    ETUNIMI = 4
    VIERAS_ETUNIMI = 5
    SUKUNIMI = 6
    VIERAS_SUKUNIMI = 7


_KOTOPERÄISET = {
    Nimilaji.YLEISSANA,
    Nimilaji.PAIKANNIMI,
    Nimilaji.ETUNIMI,
    Nimilaji.SUKUNIMI
}


# taivutusluokat perusmuodon viimeisen kirjaimen perusteella
# Kotuksen numerointi, jokseenkin yleisyysjärjestys
_TAIVUTUSLUOKAT_LOPPUKIRJAIN = {
    "a": [12, 10, 9, 11, 13, 14, 15, 17, 18, 20, 21],
    "ä": [12, 10, 9, 11, 13, 14, 15, 17, 18, 20, 21],
    "o": [1, 2, 3, 4, 18, 19, 20, 21],
    "u": [1, 2, 3, 4, 18, 20, 21],
    "ö": [1, 2, 3, 4, 18, 19, 20, 21],
    "y": [1, 2, 3, 4, 18, 20, 21],
    "e": [3, 8, 20, 21, 48],
    "i": [5, 6, 7, 23, 24, 25, 26, 27, 28, 29, 30, 31, 16, 21],

    "l": [32, 49, 5, 6, 22],
    "n": [38, 33, 34, 35, 36, 37, 32, 49, 5, 6, 22],
    "r": [32, 49, 5, 6, 22],
    "s": [39, 40, 41, 42, 45, 5, 6, 22],
    "t": [43, 44, 46, 5, 6, 22],

    ...: [5, 6, 22]
}

# sanan loput eri taivutusluokille.
# ensimmäiseen listaan 'yleiset' tapaukset, jälkimmäiseen 'harvinaiset'
_TAIVUTUSLUOKAT_SANAN_LOPPU = {
    3: (["ao", "eo", "io", "iö", "ie", "oe"], []),
    15: (["ea", "eä", "oa"], []),
    17: (["aa", "oo", "uu"], ["ee", "yy"]),
    18: (["aa", "ee", "ii", "oo", "uu", "yy", "ää", "öö"], []),
    19: (["ie", "uo", "yö"], []),
    20: (["ee", "yy", "öö"], ["aa", "oo", "uu"]),
    23: ([], [f"{L}hi", f"{L}li", f"{L}ni"]),
    24: ([], [f"{L}hi", f"{L}li", f"{L}ni", f"{L}ri", f"{L}si"]),
    25: ([], [f"{L}mi"]),
    26: ([], [f"{L}li", f"{L}ni", f"{L}ri"]),
    27: ([], [f"{L}si"]),
    28: ([], [f"{L}lsi", f"{L}nsi", f"{L}rsi"]),
    29: ([], [f"{L}psi", f"{L}ksi"]),
    30: ([], [f"{L}tsi"]),
    31: ([], [f"{L}ksi"]),
    32: ([], [f"{L}l", f"{L}n", f"{L}r"]),
    33: ([], [f"{L}n"]),
    34: ([], [f"{L}ton", f"{L}tön"]),
    35: ([], [f"{L}n"]),
    36: ([], [f"{L}in"]),
    37: ([], [f"{L}en"]),
    38: ([f"{L}nen"], []),
    43: (["ut", "yt"], []),
    46: (["at"], []),
    47: (["ut", "yt"], []),
}

# vierassanoissa aina harvinaiset taivutusluokat
_TAIVUTUSLUOKAT_KOTOPERÄISET = {
    4, 11, 13, 14, 15, 16, 19,
    23, 24, 25, 26, 27, 28, 39, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 49
}

# yleiset päätteet nimilajista riippuen
_TAIVUTUSLUOKAT_PÄÄTTEET = {
    Nimilaji.YLEISSANA: [
        ("mpi", 16)
    ],

    Nimilaji.PAIKANNIMI: [
        ("la", 12),
        ("lä", 12),
    ],

    Nimilaji.SUKUNIMI: [
        ("nen", 38)
    ],
}

# montako tavua sanassa pitää olla että se voi kuulua tähän luokkaan
_TAIVUTUSLUOKAT_TAVUJA_VÄHINTÄÄN = {
    2: 3, 3: 2, 4: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 17: 2,
    33: 2, 34: 2, 35: 2, 36: 2, 37: 2, 38: 2, 39: 2, 40: 3,
    41: 3, 45: 3, 46: 3, 47: 3
}


_VEIKATTAVAT_MUODOT = [
    (Sija.OMANTO, Luku.YKSIKKÖ),
    (Sija.OSANTO, Luku.YKSIKKÖ),
    (Sija.SISÄOLENTO, Luku.YKSIKKÖ),
    (Sija.SISÄTULENTO, Luku.YKSIKKÖ),
    (Sija.OLENTO, Luku.YKSIKKÖ),
    (Sija.OMANTO, Luku.MONIKKO),
    (Sija.OSANTO, Luku.MONIKKO),
    (Sija.SISÄOLENTO, Luku.MONIKKO),
    (Sija.SISÄTULENTO, Luku.MONIKKO),
    (Sija.OLENTO, Luku.MONIKKO),
]


# luokat joille loppuvokaali tulee kysyä käyttäjiltä
_LUOKKA_LOPPUVOKAALIT = set()

# luokat joilla on astevaihtelu; vahva tai heikko aste perusmuodossa
_LUOKKA_ASTE_VAHVA = set()
_LUOKKA_ASTE_HEIKKO = set()


for _luokka, _vartalosto in _LUOKAT:
    if any(v.startswith(V) for v in _vartalosto.yks_n):
        _LUOKKA_ASTE_VAHVA.add(_luokka)
    elif any(v.startswith(H) for v in _vartalosto.yks_n):
        _LUOKKA_ASTE_HEIKKO.add(_luokka)
    elif any(L in v for v in _vartalosto.kaikki_päätteet()) and not all(L in v for v in _vartalosto.yks_n):
        _LUOKKA_LOPPUVOKAALIT.add(_luokka)


assert not len(_LUOKKA_LOPPUVOKAALIT & (_LUOKKA_ASTE_VAHVA | _LUOKKA_ASTE_HEIKKO))


_LOPPUVOKAALIT = [
    ("e", "a"),
    ("i", "a"),
    ("e", "ä"),
    ("i", "ä"),
    ("a", "a"),
    ("ä", "ä"),
    ("o", "a"),
    ("ö", "ä"),
    ("u", "a"),
    ("y", "ä"),
]

_VIERAAT_VOKAALIT = {"é": "e", "å": "o"}


def _tarkista_loppu(sana: str, pääte: str):
    if pääte.startswith(L):
        return len(sana) >= len(pääte) and sana.endswith(pääte[1:]) and sana[-len(pääte)] in VOKAALIT
    else:
        return sana.endswith(pääte)


def _mahdolliset_luokat(sana: str, laji: Nimilaji):
    # päättelee luokat ja järjestää todennäköisimmistä vähiten todennäköiseen
    loppukirjain = sana[-1]
    tavuja = _tavuja(sana)

    luokat = _TAIVUTUSLUOKAT_LOPPUKIRJAIN.get(loppukirjain, _TAIVUTUSLUOKAT_LOPPUKIRJAIN[...])
    hyvin_yleiset, yleiset, harvinaiset = set(), set(), set()

    for luokka in luokat[:]:
        if tavuja < _TAIVUTUSLUOKAT_TAVUJA_VÄHINTÄÄN.get(luokka, 0):
            if luokka in luokat:
                luokat.remove(luokka)
            continue

        if luokka in _TAIVUTUSLUOKAT_SANAN_LOPPU:
            päättyvä_y, päättyvä_h = _TAIVUTUSLUOKAT_SANAN_LOPPU[luokka]
            if any(_tarkista_loppu(sana, p) for p in päättyvä_y):
                yleiset.add(luokka)
            elif not any(_tarkista_loppu(sana, p) for p in päättyvä_h) and luokka in luokat:
                luokat.remove(luokka)

    for pääte, luokka in _TAIVUTUSLUOKAT_PÄÄTTEET.get(laji, []):
        if sana.endswith(pääte):
            hyvin_yleiset.add(luokka)

    if laji not in _KOTOPERÄISET:
        harvinaiset |= _TAIVUTUSLUOKAT_KOTOPERÄISET  
    
    järjestys = {}
    järjestys |= {l: -2 for l in hyvin_yleiset}
    järjestys |= {l: -1 for l in yleiset}
    järjestys |= {l: 2 for l in harvinaiset}

    return sorted(luokat, key=lambda l: järjestys.get(l, 0))


def _loppukonsonantit(vartalo: str):
    KONSONANTIT = "bcdfghjklmnpqrsštvwxzž"
    
    loppu = len(vartalo)
    alku = loppu
    while alku and vartalo[alku - 1] in KONSONANTIT:
        alku -= 1

    return vartalo[alku:loppu]


def _tunnista_asteet_vahvasta(kons: str, perusmuoto: str):
    asteet = []

    if kons.endswith("kk") and kons[:-2] in {"", "l", "n", "r"}:
        asteet.append(Astevaihtelu.hae_vahvalla("kk"))
    elif kons.endswith("pp") and kons[:-2] in {"", "m"}:
        asteet.append(Astevaihtelu.hae_vahvalla("pp"))
    elif kons.endswith("tt") and kons[:-2] in {"", "n"}:
        asteet.append(Astevaihtelu.hae_vahvalla("tt"))

    elif kons in {"nk", "mp", "lt", "nt", "rt", "gg", "bb", "dd"}:
        asteet.append(Astevaihtelu.hae_vahvalla(kons))

    elif kons.endswith("t") and kons[:-1] in {"", "h"}:
        asteet.append(Astevaihtelu.hae_vahvalla("t"))
    elif kons.endswith("p") and kons[:-1] in {"", "l", "r"}:
        asteet.append(Astevaihtelu.hae_vahvalla("p"))
    elif kons.endswith("k"):
        if kons[:-1] in {"", "l", "r"} and perusmuoto[-1:] in {"e", "i"}:
            asteet.append(Astevaihtelu.hae("k", "j"))
        elif perusmuoto[-3:] in {"uku", "yky"}:
            asteet.append(Astevaihtelu.hae("k", "v"))
        if kons[:-1] in {"", "h", "l", "r"}:
            asteet.append(Astevaihtelu.hae("k", ""))

    return asteet


def _tunnista_asteet_heikosta(kons: str, perusmuoto: str):
    asteet = []

    if kons.endswith("k") and kons[:-2] in {"", "l", "n", "r"}:
        asteet.append(Astevaihtelu.hae_vahvalla("kk"))
    elif kons.endswith("p") and kons[:-2] in {"", "m"}:
        asteet.append(Astevaihtelu.hae_vahvalla("pp"))
    elif kons.endswith("t") and kons[:-2] in {"", "n"}:
        asteet.append(Astevaihtelu.hae_vahvalla("tt"))

    elif kons in {"ng", "mm", "ll", "nn", "rr", "g", "b"}:
        asteet.append(Astevaihtelu.hae_heikolla(kons))

    elif kons == "d":
        asteet.append(Astevaihtelu.hae_vahvalla("t"))
        asteet.append(Astevaihtelu.hae_vahvalla("dd"))

    elif kons == "hd":
        asteet.append(Astevaihtelu.hae_vahvalla("t"))

    elif kons == "v":
        asteet.append(Astevaihtelu.hae_vahvalla("p"))
        v_kohta = perusmuoto.rfind("v")
        if (v_kohta > 0 and v_kohta < len(perusmuoto - 1)
                and perusmuoto[v_kohta - 1] == perusmuoto[v_kohta + 1]
                and perusmuoto[v_kohta - 1] in "uy"):
            asteet.append(Astevaihtelu.hae("k", "v"))

    elif kons in {"lj", "rj"}:
        asteet.append(Astevaihtelu.hae("k", "j"))

    elif kons == "":
        asteet.append(Astevaihtelu.hae("k", ""))

    return asteet


def _luokat_nimisanoiksi(sana: str, laji: Nimilaji, luokat: list[int], viimeinen_vokaali: str, vain_yksikkö: bool):
    # tekee taivutusluokista nimisanoja
    taivutukset = []

    for luokka in luokat:
        if luokka in {4, 14}:
            aste = Astevaihtelu.hae_vahvalla(sana[-3:-1])
        elif luokka == 16:
            aste = Astevaihtelu.MP_MM
        else:
            aste = None

        if luokka in _LUOKKA_LOPPUVOKAALIT:
            lv0, lv1 = ([(v, s) for v, s in _LOPPUVOKAALIT if v == viimeinen_vokaali],
                        [(v, s) for v, s in _LOPPUVOKAALIT if v != viimeinen_vokaali])
            for vokaali, sointu in lv0:
                taivutukset.append(Nimisana(
                    sana=sana, luokka=luokka, aste=None, loppuvokaali=vokaali,
                    sointu=sointu, vain_yksikkö=vain_yksikkö
                ))
            for vokaali, sointu in lv1:
                taivutukset.append(Nimisana(
                    sana=sana, luokka=luokka, aste=None, loppuvokaali=vokaali,
                    sointu=sointu, vain_yksikkö=vain_yksikkö
                ))
            continue

        if viimeinen_vokaali in "aouäöy":
            try:
                kokeet = [Nimisana(sana=sana, luokka=luokka, aste=None, sointu=viimeinen_vokaali)]
            except ValueError:
                continue
        else:
            try:
                kokeet = [Nimisana(sana=sana, luokka=luokka, aste=None, sointu="a"), Nimisana(sana=sana, luokka=luokka, aste=None, sointu="ä")]
            except ValueError:
                continue

        for koe in kokeet:
            if luokka == 38 and laji == Nimilaji.PAIKANNIMI:
                try:
                    taivutukset.append(Nimisana(sana=sana, luokka=luokka, aste=None, sointu=koe.sointu(), pakota_alisteiset_sijat_monikkoon=True))
                except ValueError:
                    pass

            if luokka in {24, 26} and laji in {Nimilaji.YLEISSANA, Nimilaji.PAIKANNIMI} and koe.sointu() == "ä":
                try:
                    taivutukset.append(Nimisana(sana=sana, luokka=luokka, aste=None, sointu=koe.sointu(), meri=True))
                except ValueError:
                    pass

            if luokka in _LUOKKA_ASTE_VAHVA or luokka in _LUOKKA_ASTE_HEIKKO:
                vartalo = koe._vartalo
                konsonantit = _loppukonsonantit(vartalo)
                if luokka in _LUOKKA_ASTE_HEIKKO:
                    asteet = _tunnista_asteet_heikosta(konsonantit, sana)
                else:
                    asteet = _tunnista_asteet_vahvasta(konsonantit, sana)

                for aste in asteet:
                    if (luokka in {9, 10} and aste.vahva() == "k" and aste.heikko() == ""
                                        and len(vartalo) >= 3
                                        and vartalo[-3] in VOKAALIT
                                        and vartalo.endswith("ik")):
                        try:
                            taivutukset.append(Nimisana(sana=sana, luokka=luokka, aste=aste, sointu=koe.sointu(), aika=True))
                        except ValueError:
                            pass

                    try:
                        taivutukset.append(Nimisana(sana=sana, luokka=luokka, aste=aste, sointu=koe.sointu()))
                    except ValueError:
                        pass

            taivutukset.append(koe)

    return taivutukset


def _päättele_luokat(sana: str, taivutuspohja: str, laji: Nimilaji, viimeinen_vokaali: str, vain_yksikkö: bool):
    assert len(sana) 
    luokat = _mahdolliset_luokat(sana, laji)
    return _luokat_nimisanoiksi(taivutuspohja, laji, luokat, viimeinen_vokaali, vain_yksikkö=vain_yksikkö)


class Taivutusveikkain():
    def __init__(self, sana: str, laji: Nimilaji, vain_yksikkö: bool = False, vain_yksikko: bool = False):
        """
        Taivutusveikkain, joka veikkaa nimisanan eli nominin taivutuksen valittujen muotojen perusteella.

        :param sana: sanan perusmuoto (nimennön eli nominatiivin yksikkö, tai monikko jos sanalla ei ole yksikköä)
        :param luokka: Kielitoimiston sanakirjan mukainen taivutusluokka (1-49)
        :param vain_yksikkö: onko sanalla vain yksikkömuodot
        :returns: taivutusveikkain; ensin katso vaihtoehdot, valitse oikea, ja toista kunnes tulos on valmis
        """
        loppukirjain = sana[-1:]
        if not loppukirjain or loppukirjain == loppukirjain.upper() or loppukirjain not in ("abcdefghijklmnopqrsštuvwxyzžåö" + "".join(_VIERAAT_VOKAALIT.keys())):
            self._tulos = Nimisana.varataivutus(sana, vain_yksikkö=vain_yksikkö)
            return

        sana_vierasvokaalit = sana
        for k, v in _VIERAAT_VOKAALIT.items():
            if k in sana_vierasvokaalit:
                sana_vierasvokaalit = sana_vierasvokaalit.replace(k, v)
        sanan_vokaalit = [v for v in sana_vierasvokaalit if v in VOKAALIT]
        if not sanan_vokaalit:
            self._tulos = Nimisana.varataivutus(sana, vain_yksikkö=vain_yksikkö)
            return

        vain_yksikkö = vain_yksikkö or vain_yksikko

        self._luokat = _päättele_luokat(sana_vierasvokaalit, sana, laji, sanan_vokaalit[-1], vain_yksikkö=vain_yksikkö)
        if not self._luokat:
            self._tulos = Nimisana.varataivutus(sana, vain_yksikkö=vain_yksikkö)
            return

        self._tulos = None
        self._sana = sana
        self._vain_yksikkö = vain_yksikkö
        self._muodot = [muoto for muoto in _VEIKATTAVAT_MUODOT if muoto[1] == Luku.YKSIKKÖ or not vain_yksikkö]
        self._tilastot = {}
        self._luokkia_viimeksi = len(self._luokat) + 1
        self._seuraava_muoto()


    def _seuraava_muoto(self):
        while True:
            if len(self._luokat) == 1:
                self._tulos = self._luokat[0]
                return
            if not self._muodot:
                assert self._luokat
                self._tulos = sorted(self._luokat, key=lambda luokka: self._tilastot.get(id(luokka), 0))[0]
                return

            self._muoto, self._muodot = self._muodot[0], self._muodot[1:]
            self._vaihtoehdot = OrderedDict()
            sija, luku = self._muoto

            # koosta uusi luettelo luokista -- jos muotoja ei ole, jätä luokka pois
            #print([x.kotus() for x in self._luokat])
            luokat = []
            for luokka in self._luokat:
                muodot = luokka.taivuta(sija, luku)
                for muoto in muodot:
                    self._vaihtoehdot.setdefault(muoto, []).append(luokka)
                if muodot:
                    luokat.append(luokka)
                self._tilastot[id(luokka)] = self._tilastot.get(id(luokka), 0) + len(muodot)

            self._luokat = luokat
            assert len(self._vaihtoehdot) > 0
            if len(self._vaihtoehdot) > 1:
                # älä kysy käyttäjältä mitään jos vastaaminen ei muuta tulosta
                if max(len(luokat) for luokat in self._vaihtoehdot.values()) < self._luokkia_viimeksi:
                    #print(self._luokkia_viimeksi, len(luokat))
                    self._luokkia_viimeksi = len(luokat)
                    return


    def vaihtoehdot(self) -> Iterable[tuple[Sija, Luku, list[str]]]:
        """
        Jos taivutusveikkain ei ole vielä keksinyt sanan taivutusta, antaa sijamuodon ja mahdolliset taivutusmuodot. Vastaa valitsemalla oikea vaihtoehto.

        :returns: niin pitkään kun taivutusveikkain miettii, palauttaa (yleidin avulla) sijan, luvun ja mahdolliset taivutusmuodot
        """
        while not self._tulos:
            sija, luku = self._muoto
            yield (sija, luku, list(self._vaihtoehdot.keys()))


    def valitse(self, muoto: str):
        """
        Valitsee vaihtoehdon, jolloin taivutusveikkain voi päätellä, mikä taivutusluokka voisi olla oikea.

        :param muoto: valittava vaihtoehto
        :raises ValueError: annettu muoto ei ole vaihtoehtona, tai vaihtoehtoja ei voi enää valita
        """
        """Vastaa aiempaan arveluun oikealla taivutusmuodolla."""
        if self._tulos:
            raise ValueError("veikkain on jo ajettu loppuun asti")

        if muoto not in self._vaihtoehdot:
            raise ValueError("annettu muoto ei ole vaihtoehtona")

        self._luokat = self._vaihtoehdot[muoto]
        self._seuraava_muoto()


    def tulos(self):
        """Palauttaa taivutettavan nimisanan. Jos arveluvaihe on vielä kesken, palauttaa None."""
        return self._tulos


__all__ = ["Taivutusveikkain", "Nimilaji"]

