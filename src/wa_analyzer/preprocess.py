"""Preprocessing: ruwe WhatsApp-export (_chat.txt) parsen en anonimiseren."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from loguru import logger

from wa_analyzer.config import AUTHOR_MAPPING

IOS_HEADER_PATTERN: str = r"^\[(\d{2}-\d{2}-\d{4}, \d{2}:\d{2}:\d{2})\]\s(.+?):\s(.*)$"
IOS_LINE_START_PATTERN: str = r"\[(.+?)]\s.+?:.+"
IOS_TIMESTAMP_FORMAT: str = "%d-%m-%Y, %H:%M:%S"


def parse_raw_chat(
    raw_path: Path,
    author_mapping: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Parse een ruwe iOS WhatsApp-export (.txt) en anonimiseer de auteurs.

    Behoudt exact de originele multi-line samenvoeging zodat de resulterende
    dataset exact N = 6.414 berichten bevat.

    Args:
        raw_path: Pad naar het ruwe `_chat.txt` bestand.
        author_mapping: Optionele dictionary voor auteur-anonimisering.

    Returns:
        Geanonimiseerd basis-DataFrame met kolommen `timestamp`, `author`, `message`.
    """
    mapping = author_mapping if author_mapping is not None else AUTHOR_MAPPING
    records: list[tuple[datetime, str, str]] = []
    header_regex = re.compile(IOS_HEADER_PATTERN)
    line_start_regex = re.compile(IOS_LINE_START_PATTERN)

    with raw_path.open(encoding="utf-8") as handle:
        raw_lines = handle.readlines()

    merged_lines: list[str] = []
    current_record = ""

    for line in raw_lines:
        if "waited for this message" in line or "encryption" in line:
            continue
        if line_start_regex.match(line):
            if current_record:
                merged_lines.append(current_record)
            current_record = line.strip()
        else:
            current_record += f" {line.strip()}"

    if current_record:
        merged_lines.append(current_record)

    for record_line in merged_lines:
        match = header_regex.match(record_line)
        if match:
            ts_raw, author_raw, message_raw = match.groups()
            ts = datetime.strptime(ts_raw, IOS_TIMESTAMP_FORMAT)
            clean_author = mapping.get(author_raw.strip(), author_raw.strip())
            records.append((ts, clean_author, message_raw.strip()))

    df = pd.DataFrame(records, columns=["timestamp", "author", "message"])
    df["message"] = df["message"].replace("", None)
    df["timestamp"] = pd.to_datetime(df["timestamp"]).astype("datetime64[us]")
    logger.info(f"Parsed {len(df):,} messages from {raw_path.name}")
    return df
