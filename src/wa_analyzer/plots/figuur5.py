"""Figuur 5 (Les 6): 384D Hugging Face MiniLM PCA-vectorruimte (Jeffrey huisman vs. Rick werk)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from wa_analyzer.config import THEME_ORDER
from wa_analyzer.visualizer import (
    JeffreyPlotSettings,
    SemanticPCAPlot,
    format_footnote,
)


@dataclass(frozen=True)
class Figuur5PCAResult:
    """Statistische samenvatting en centroïden van de 384D PCA-projectie (Les 6)."""

    sessions_df: pd.DataFrame
    theme_centroids: pd.DataFrame
    author_centroids: pd.DataFrame
    author_theme_counts: pd.DataFrame
    author_theme_shares: pd.DataFrame
    jeffrey_food: int
    rick_food: int
    jeffrey_work: int
    rick_work: int
    pc1_var: float
    pc2_var: float
    cum2_var: float
    threshold_min: float
    n_sessions: int


def fit_figuur5_pca(df_sessions: pd.DataFrame) -> Figuur5PCAResult:
    """Bereken thematische centroïden, auteur-tellingen en domeinverdelingen."""
    theme_centroids = (
        df_sessions.groupby("theme", as_index=False)
        .agg(
            pca_x=("pca_x", "mean"),
            pca_y=("pca_y", "mean"),
            n_units=("pca_x", "count"),
        )
        .set_index("theme")
        .reindex([t for t in THEME_ORDER if t in df_sessions["theme"].unique()])
        .reset_index()
    )

    author_centroids = (
        df_sessions.groupby("author", as_index=False)
        .agg(
            pca_x=("pca_x", "mean"),
            pca_y=("pca_y", "mean"),
            n_units=("pca_x", "count"),
        )
        .set_index("author")
        .reindex(["Student", "Partner"])
        .reset_index()
    )

    author_theme_counts = pd.crosstab(df_sessions["author"], df_sessions["theme"])
    author_theme_shares = (
        pd.crosstab(
            df_sessions["author"],
            df_sessions["theme"],
            normalize="index",
        )
        * 100.0
    )

    jeffrey_food = int(
        len(
            df_sessions[
                (df_sessions["author"] == "Student")
                & (df_sessions["theme"] == "Huishouden en Voeding")
            ]
        )
    )
    rick_food = int(
        len(
            df_sessions[
                (df_sessions["author"] == "Partner")
                & (df_sessions["theme"] == "Huishouden en Voeding")
            ]
        )
    )
    jeffrey_work = int(
        len(
            df_sessions[
                (df_sessions["author"] == "Student")
                & (df_sessions["theme"] == "Werk en Mobiliteit")
            ]
        )
    )
    rick_work = int(
        len(
            df_sessions[
                (df_sessions["author"] == "Partner")
                & (df_sessions["theme"] == "Werk en Mobiliteit")
            ]
        )
    )

    pc1_var = float(df_sessions["pc1_var"].iloc[0])
    pc2_var = float(df_sessions["pc2_var"].iloc[0])
    threshold_min = (
        float(df_sessions["session_threshold_min"].iloc[0])
        if "session_threshold_min" in df_sessions.columns
        else 21.0
    )

    return Figuur5PCAResult(
        sessions_df=df_sessions,
        theme_centroids=theme_centroids,
        author_centroids=author_centroids,
        author_theme_counts=author_theme_counts,
        author_theme_shares=author_theme_shares,
        jeffrey_food=jeffrey_food,
        rick_food=rick_food,
        jeffrey_work=jeffrey_work,
        rick_work=rick_work,
        pc1_var=pc1_var,
        pc2_var=pc2_var,
        cum2_var=pc1_var + pc2_var,
        threshold_min=threshold_min,
        n_sessions=len(df_sessions),
    )


def plot_figuur5(
    pca_res: Figuur5PCAResult,
    save_path: Path | None = None,
) -> Figure:
    """Genereer Figuur 5: 2D PCA-projectie van de 384D Hugging Face MiniLM vectorruimte."""
    units = pca_res.sessions_df
    tc = pca_res.theme_centroids.set_index("theme")
    cx_food = float(tc.loc["Huishouden en Voeding", "pca_x"])
    cy_food = float(tc.loc["Huishouden en Voeding", "pca_y"])
    cx_work = float(tc.loc["Werk en Mobiliteit", "pca_x"])
    cy_work = float(tc.loc["Werk en Mobiliteit", "pca_y"])

    settings = JeffreyPlotSettings(figsize=(11, 9.6), title="")
    fig, ax = SemanticPCAPlot(settings).plot(
        units=units,
        cx_food=cx_food,
        cy_food=cy_food,
        cx_work=cx_work,
        cy_work=cy_work,
    )

    ax.annotate(
        f"Huishouden en Voeding\nJeffrey: {pca_res.jeffrey_food} | Rick: {pca_res.rick_food} sessies\n(Jeffrey leidt met +44%)",
        xy=(cx_food, cy_food),
        xytext=(25, 20),
        textcoords="offset points",
        fontsize=9.0,
        fontweight="bold",
        color="#B45309",
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#FEF3C7",
            "edgecolor": "#D97706",
            "alpha": 0.95,
            "lw": 1.2,
        },
        arrowprops={"arrowstyle": "->", "color": "#D97706", "lw": 1.4, "shrinkB": 6},
        zorder=7,
    )

    ax.annotate(
        f"Werk en Mobiliteit\nRick: {pca_res.rick_work} | Jeffrey: {pca_res.jeffrey_work} sessies\n(Rick leidt met +23%)",
        xy=(cx_work, cy_work),
        xytext=(-175, -45),
        textcoords="offset points",
        fontsize=9.0,
        fontweight="bold",
        color="#1D4ED8",
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#DBEAFE",
            "edgecolor": "#2563EB",
            "alpha": 0.95,
            "lw": 1.2,
        },
        arrowprops={"arrowstyle": "->", "color": "#2563EB", "lw": 1.4, "shrinkB": 6},
        zorder=7,
    )

    ax.set_title(
        "Jeffrey is meer de huisman, terwijl Rick zich focust op werk in onze chat",
        fontsize=12.2,
        fontweight="bold",
        pad=38,
        color="#1A202C",
        loc="left",
    )

    n_units_fmt = f"{pca_res.n_sessions:,}".replace(",", ".")
    pc1_str = f"{pca_res.pc1_var:.1f}%".replace(".", ",")
    pc2_str = f"{pca_res.pc2_var:.1f}%".replace(".", ",")
    cum_str = f"{pca_res.cum2_var:.1f}%".replace(".", ",")

    subtitle = (
        f"2D PCA-projectie van 384D Hugging Face embeddings (N = {n_units_fmt} dialoogsessies; PC1: {pc1_str}, PC2: {pc2_str}).\n"
        "Punten gekleurd op thema: Huishouden en Voeding (oranje) vs. Werk en Mobiliteit (blauw); secundaire thema's gedimd. Vorm: Jeffrey (○), Rick (△)."
    )
    ax.text(
        0.0,
        1.02,
        subtitle,
        transform=ax.transAxes,
        fontsize=8.8,
        style="italic",
        color="#4A5568",
        va="bottom",
        ha="left",
    )

    ax.set_xlabel(
        f"Hoofdcomponent 1 ({pc1_str} variantie) — Semantische as 1",
        fontsize=9.2,
        color="#1A202C",
    )
    ax.set_ylabel(
        f"Hoofdcomponent 2 ({pc2_str} variantie) — Semantische as 2",
        fontsize=9.2,
        color="#1A202C",
    )

    footnote_text = (
        "* Methodologie & Verantwoording (Hugging Face 384D):\n"
        f"  Tekstsegmenten (N = {n_units_fmt}, min. 6 woorden, empirische pauzedrempel = {pca_res.threshold_min:.0f} min) omgezet naar 384D dichte vectoren via all-MiniLM-L6-v2.\n"
        f"  Na L2-normalisatie (cosinus-ruimte) projecteert 2D PCA de continue semantische ruimte (cumulatieve variantie: {cum_str}).\n"
        f"  Steekproefverdeling kerndomeinen: Huishouden en Voeding: Jeffrey n={pca_res.jeffrey_food}, Rick n={pca_res.rick_food} | Werk en Mobiliteit: Rick n={pca_res.rick_work}, Jeffrey n={pca_res.jeffrey_work}."
    )
    format_footnote(ax, text=footnote_text, y_offset=-0.21)

    plt.subplots_adjust(bottom=0.24, top=0.83, left=0.10, right=0.95)

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return fig
