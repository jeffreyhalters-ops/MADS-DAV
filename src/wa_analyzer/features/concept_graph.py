"""Concept-extractie en adjacency-matrix constructie voor Figuur 6 (Les 7)."""

from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

CONCEPTS_16: dict[str, dict[str, str]] = {
    "Voeding & Huishouden": {
        "thuis": r"\b(thuis|naar huis|ben thuis|thuiskomen|thuiskomt|thuiskwam|thuiswerken|doenradestraat|vijfhagen|ijpelaar|huis|tuin|\bbank\b|huishouden)\b",
        "eten & koken": r"\b(eten|eet|eette|gegeten|avondeten|lunch|lunchen|geluncht|ontbijt|ontbijten|koffie|bakkie|koffietje|cappuccino|bonen|brood|broodjes|broodje|bakker|croissant|beleg|soep|yoghurt|havermout|tosti|fruit|pasta|pastatje|spaghetti|spagetti|macaroni|makkaroni|pizza|pizza\'s|pizzas|lasagne|lasagna|risotto|tagliatelle|penne|koken|kookt|kookte|gekookt|kook|pan|pannen|gerechten|gerecht|ingredienten|ingrediënten|recept|recepten|bakken|gebakken|ovenschaal|wokken|snijden|braden|boodschappen|boodschap|boodschappenlijst|boodschappenlijstje|jumbo|appie|albert heijn|\bah\b|lidl|aldi|toko|markt|supermarkt|inkopen|thuisbezorgen|bezorgd|bestelling)\b",
        "horeca": r"\b(restaurant|restaurants|uiteten|bestellen|afhalen|thuisbezorgd|sabero|fazant|tthai|t-thai|terras|terrasje|terrassie|borrel|borrelen|borreltje|drankje|drankjes|biertje|biertjes|wijntje|wijntjes|wijnproeverij|proeverij|cocktail|cocktails|friet|frietje|frietjes|patat|snackbar|frituur|chinees|sushi|tapas|griek|italiaan|pizzeria|kroeg|cafe|café|cafes|cafés|lunchroom|bistro|brasserie|mcdonalds|\bmac\b|kfc|burger|hamburgers)\b",
        "sporten": r"\b(sporten|sport|gesport|sportte|sportschool|fitness|hardlopen|hardgelopen|rennen|loods|loods5|workout|gym)\b",
    },
    "Werk & Mobiliteit": {
        "Avans": r"\b(avans|den bosch|\bdb\b|lesgeven|\bles\b|lessen|icais|ilse|emese|marit|saskia|patricia|student|studenten|nakijken|toets|toetsen|collega|collega\'s|collegas|vergadering)\b",
        "Rabobank & Gemeente": r"\b(moerdijk|zevenbergen|rabobank|\brabo\b|kantoor|locatie|locaties|afdeling|gemeente)\b",
        "werken algemeen": r"\b(werken|werkt|werkte|gewerkt|overleg|meeting|gesprek|afspraak|werkdag|\bwerk\b|teams)\b",
        "vervoersmiddelen": r"\b(trein|treinen|spoor|vertraging|vertragingen|centraal|station|stations|perron|perrons|intercity|sprinter|\bns\b|treinkaartje|overstap|overstappen|auto|auto\'s|autos|autootje|wagen|file|files|vakantiefile|garage|opladen|tanken|benzine|bezine|peugeot|parkeergarage|stalling|parkeren|parkeer|parkeerkaart|autosleutel|autosleutels|rijden|rijd|rijdt|reed|gereden|onderweg|reistijd|filerijden|aangereden|vertrokken|\brij\b)\b",
    },
    "Huisdieren": {
        "Nusa & Indy": r"\b(hond|honden|hondje|hondjes|doggo|doggo\'s|doggos|beestje|beestjes|hondepoot|nusa|musa|noes|indy|indi)\b",
        "uitlaten": r"\b(uitlaten|uitgelaten|uitlaat|rondje|blokje|blokje om|wandelen|gewandeld|wandel|gepoept|poepen|poept|geplast|plassen|plast)\b",
        "eten honden": r"\b(worst|brok|brokken|brokje|brokjes|eten gegeven|hondeneten|hondenvoer|pensstaafje|kauwstaaf|kauwbot)\b",
        "dierenarts": r"\b(dierenarts|dierenartsen|dierarts|kliniek|dierenkliniek|dierenpension|puppytraining|inenting|inentingen|vaccin|vaccins|vaccinatie|vaccinaties|ontwormen|ontvlooien|pilletje|pilletjes|tandjes gewisseld)\b",
    },
    "Zorg & Familie": {
        "onze ouders": r"\b(moeder|mam|mama|mams|vader|pap|papa|paps|ouders|schoonouders|heeze|maarheeze|oosterhout|oosterh|den hout|oosteind|joury|milou|carnaval|carnavallen|carnavals)\b",
        "familie": r"\b(familie|oma|bep|carola|\bad\b|leo|mirjam|joost|luuk|luke|luc|suus|spelen|julie|sinterklaas|oppassen|neefje|nichtje|tante|oom|schoonfamilie)\b",
        "Feesten": r"\b(verjaardag|verjaardagen|verjaardagsfeest|verjaardagscadeau|jarig|jarige|gefeliciteerd|gefeliciteerdjes|feliciteren|felicitaties|feest|feestje|feestjes|party|bday|cadeau|cadeautje|cadeaus|cadeautjes|kerst|kerstmis|kerstdiner|kerstdagen|oud en nieuw|jaarwisseling|bruiloft|trouwen|huwelijk|jubileum)\b",
        "medisch & zorg": r"\b(dokter|dokters|huisarts|huisartsen|ziekenhuis|ziekenhuizen|amphia|apotheek|apotheken|bloedprikken|fysio|fysiotherapie|tandarts|tandartsen|mondhygienist|operatie|operaties|ingreep|revalidatie|behandeling|medicijnen|medicatie|pillen|paracetamol|ibuprofen|antibiotica|oogdruppels|zalf|pleister|verband|wond|pijn|hoofdpijn|buikpijn|keelpijn|rugpijn|ziek|zieker|ziekjes|griep|verkouden|koorts|corona|covid|slaap|slapen|geslapen|moe|uitrusten|bijkomen|rustig aan|beterschap|buurstede|wmo|wlz|zorg|dement|dementie|dagbesteding|geheugen|achteruit|indicatie|zorgkantoor)\b",
    },
}

THEME_COLORS_4: dict[str, str] = {
    "Voeding & Huishouden": "#B45309",  # Diep warm oranje/amber
    "Werk & Mobiliteit": "#1D4ED8",  # Zakelijk kobaltblauw
    "Huisdieren": "#475569",  # Rustig leisteengrijs
    "Zorg & Familie": "#047857",  # Warm bosgroen
}


def clean_whatsapp_text(text: object) -> str:
    """Verwijder URL's, mediateksten en stuurcodes conform Les 7."""
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r"[\u200e\u200f\u202a-\u202e]", "", text)
    cleaned = re.sub(r"https?://\S+|www\.\S+", "", cleaned)
    cleaned = re.sub(r"<bijgevoegd:.*?>|bestand bijgevoegd", "", cleaned)
    cleaned = re.sub(r"•\s*\d+\s*pagina.*", "", cleaned)
    cleaned = re.sub(
        r"gemiste spraakoproep.*|spraakoproep.*", "", cleaned, flags=re.IGNORECASE
    )
    return cleaned.lower()


def build_hierarchical_adjacency_matrix(
    df: pd.DataFrame,
    delta_seconds: float = 600.0,
    min_weight: int = 3,
) -> tuple[np.ndarray, list[str], dict[str, tuple[int, int]]]:
    """Bereken de 16x16 geordende concept-co-occurrencematrix conform Les 7.4.

    Gebruikt een sliding window op concept-occurrences met dubbel gewicht
    bij dialoog (auteurswisseling) en minimumdrempel voor incidentele ruis.

    Parameters
    ----------
    df : pd.DataFrame
        Chatberichten met 'timestamp', 'author', 'message' en optioneel 'has_only_media'.
    delta_seconds : float, default=600.0
        Tijdvenster in seconden (10 minuten).
    min_weight : int, default=3
        Drempelwaarde om incidentele ruis weg te filteren.

    Returns
    -------
    tuple[np.ndarray, list[str], dict[str, tuple[int, int]]]
        Tuple van (adj_clean, ordered_concepts, theme_slices).
    """
    valid = df[df["message"].notna() & ~df.get("has_only_media", False)].copy()
    valid["timestamp"] = pd.to_datetime(valid["timestamp"])
    valid = valid.sort_values("timestamp").reset_index(drop=True)
    valid["clean_msg"] = valid["message"].apply(clean_whatsapp_text)

    ordered_concepts: list[str] = []
    concept_to_theme: dict[str, str] = {}
    theme_slices: dict[str, tuple[int, int]] = {}
    current_idx = 0

    for theme, subdict in CONCEPTS_16.items():
        start_idx = current_idx
        for c_name in subdict:
            ordered_concepts.append(c_name)
            concept_to_theme[c_name] = theme
            current_idx += 1
        theme_slices[theme] = (start_idx, current_idx)

    compiled_patterns = {
        c: re.compile(pat)
        for t_dict in CONCEPTS_16.values()
        for c, pat in t_dict.items()
    }

    records: list[dict[str, Any]] = []
    msgs = valid["clean_msg"].tolist()
    ts_list = valid["timestamp"].tolist()
    authors_list = valid["author"].tolist()

    for msg, ts_val, auth_val in zip(msgs, ts_list, authors_list, strict=False):
        if not msg:
            continue
        for c_name, rx in compiled_patterns.items():
            if rx.search(msg):
                records.append(
                    {
                        "timestamp": ts_val,
                        "author": auth_val,
                        "concept": c_name,
                    }
                )

    df_concepts = pd.DataFrame(records).sort_values("timestamp").reset_index(drop=True)
    n_c = len(ordered_concepts)
    c_to_i = {c: i for i, c in enumerate(ordered_concepts)}

    adj = np.zeros((n_c, n_c), dtype=int)
    window = pd.Timedelta(seconds=delta_seconds)
    left = 0
    n_rec = len(df_concepts)
    if n_rec == 0:
        return adj, ordered_concepts, theme_slices

    ts = df_concepts["timestamp"].values
    c_arr = df_concepts["concept"].values
    authors = df_concepts["author"].values

    for right in range(n_rec):
        current_ts = ts[right]
        current_c = c_arr[right]
        current_a = authors[right]
        w_start = current_ts - window
        while left < right and ts[left] < w_start:
            left += 1
        for i in range(left, right):
            other_c = c_arr[i]
            other_a = authors[i]
            if current_c != other_c:
                i1 = c_to_i[current_c]
                i2 = c_to_i[other_c]
                wgt = 2 if current_a != other_a else 1
                adj[i1, i2] += wgt
                adj[i2, i1] += wgt

    adj_clean = adj.copy()
    adj_clean[adj_clean < min_weight] = 0

    return adj_clean, ordered_concepts, theme_slices
