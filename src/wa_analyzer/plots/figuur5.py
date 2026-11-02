"""Figuur 5: Stylometrische vectorruimte en taalconvergentie over de tijd.

Adopteert Les 6 cel 28-30 van DAV:
- 13 stilistische features op tekstchunks (600 tekens).
- 2x2 raster over kalenderjaren (2022-2025).
- Centroidafstand (Euclidisch) tussen auteurs per kalenderjaar.
- Statistische verificatie via 1-NN cross-validatie nauwkeurigheid en silhouette score.
"""

import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from wa_analyzer.features.stylometry import (
    STYLE_FEATURE_NAMES,
    build_chunks_dataframe,
)
from wa_analyzer.visualizer import StylometryTimelinePlot


@dataclass(frozen=True)
class Figuur5StylometryResult:
    """Bevindingen van het stylometrische PCA-tijdreeksmodel."""

    chunks_df: pd.DataFrame
    pca_df: pd.DataFrame
    deltas_df: pd.DataFrame
    pca_model: PCA
    scaler: StandardScaler
    metrics_by_year: dict[int, dict[str, float]]
    n_total_chunks: int
    delta_initial: float
    delta_final: float
    delta_reduction_pct: float

    def to_dict(self) -> dict[str, Any]:
        """Exporteert kernresultaten naar dictionary voor rapportage."""
        return {
            "n_total_chunks": self.n_total_chunks,
            "delta_initial": self.delta_initial,
            "delta_final": self.delta_final,
            "delta_reduction_pct": self.delta_reduction_pct,
            "metrics_by_year": self.metrics_by_year,
        }


def fit_figuur5_stylometry(
    df_chat: pd.DataFrame,
    chunk_size: int = 600,
    years: list[int] | None = None,
    seed: int = 42,
) -> Figuur5StylometryResult:
    """Berekent stylometrische features, PCA-projectie en convergentie per kalenderjaar.

    Parameters
    ----------
    df_chat : pd.DataFrame
        Geparseerde chatberichten met kolommen 'author', 'message' en 'timestamp'.
    chunk_size : int, default=600
        Aantal karakters per tekstchunk.
    years : list[int], optional
        Jaren om te analyseren; standaard [2022, 2023, 2024, 2025].
    seed : int, default=42
        Willekeurige zaadwaarde voor reproduceerbaarheid.

    Returns
    -------
    Figuur5StylometryResult
        Dataclass met alle berekende dataframes, PCA-model en metrieken.
    """
    if years is None:
        years = [2022, 2023, 2024, 2025]

    chunks_df = build_chunks_dataframe(df_chat, chunk_size=chunk_size, years=years)
    if chunks_df.empty:
        raise ValueError("Geen geldige tekstchunks gevonden voor de opgegeven jaren.")

    x_features = chunks_df[STYLE_FEATURE_NAMES].values
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_features)

    pca = PCA(n_components=2, random_state=seed)
    coords = pca.fit_transform(x_scaled)

    pca_df = chunks_df.copy()
    pca_df["pca1"] = coords[:, 0]
    pca_df["pca2"] = coords[:, 1]
    pca_df["pca_x"] = coords[:, 0]
    pca_df["pca_y"] = coords[:, 1]

    delta_rows: list[dict[str, Any]] = []
    metrics_by_year: dict[int, dict[str, float]] = {}

    for year in years:
        df_y = pca_df[pca_df["year"] == year]
        if df_y.empty:
            continue

        p_coords = df_y[df_y["author"] == "Partner"][["pca1", "pca2"]].values
        s_coords = df_y[df_y["author"] == "Student"][["pca1", "pca2"]].values

        if len(p_coords) == 0 or len(s_coords) == 0:
            continue

        c_p = p_coords.mean(axis=0)
        c_s = s_coords.mean(axis=0)
        delta_val = float(np.linalg.norm(c_p - c_s))

        # 1-NN cross-validatie nauwkeurigheid & silhouette score
        y_labels = df_y["author"].values
        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(df_y[["pca1", "pca2"]].values, y_labels)
        acc_1nn = float(knn.score(df_y[["pca1", "pca2"]].values, y_labels))

        sil = (
            float(silhouette_score(df_y[["pca1", "pca2"]].values, y_labels))
            if len(set(y_labels)) > 1
            else 0.0
        )

        delta_rows.append(
            {
                "year": year,
                "delta": delta_val,
                "n_chunks": len(df_y),
                "n_partner": len(p_coords),
                "n_student": len(s_coords),
                "accuracy_1nn": acc_1nn,
                "silhouette": sil,
            }
        )
        metrics_by_year[year] = {
            "delta": delta_val,
            "accuracy_1nn": acc_1nn,
            "silhouette": sil,
            "n_chunks": float(len(df_y)),
        }

    deltas_df = pd.DataFrame(delta_rows)

    d_init = delta_rows[0]["delta"] if delta_rows else 0.0
    d_final = delta_rows[-1]["delta"] if delta_rows else 0.0
    reduct = ((d_init - d_final) / d_init * 100.0) if d_init > 0 else 0.0

    return Figuur5StylometryResult(
        chunks_df=chunks_df,
        pca_df=pca_df,
        deltas_df=deltas_df,
        pca_model=pca,
        scaler=scaler,
        metrics_by_year=metrics_by_year,
        n_total_chunks=len(pca_df),
        delta_initial=d_init,
        delta_final=d_final,
        delta_reduction_pct=reduct,
    )


def plot_figuur5(
    result: Figuur5StylometryResult,
    save_path: Path | None = None,
) -> Figure:
    """Genereert en retourneert de 2x2 stylometrische tijdreeksvisualisatie.

    Parameters
    ----------
    result : Figuur5StylometryResult
        Het berekende resultaat van `fit_figuur5_stylometry`.
    save_path : Path, optional
        Optioneel pad om de figuur als PNG/PDF op te slaan.

    Returns
    -------
    plt.Figure
        De resulterende matplotlib-figuur.
    """
    plot = StylometryTimelinePlot()
    fig, _ = plot.build(result.pca_df, result.deltas_df)

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=200, bbox_inches="tight")

    plt.close(fig)
    return fig
