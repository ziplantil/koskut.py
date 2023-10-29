

VOKAALIT = ["a", "e", "i", "o", "u", "y", "ä", "ö"]


DIFTONGIT = [
    "aa", "ee", "ii", "oo", "uu", "yy", "ää", "öö",
    "ai", "ei",       "oi", "ui", "yi", "äi", "öi",
    "au", "eu", "iu", "ou", "äy", "ey", "iy", "öy",
    "ie", "uo", "yö"
]


DIFTONGISOI = {"ee": "ie", "oo": "uo", "öö": "yö"}


def diftongisoi(pääte: str):
    return DIFTONGISOI.get(pääte[:2], pääte[:2]) + pääte[2:]


__all__ = ["VOKAALIT", "DIFTONGIT", "diftongisoi"]
