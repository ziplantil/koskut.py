
from __future__ import annotations

from typing import ClassVar
from dataclasses import dataclass


_astevaihtelut_vahva_heikko: dict[tuple[str, str], Astevaihtelu]


@dataclass
class Astevaihtelu():
    """Esittää astevaihtelua, jolla on vahva ja heikko aste."""

    vahva: str
    heikko: str
    kotus: str | None = None

    @staticmethod
    def hae(vahva: str, heikko: str):
        if astevaihtelu := _astevaihtelut_vahva_heikko.get((vahva, heikko), None):
            return astevaihtelu
        return Astevaihtelu((vahva, heikko))

    @staticmethod
    def hae_vahvalla(vahva: str):
        for (v, h), av in _astevaihtelut_vahva_heikko.items():
            if v == vahva:
                return av
        return None

    @staticmethod
    def hae_heikolla(heikko: str):
        for (v, h), av in _astevaihtelut_vahva_heikko.items():
            if h == heikko:
                return av
        return None

    KOTUS_A: ClassVar[Astevaihtelu]
    KOTUS_B: ClassVar[Astevaihtelu]
    KOTUS_C: ClassVar[Astevaihtelu]
    KOTUS_D: ClassVar[Astevaihtelu]
    KOTUS_E: ClassVar[Astevaihtelu]
    KOTUS_F: ClassVar[Astevaihtelu]
    KOTUS_G: ClassVar[Astevaihtelu]
    KOTUS_H: ClassVar[Astevaihtelu]
    KOTUS_I: ClassVar[Astevaihtelu]
    KOTUS_J: ClassVar[Astevaihtelu]
    KOTUS_K: ClassVar[Astevaihtelu]
    KOTUS_L: ClassVar[Astevaihtelu]
    KOTUS_M: ClassVar[Astevaihtelu]

    KK_K: ClassVar[Astevaihtelu]
    PP_P: ClassVar[Astevaihtelu]
    TT_T: ClassVar[Astevaihtelu]
    K_0: ClassVar[Astevaihtelu]
    P_V: ClassVar[Astevaihtelu]
    T_D: ClassVar[Astevaihtelu]
    MK_N: ClassVar[Astevaihtelu]
    MP_M: ClassVar[Astevaihtelu]
    LT_L: ClassVar[Astevaihtelu]
    NT_N: ClassVar[Astevaihtelu]
    RT_R: ClassVar[Astevaihtelu]
    K_J: ClassVar[Astevaihtelu]
    K_V: ClassVar[Astevaihtelu]
    GG_G: ClassVar[Astevaihtelu]
    BB_B: ClassVar[Astevaihtelu]
    DD_D: ClassVar[Astevaihtelu]


_astevaihtelut = [
    Astevaihtelu("kk", "k", "A"),
    Astevaihtelu("pp", "p", "B"),
    Astevaihtelu("tt", "t", "C"),
    Astevaihtelu("k", "", "D"),
    Astevaihtelu("p", "v", "E"),
    Astevaihtelu("t", "d", "F"),
    Astevaihtelu("nk", "ng", "G"),
    Astevaihtelu("mp", "mm", "H"),
    Astevaihtelu("lt", "ll", "I"),
    Astevaihtelu("nt", "nn", "J"),
    Astevaihtelu("rt", "rr", "K"),
    Astevaihtelu("k", "j", "L"),
    Astevaihtelu("k", "v", "M"),
    Astevaihtelu("gg", "g"),
    Astevaihtelu("bb", "b"),
    Astevaihtelu("dd", "d"),
    Astevaihtelu("t", ""),
]

_astevaihtelut_vahva_heikko = {}


# lisää Astevaihteluun kaiken olennaisen, esim. KOTUS_A, KK_K
for astevaihtelu in _astevaihtelut:
    if astevaihtelu.kotus:
        setattr(Astevaihtelu, f"KOTUS_{astevaihtelu.kotus.upper()}", astevaihtelu)
    _astevaihtelut_vahva_heikko[(astevaihtelu.vahva, astevaihtelu.heikko)] = astevaihtelu
    setattr(Astevaihtelu, f"{astevaihtelu.vahva.upper() or '0'}_{astevaihtelu.heikko.upper() or '0'}", astevaihtelu)


__all__ = ["Astevaihtelu"]
