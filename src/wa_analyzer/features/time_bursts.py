"""Tijd- en burst-features: dagdelen, reactietijden, empirische pauzedrempel en sessies."""

from __future__ import annotations

import numpy as np
import pandas as pd
from goad_toolkit.analytics import DistributionFitter, FitResult
from goad_toolkit.datatransforms import TransformBase
from goad_toolkit.distributions import DistributionRegistry

from wa_analyzer.config import (
    MAX_RESPONSE_MINUTES,
    THAILAND_END,
    THAILAND_START,
)


class DayPart(TransformBase):
    """Verrijk een tijdstempel-kolom met uur, datum en Nederlands dagdeel."""

    def transform(
        self,
        data: pd.DataFrame,
        column: str = "timestamp",
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        ts = pd.to_datetime(out[column])
        out["hour"] = ts.dt.hour
        out["date"] = ts.dt.date
        out["day_part"] = pd.cut(
            out["hour"],
            bins=[0, 6, 12, 18, 24],
            labels=["Nacht", "Ochtend", "Middag", "Avond"],
            right=False,
        ).astype(str)
        return out


class PeriodFeature(TransformBase):
    """Voeg weekdag/weekend-classificatie en de Thailand-eventvlag toe."""

    def transform(
        self,
        data: pd.DataFrame,
        column: str = "day_name",
        thailand_start: str = THAILAND_START,
        thailand_end: str = THAILAND_END,
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        out["is_weekend"] = out[column].isin(["Saturday", "Sunday"])
        out["period"] = np.where(out["is_weekend"], "Weekend", "Werkdag")

        ts = pd.to_datetime(out["timestamp"])
        dates_norm = ts.dt.normalize()
        start_dt = pd.Timestamp(thailand_start)
        end_dt = pd.Timestamp(thailand_end)
        out["is_thailand"] = (dates_norm >= start_dt) & (dates_norm <= end_dt)
        return out


class ResponseTimeFeature(TransformBase):
    """Bereken de 1-op-1 reactietijd in minuten bij sprekerwisseling op dezelfde dag."""

    def transform(
        self,
        data: pd.DataFrame,
        timestamp_col: str = "timestamp",
        author_col: str = "author",
        max_minutes: float = MAX_RESPONSE_MINUTES,
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        ts = pd.to_datetime(out[timestamp_col])
        out["delta_sec"] = ts.diff().dt.total_seconds()
        out["prev_author"] = out[author_col].shift(1)
        out["is_reply"] = out[author_col] != out["prev_author"]
        out["same_day"] = ts.dt.date == ts.shift(1).dt.date

        delta_min = out["delta_sec"] / 60.0
        valid_reply = (
            out["is_reply"]
            & out["same_day"]
            & (delta_min > 0.0)
            & (delta_min <= max_minutes)
        )
        out["response_time_min"] = np.where(valid_reply, delta_min, np.nan)
        return out


def fit_session_threshold(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    author_col: str = "author",
    tail: float = 0.05,
) -> float:
    """Bepaal empirisch de sessie-pauzedrempel (in seconden) via een exponentiële MLE-fit.

    Fit een exponentiële verdeling op alle inter-message pauzes binnen dezelfde auteur
    (0 < gap < 3600s) met `DistributionFitter(seed=42)` en retourneert de 95%-drempel
    in seconden (~1262s ≈ 21,0 minuten).
    """
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(df[timestamp_col]),
            "author": df[author_col],
        }
    ).sort_values(["author", "timestamp"], kind="stable")
    gaps = frame.groupby("author")["timestamp"].diff().dt.total_seconds()
    burst = gaps[(gaps > 0.0) & (gaps < 3600.0)]

    registry = DistributionRegistry()
    fit = DistributionFitter(registry, seed=42).fit_distribution(
        "exponential", burst.to_numpy()
    )
    if not isinstance(fit, FitResult):
        raise ValueError(f"Exponential fit failed on burst gaps: {fit}")

    loc = float(fit.params[0])
    scale = float(fit.params[1])
    return float(loc + scale * np.log(1.0 / tail))


class SessionizeFeature(TransformBase):
    """Ken een `session_id` toe op basis van de empirische pauzedrempel (~21 min)."""

    def transform(
        self,
        data: pd.DataFrame,
        timestamp_col: str = "timestamp",
        author_col: str = "author",
        *_args: object,
        **_kwargs: object,
    ) -> pd.DataFrame:
        out = data.copy()
        sorted_df = out.sort_values(timestamp_col, kind="stable")
        threshold_sec = fit_session_threshold(
            sorted_df, timestamp_col=timestamp_col, author_col=author_col
        )
        gaps_sec = (
            pd.to_datetime(sorted_df[timestamp_col])
            .diff()
            .dt.total_seconds()
            .fillna(threshold_sec + 1.0)
        )
        session_ids = (gaps_sec > threshold_sec).cumsum()
        out["session_id"] = session_ids.reindex(out.index).astype(int)
        out["session_threshold_min"] = threshold_sec / 60.0
        return out


def build_sessions_dataframe(
    df: pd.DataFrame,
    min_words: int = 6,
) -> tuple[pd.DataFrame, float]:
    """Groepeer berichten per (session_id, author) tot dialoog-eenheden (N = 1.965 bij ≥ 6w).

    Returns:
        Tuple van `(df_sessions, threshold_min)`.
    """
    threshold_min = (
        float(df["session_threshold_min"].iloc[0])
        if "session_threshold_min" in df.columns and len(df) > 0
        else fit_session_threshold(df) / 60.0
    )

    df_sorted = df.sort_values("timestamp", kind="stable").reset_index(drop=True)
    units = (
        df_sorted.groupby(["session_id", "author"], as_index=False)
        .agg(
            text=(
                "message",
                lambda msgs: " ".join(str(m) for m in msgs if pd.notna(m)),
            ),
            timestamp=("timestamp", "min"),
            n_msgs=("message", "count"),
        )
        .reset_index(drop=True)
    )
    units["word_count"] = units["text"].apply(lambda s: len(str(s).split()))
    df_sessions = units[units["word_count"] >= min_words].copy().reset_index(drop=True)
    df_sessions["session_threshold_min"] = threshold_min
    return df_sessions, threshold_min
