"""Centrale pipeline-orchestratie: van ruwe tekst naar één verrijkte feature-set."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from goad_toolkit.datatransforms import Pipeline, RegexFeature, TimeFeatures
from loguru import logger

from wa_analyzer.config import (
    DELETED_PATTERN,
    MEDIA_PATTERN,
    ONLY_MEDIA_PATTERN,
    URL_PATTERN,
    PipelineConfig,
)
from wa_analyzer.features.embeddings import enrich_sessions_with_embeddings
from wa_analyzer.features.text_regex import (
    EmojiOnly,
    ReplyWordCountFeature,
    ThematicRegexFeature,
)
from wa_analyzer.features.time_bursts import (
    DayPart,
    PeriodFeature,
    ResponseTimeFeature,
    SessionizeFeature,
    build_sessions_dataframe,
)
from wa_analyzer.preprocess import parse_raw_chat


def build_message_pipeline() -> Pipeline:
    """Construeer de centrale `goad_toolkit` Pipeline voor alle bericht-features.

    Volgt strikt het Source-to-Sinks principe: elke stap voegt deterministische
    kolommen toe aan hetzelfde DataFrame zonder wees-variabelen.
    """
    pipe = Pipeline()
    pipe.add(TimeFeatures, name="time_features", column="timestamp")
    pipe.add(
        RegexFeature,
        name="url_flag",
        column="message",
        pattern=URL_PATTERN,
        feature="has_url",
        mode="has",
    )
    pipe.add(
        RegexFeature,
        name="deleted_flag",
        column="message",
        pattern=DELETED_PATTERN,
        feature="is_deleted",
        mode="has",
    )
    pipe.add(
        RegexFeature,
        name="media_flag",
        column="message",
        pattern=MEDIA_PATTERN,
        feature="has_media",
        mode="has",
    )
    pipe.add(
        RegexFeature,
        name="only_media_flag",
        column="message",
        pattern=ONLY_MEDIA_PATTERN,
        feature="has_only_media",
        mode="has",
    )
    pipe.add(DayPart, name="day_part", column="timestamp")
    pipe.add(PeriodFeature, name="period_feature", column="day_name")
    pipe.add(EmojiOnly, name="emoji_only", column="message", feature="only_emoji")
    pipe.add(ResponseTimeFeature, name="response_time", timestamp_col="timestamp")
    pipe.add(ReplyWordCountFeature, name="word_counts", text_col="message")
    pipe.add(ThematicRegexFeature, name="thematic_regexes", column="message")
    pipe.add(SessionizeFeature, name="sessionize", timestamp_col="timestamp")
    return pipe


def run_feature_pipeline(
    config: PipelineConfig,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Voer de volledige datapijplijn uit van `_chat.txt` naar verrijkte Parquet-bestanden.

    Args:
        config: `PipelineConfig` met in- en uitvoerpaden en modelinstellingen.

    Returns:
        Tuple `(df_chat, df_sessions)`.
    """
    df_raw = parse_raw_chat(config.raw_chat_path, config.author_mapping)

    message_pipe = build_message_pipeline()
    df_chat = message_pipe.apply(df_raw, keep_intermediate=False)

    df_sessions_base, _ = build_sessions_dataframe(
        df_chat, min_words=config.min_session_words
    )
    df_sessions = enrich_sessions_with_embeddings(
        df_sessions_base,
        model_name=config.embedding_model,
        random_state=config.random_seed,
    )

    config.processed_chat_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df_chat.to_parquet(config.processed_chat_path, index=False)
        df_sessions.to_parquet(config.processed_sessions_path, index=False)
        logger.info(
            f"Saved enriched datasets to {config.processed_chat_path} "
            f"({len(df_chat):,} rows) and {config.processed_sessions_path} "
            f"({len(df_sessions):,} rows)"
        )
    except PermissionError:
        logger.warning(
            f"Datasets in {config.processed_chat_path.parent} are locked by another process; "
            "using in-memory DataFrames."
        )

    return df_chat, df_sessions


def load_chat_data(processed_path: Path) -> pd.DataFrame:
    """Laad het verrijkte berichten-DataFrame (`chat.parq`)."""
    return pd.read_parquet(processed_path)


def load_sessions_data(sessions_path: Path) -> pd.DataFrame:
    """Laad het verrijkte sessie-DataFrame (`sessions.parq`)."""
    return pd.read_parquet(sessions_path)
