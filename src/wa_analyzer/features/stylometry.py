"""Stijlometrie en tekststructuur-features voor Figuur 5 (Les 6)."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

FEATURE_NAMES_13: list[str] = [
    "gem_woordlengte",
    "korte_woorden_ratio",
    "lange_woorden_ratio",
    "kommas_intensiteit",
    "punten_intensiteit",
    "vraagtekens",
    "uitroeptekens",
    "hoofdletters_ratio",
    "cijfers_ratio",
    "herhaalde_letters",
    "emojis_ratio",
    "smileys_ratio",
    "informele_partikels",
]

STYLE_FEATURE_NAMES = FEATURE_NAMES_13


def extract_style_features(text: str) -> list[float]:
    """Extraheer 13 objectieve stijl- en interpunctiekenmerken uit een tekstfragment."""
    n_chars = max(len(text), 1)
    words = text.split()
    n_words = max(len(words), 1)
    word_lens = [len(w) for w in words]

    avg_word_len = float(np.mean(word_lens)) if word_lens else 0.0
    short_words = sum(1 for el in word_lens if el <= 3) / n_words
    long_words = sum(1 for el in word_lens if el >= 8) / n_words

    # Interpunctie: komma's (Jeffrey) versus punten (Rick)
    comma_rate = text.count(",") / n_chars * 100.0
    dot_rate = text.count(".") / n_chars * 100.0
    q_mark = text.count("?") / n_chars * 100.0
    excl_mark = text.count("!") / n_chars * 100.0

    # Typografie & structuur
    caps_ratio = sum(1 for c in text if c.isupper()) / n_chars * 100.0
    digits_ratio = sum(1 for c in text if c.isdigit()) / n_chars * 100.0
    repeated_letters = len(re.findall(r"(.)\1{2,}", text)) / n_chars * 100.0

    # Expressie & conversatie
    emojis = sum(1 for c in text if ord(c) >= 0x10000) / n_chars * 100.0
    smileys = len(re.findall(r"[:;=]-?[)\]D(\[pP/\\|oO]", text)) / n_chars * 100.0
    particles = (
        len(
            re.findall(
                r"\b(ff|thx|top|prima|idd|haha|hahaha|ow|oh|ja|nee|super|thnx|thanks|ok|oke|okee|succes|fijn)\b",
                text.lower(),
            )
        )
        / n_words
        * 100.0
    )

    return [
        avg_word_len,
        short_words,
        long_words,
        comma_rate,
        dot_rate,
        q_mark,
        excl_mark,
        caps_ratio,
        digits_ratio,
        repeated_letters,
        emojis,
        smileys,
        particles,
    ]


def build_chunks_dataframe(
    df: pd.DataFrame,
    chunk_size: int = 600,
    years: list[int] | None = None,
) -> pd.DataFrame:
    """Verdeel berichten over vaste chunks per (kalenderjaar, auteur) voor stabiele stijlometrie."""
    active_years = years if years is not None else [2022, 2023, 2024, 2025]
    frame = df.copy()
    if "year" not in frame.columns:
        ts = pd.to_datetime(frame["timestamp"])
        frame["year"] = ts.dt.year

    valid = frame[
        frame["year"].isin(active_years)
        & frame["message"].notna()
        & ~frame.get("has_only_media", False)
    ].sort_values("timestamp")

    chunks: list[dict[str, object]] = []
    for (yr, author), grp in valid.groupby(["year", "author"], observed=True):
        full_text = " ".join(str(m) for m in grp["message"] if pd.notna(m))
        for i in range(0, len(full_text) - chunk_size + 1, chunk_size):
            chunks.append(
                {
                    "year": int(yr),
                    "author": str(author),
                    "text": full_text[i : i + chunk_size],
                }
            )

    df_res = pd.DataFrame(chunks)
    if not df_res.empty:
        feats = np.array([extract_style_features(str(t)) for t in df_res["text"]])
        for idx, col in enumerate(FEATURE_NAMES_13):
            df_res[col] = feats[:, idx]

    return df_res
