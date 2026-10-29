"""Centrale configuratie: constanten, thematische regexes, kleurenpaletten en PipelineConfig."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Auteurs & Anonimisering
# ---------------------------------------------------------------------------
AUTHOR_MAPPING: dict[str, str] = {
    "Jeffrey Halters": "Student",
    "Rick": "Partner",
}

AUTHOR_DISPLAY: dict[str, str] = {
    "Student": "Jeffrey (Student)",
    "Partner": "Rick (Partner)",
}

# ---------------------------------------------------------------------------
# Event- en Tijdconstanten
# ---------------------------------------------------------------------------
THAILAND_START: str = "2025-09-21"
THAILAND_END: str = "2025-10-06"
DAY_PARTS_ORDER: tuple[str, ...] = ("Nacht", "Ochtend", "Middag", "Avond")
ACTIVE_DAY_PARTS: tuple[str, ...] = ("Avond", "Middag", "Ochtend")
MAX_RESPONSE_MINUTES: float = 480.0
PIECEWISE_KNOT_WORDS: float = 10.5

# ---------------------------------------------------------------------------
# Basis Regex-patronen (Media, URL, Systeemberichten)
# ---------------------------------------------------------------------------
URL_PATTERN: str = r"https?://\S+|www\.\S+"
DELETED_PATTERN: str = r"Je hebt dit bericht verwijderd|Dit bericht is verwijderd"
MEDIA_PATTERN: str = (
    r"<bijgevoegd:|afbeelding weggelaten|video weggelaten|"
    r"audio weggelaten|sticker weggelaten|gif weggelaten|"
    r"document weggelaten"
)
ONLY_MEDIA_PATTERN: str = (
    r"^\s*(?:<bijgevoegd:[^>]+>|"
    r"(?:afbeelding|video|audio|sticker|gif|document) weggelaten)\s*$"
)
CLEAN_TEXT_PATTERN: str = (
    r"<bijgevoegd:[^>]+>|https?://\S+|www\.\S+|"
    r"(?:afbeelding|video|audio|sticker|gif|document) weggelaten"
)

# ---------------------------------------------------------------------------
# De 16 Specifieke Regex-Features (onderverdeeld in 4 Leefdomeinen)
# ---------------------------------------------------------------------------
THEMATIC_REGEXES_16: dict[str, str] = {
    # Domein 1: Huishouden en Voeding (4 sub-regexes)
    "rx_koken_eten": r"\b(?:eten|gekookt|koken|recept|oven|lunch|ontbijt|avondeten|pizza|pasta|soep|salade)\b",
    "rx_boodschappen": r"\b(?:boodschappen|supermarkt|appie|ah|jumbo|lidl|halen|meenemen|fles|brood|kaas|melk)\b",
    "rx_schoonmaak_was": r"\b(?:wassen|wasje|vaatwasser|schoonmaken|stofzuigen|opruimen|prullenbak|containers?)\b",
    "rx_pakket_klus": r"\b(?:pakket(?:je)?|postnl|dhl|bezorgd|tuin|planten|klussen|verf|ikea)\b",
    # Domein 2: Werk en Mobiliteit (4 sub-regexes)
    "rx_werk_kantoor": r"\b(?:werk|werken|kantoor|collega(?:'s)?|dienst|rooster|vrij|vakantie)\b",
    "rx_overleg_studie": r"\b(?:meeting|vergadering|overleg|teams|mail(?:tje)?|school|studie|opdracht|les)\b",
    "rx_auto_verkeer": r"\b(?:auto|rijden|onderweg|file|parkeren|tanken|garage|vertrek|aankomst)\b",
    "rx_ov_reizen": r"\b(?:trein|station|bus|metro|ov|fiets(?:en)?|vertraging|spoor)\b",
    # Domein 3: Huisdieren (4 sub-regexes)
    "rx_hond_uitlaten": r"\b(?:hond(?:je|en)?|wandelen|uitlaten|rondje|bos|park|riem|losloop)\b",
    "rx_kat_Gedrag": r"\b(?:kat(?:je|ten)?|poes|miauwen|krabpaal|kattenbak|spinnen|knuffelen)\b",
    "rx_dier_voeding": r"\b(?:brokken|brokjes|voer(?:en)?|snoepjes|kluif|waterbak|natvoer)\b",
    "rx_dierenarts": r"\b(?:dierenarts|inenting|vaccinatie|vlooien|teek|poot(?:je)?|mand(?:je)?)\b",
    # Domein 4: Zorg & Familie (4 sub-regexes)
    "rx_familie_bezoek": r"\b(?:mama|papa|moeder|vader|ouders|opa|oma|zus|broer|familie|visite|bezoek)\b",
    "rx_gezondheid": r"\b(?:ziek|pijn|hoofdpijn|koorts|verkouden|moe|slapen|wakker|rusten)\b",
    "rx_medisch_zorg": r"\b(?:dokter|huisarts|apotheek|ziekenhuis|tandarts|fysio|medicijnen|paracetamol)\b",
    "rx_sociaal_feest": r"\b(?:verjaardag|cadeau|feest(?:je)?|borrel|uitje|gefeliciteerd|weekendje)\b",
}

# Geaggregeerde domein-regexes voor sessie-classificatie (Exact conform Les 6 / Figuur 5)
THEME_DOMAIN_PATTERNS: dict[str, str] = {
    "Huishouden en Voeding": (
        r"\b(eten|eet|koken|boodschappen|jumbo|appie|albert heijn|lidl|brood|"
        r"avondeten|lunch|lunchen|supermarkt|gegeten|pasta|pizza|koffie|"
        r"restaurant|bestellen|vega)\b"
    ),
    "Werk en Mobiliteit": (
        r"\b(onderweg|auto|rijden|file|trein|station|vertrokken|aankomen|"
        r"hoe laat|ben thuis|werk|werken|werkt|kantoor|meeting|overleg|han|"
        r"laptop|avans|moerdijk|rabobank|saskia|marit|emese|patricia|nakijken|"
        r"les|bus|collega|mail|mailen)\b"
    ),
    "Huisdieren": (
        r"\b(nusa|indy|hond|honden|hondje|hondjes|uitlaten|uitgelaten|"
        r"gewandeld|wandelen|brokjes|voer|dierenarts)\b"
    ),
    "Zorg & Familie": (
        r"\b(moeder|mam|mama|pap|papa|pappa|vader|ouders|schoonouders|oma|"
        r"heeze|familie|verjaardag|bezoek|op bezoek|carina|sterq|buurstede|"
        r"levensvreugde|zorg|zorgen|wmo|ziekenhuis|huisarts|medicijn|arts|opname)\b"
    ),
}

THEME_ORDER: tuple[str, ...] = (
    "Huishouden en Voeding",
    "Werk en Mobiliteit",
    "Huisdieren",
    "Zorg & Familie",
    "Overig",
)

# ---------------------------------------------------------------------------
# Visuele Stijl & Kleurenpalet (Jeffrey DAV Huisstijl)
# ---------------------------------------------------------------------------
COLOR_HIGHLIGHT: str = "#1F4E78"  # Diep marineblauw (primaire focus / Rick / Thailand)
COLOR_ACCENT_TEAL: str = "#2B5C8F"  # Secundair blauw
COLOR_STUDENT: str = "#D95F02"  # Warm oranje/roestbruin (Jeffrey / Student / Knikpunt)
COLOR_BASE: str = "#BDC3C7"  # Rustig grijs voor context / nulmodel
COLOR_BASE_DARK: str = "#6C7A89"  # Donkergrijs voor referentielijnen
COLOR_TEXT_MAIN: str = "#2C3E50"  # Antraciet voor titels en hoofdtekst
COLOR_TEXT_MUTED: str = "#595959"  # Muted grijs voor subtitels en voetnoten
COLOR_GRID: str = "#EAECEE"  # Subtiele gridlijnen
COLOR_REF_LINE: str = "#7F8C8D"  # Gestippelde referentielijnen
COLOR_CALLOUT_BG: str = "#F8F9F9"  # Achtergrond van callout-boxen
COLOR_CALLOUT_EDGE: str = "#D0D3D4"  # Rand van callout-boxen

THEME_COLORS: dict[str, str] = {
    "Huishouden en Voeding": "#1F4E78",  # Marineblauw
    "Werk en Mobiliteit": "#D95F02",  # Warm oranje
    "Huisdieren": "#2E8B57",  # Zeegroen
    "Zorg & Familie": "#8E44AD",  # Dieppaars
    "Overig": "#BDC3C7",  # Lichtgrijs
}


@dataclass(frozen=True)
class PipelineConfig:
    """Immutable configuratie voor de volledige wa-analyzer pipeline."""

    raw_chat_path: Path
    processed_chat_path: Path
    processed_sessions_path: Path
    img_dir: Path
    thailand_start: str = THAILAND_START
    thailand_end: str = THAILAND_END
    max_response_minutes: float = MAX_RESPONSE_MINUTES
    piecewise_knot_words: float = PIECEWISE_KNOT_WORDS
    min_session_words: int = 6
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    random_seed: int = 42
    author_mapping: dict[str, str] = field(default_factory=lambda: dict(AUTHOR_MAPPING))

    @classmethod
    def from_root(cls, root_dir: Path) -> PipelineConfig:
        """Construeer alle in- en uitvoerpaden relatief aan het opgegeven `root_dir`."""
        return cls(
            raw_chat_path=root_dir / "data" / "raw" / "_chat.txt",
            processed_chat_path=root_dir / "data" / "processed" / "chat.parq",
            processed_sessions_path=root_dir / "data" / "processed" / "sessions.parq",
            img_dir=root_dir / "img",
        )
