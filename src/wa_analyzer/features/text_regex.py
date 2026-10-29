"""Tekst- en regex-features: emoji-detectie, woordlengtes en de 16 thematische regexes."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from goad_toolkit.datatransforms import TransformBase

from wa_analyzer.config import (
    THEME_DOMAIN_PATTERNS,
    THEMATIC_REGEXES_16,
)


def count_clean_words(text: object) -> int:
    """Tel uitsluitend inhoudelijke alfanumerieke woorden (geen emoji's of leestekens)."""
    if not isinstance(text, str):
        return 0
    return len(re.findall(r"\b[a-zA-Z0-9_À-ÿ]+\b", text))


class EmojiOnly(TransformBase):
    """Voeg boolean kolom `only_emoji` toe voor berichten zonder alfanumerieke tekens."""

    def transform(
        self,
        data: pd.DataFrame,
        column: str = "message",
        feature: str = "only_emoji",
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        out[feature] = ~out[column].fillna("").str.contains(r"[a-zA-Z0-9]", regex=True)
        return out


class ReplyWordCountFeature(TransformBase):
    """Bereken schone woordlengte (`word_count`), `prev_words` en `log10_time`."""

    def transform(
        self,
        data: pd.DataFrame,
        text_col: str = "message",
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        out["word_count"] = out[text_col].apply(count_clean_words).astype(int)
        out["prev_words"] = out["word_count"].shift(1).fillna(0).astype(int)

        if "response_time_min" in out.columns:
            valid_pair = (
                out["response_time_min"].notna()
                & (out["prev_words"] > 0)
                & out[text_col].notna()
            )
            clipped_rt = out["response_time_min"].clip(lower=0.05)
            out["log10_time"] = np.where(valid_pair, np.log10(clipped_rt), np.nan)
        return out


def classify_theme(text: str) -> str:
    """Classificeer een bericht of sessietekst in één van de 4 leefdomeinen of 'Overig'.

    Telt per domein het aantal regex-matches en kiest het domein met de hoogste
    frequentie (conform Les 6 / Figuur 5).
    """
    lower = text.lower()
    best_domain = "Overig"
    best_count = 0
    for domain, pattern in THEME_DOMAIN_PATTERNS.items():
        cnt = len(re.findall(pattern, lower))
        if cnt > best_count:
            best_count = cnt
            best_domain = domain
    return best_domain


class ThematicRegexFeature(TransformBase):
    """Pas alle 16 thematische sub-regexes én de overkoepelende domeinclassificatie toe."""

    def transform(
        self,
        data: pd.DataFrame,
        column: str = "message",
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        lower_series = out[column].fillna("").str.lower()
        for rx_name, rx_pattern in THEMATIC_REGEXES_16.items():
            out[rx_name] = lower_series.str.count(rx_pattern)
        out["theme"] = lower_series.apply(classify_theme)
        return out
