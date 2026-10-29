"""Hugging Face MiniLM 384D embeddings, L2-cosinusnormalisatie en 2D PCA-projectie."""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
from loguru import logger
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

from wa_analyzer.config import THEMATIC_REGEXES_16
from wa_analyzer.features.text_regex import classify_theme

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

DEFAULT_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"


def enrich_sessions_with_embeddings(
    df_sessions: pd.DataFrame,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    random_state: int = 42,
) -> pd.DataFrame:
    """Verrijk sessie-eenheden met 16 regexes, 384D MiniLM embeddings en 2D PCA-coördinaten.

    Args:
        df_sessions: DataFrame met geaggregeerde sessie-beurten (`text`, `author`, `word_count`).
        model_name: Naam van het Hugging Face SentenceTransformer model.
        random_state: Random seed voor reproduceerbare PCA-decompositie.

    Returns:
        Verrijkt sessie-DataFrame met `theme`, 16 `rx_*` kolommen, `pca_x`, `pca_y`,
        `pc1_var`, `pc2_var` en `cum2_var`.
    """
    result = df_sessions.copy()
    lower_texts = result["text"].fillna("").str.lower()

    for rx_name, rx_pattern in THEMATIC_REGEXES_16.items():
        result[rx_name] = lower_texts.str.count(rx_pattern)

    result["theme"] = result["text"].apply(classify_theme)

    logger.info(f"Encoding {len(result):,} sessions with {model_name} (384D)...")
    model = SentenceTransformer(model_name, local_files_only=True)
    raw_vectors = model.encode(
        result["text"].tolist(),
        batch_size=64,
        show_progress_bar=False,
        convert_to_numpy=True,
    )

    norms = np.linalg.norm(raw_vectors, axis=1, keepdims=True)
    vectors_l2 = raw_vectors / np.maximum(norms, 1e-12)

    pca = PCA(n_components=2, random_state=random_state)
    coords = pca.fit_transform(vectors_l2)

    pc1_var = float(pca.explained_variance_ratio_[0] * 100.0)
    pc2_var = float(pca.explained_variance_ratio_[1] * 100.0)

    result["pca_x"] = coords[:, 0]
    result["pca_y"] = coords[:, 1]
    result["pc1_var"] = pc1_var
    result["pc2_var"] = pc2_var
    result["cum2_var"] = pc1_var + pc2_var

    logger.info(
        f"PCA 2D projection complete: PC1={pc1_var:.1f}%, PC2={pc2_var:.1f}% "
        f"(cum={pc1_var + pc2_var:.1f}%)"
    )
    return result
