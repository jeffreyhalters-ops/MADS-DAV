"""Feature-extractie modules voor tijd/bursts, tekst/regex en 384D embeddings."""

from wa_analyzer.features.embeddings import enrich_sessions_with_embeddings
from wa_analyzer.features.text_regex import (
    EmojiOnly,
    ReplyWordCountFeature,
    ThematicRegexFeature,
    classify_theme,
)
from wa_analyzer.features.time_bursts import (
    DayPart,
    PeriodFeature,
    ResponseTimeFeature,
    SessionizeFeature,
    build_sessions_dataframe,
    fit_session_threshold,
)

__all__ = [
    "DayPart",
    "EmojiOnly",
    "PeriodFeature",
    "ReplyWordCountFeature",
    "ResponseTimeFeature",
    "SessionizeFeature",
    "ThematicRegexFeature",
    "build_sessions_dataframe",
    "classify_theme",
    "enrich_sessions_with_embeddings",
    "fit_session_threshold",
]
