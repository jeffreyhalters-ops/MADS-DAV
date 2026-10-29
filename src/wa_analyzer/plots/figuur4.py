"""Figuur 4 (Les 5): Relatie tussen woordlengte en reactietijd (2-fasen stuksgewijze regressie)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats import pearsonr

from wa_analyzer.config import PIECEWISE_KNOT_WORDS
from wa_analyzer.visualizer import (
    JeffreyPlotSettings,
    PiecewiseRegPlot,
)


@dataclass(frozen=True)
class AuthorRegressionStats:
    """Statistieken per auteur voor Figuur 4 (Pearson r en reflexmediaan)."""

    name: str
    n: int
    r_val: float
    r_str: str
    p_str: str
    med_reflex: float


@dataclass(frozen=True)
class Figuur4PiecewiseResult:
    """Resultaten van de 2-fasen stuksgewijze regressie voor Figuur 4 (Les 5)."""

    binned_df: pd.DataFrame
    total_pairs: int
    n_sub: int
    knot_words: float
    coeffs_j: np.ndarray
    coeffs_r: np.ndarray
    x_grid: np.ndarray
    y_pred_j: np.ndarray
    y_pred_r: np.ndarray
    stats_res: dict[str, AuthorRegressionStats]


def _fit_piecewise_linear(df: pd.DataFrame, knot: float = 10.5) -> np.ndarray:
    """Fit een continue 2-fasen lineaire regressie die 100% aansluit bij `knot`."""
    x = df["prev_words"].to_numpy(dtype=float)
    y = df["log10_time"].to_numpy(dtype=float)
    design_mat = np.column_stack([np.ones_like(x), x, np.maximum(0.0, x - knot)])
    coeffs, _, _, _ = np.linalg.lstsq(design_mat, y, rcond=None)
    return coeffs


def _predict_piecewise_linear(
    x_vals: np.ndarray,
    coeffs: np.ndarray,
    knot: float = 10.5,
) -> np.ndarray:
    b0, b1, b2 = float(coeffs[0]), float(coeffs[1]), float(coeffs[2])
    return b0 + b1 * x_vals + b2 * np.maximum(0.0, x_vals - knot)


def fit_figuur4_piecewise(
    df_chat: pd.DataFrame,
    knot: float = PIECEWISE_KNOT_WORDS,
) -> Figuur4PiecewiseResult:
    """Fit het continue 2-fasen (broken-stick) regressiemodel per auteur over 9 woordgroepen."""
    valid_mask = (
        df_chat["response_time_min"].notna()
        & (df_chat["response_time_min"] > 0.0)
        & (df_chat["response_time_min"] <= 480.0)
        & (df_chat["prev_words"] > 0)
        & df_chat["message"].notna()
    )
    replies = df_chat.loc[
        valid_mask,
        ["author", "prev_words", "response_time_min", "log10_time"],
    ].copy()
    total_pairs = len(replies)

    sub = replies[replies["prev_words"].between(1, 40)].copy()

    word_bins = [1, 3, 5, 7, 10, 13, 17, 23, 31, 41]
    bin_labels = [
        "1–2w",
        "3–4w",
        "5–6w",
        "7–9w",
        "10–12w",
        "13–16w",
        "17–22w",
        "23–30w",
        "31–40w",
    ]
    sub["word_bin"] = pd.cut(
        sub["prev_words"],
        bins=word_bins,
        labels=bin_labels,
        right=False,
    )

    binned = (
        sub.groupby(["author", "word_bin"], observed=True)
        .agg(
            med_words=("prev_words", "median"),
            med_log=("log10_time", "median"),
            med_time=("response_time_min", "median"),
        )
        .reset_index()
    )

    coeffs_j = _fit_piecewise_linear(sub[sub["author"] == "Student"], knot)
    coeffs_r = _fit_piecewise_linear(sub[sub["author"] == "Partner"], knot)

    x_grid = np.linspace(1.0, 36.0, 300)
    y_pred_j = _predict_piecewise_linear(x_grid, coeffs_j, knot)
    y_pred_r = _predict_piecewise_linear(x_grid, coeffs_r, knot)

    stats_res: dict[str, AuthorRegressionStats] = {}
    for author_code, author_name in (("Student", "Jeffrey"), ("Partner", "Rick")):
        df_all_a = replies[replies["author"] == author_code]
        df_sub_a = sub[sub["author"] == author_code]
        r_val, p_r = pearsonr(df_all_a["prev_words"], df_all_a["log10_time"])
        p_str = (
            "p < 0,0001"
            if float(p_r) < 0.0001
            else f"p = {float(p_r):.4f}".replace(".", ",")
        )
        med_reflex = float(
            df_sub_a[df_sub_a["prev_words"] <= 10]["response_time_min"].median()
        )
        stats_res[author_code] = AuthorRegressionStats(
            name=author_name,
            n=len(df_all_a),
            r_val=float(r_val),
            r_str=f"r = {float(r_val):+.3f}".replace(".", ","),
            p_str=p_str,
            med_reflex=med_reflex,
        )

    return Figuur4PiecewiseResult(
        binned_df=binned,
        total_pairs=total_pairs,
        n_sub=len(sub),
        knot_words=knot,
        coeffs_j=coeffs_j,
        coeffs_r=coeffs_r,
        x_grid=x_grid,
        y_pred_j=y_pred_j,
        y_pred_r=y_pred_r,
        stats_res=stats_res,
    )


def plot_figuur4(
    model_res: Figuur4PiecewiseResult,
    save_path: Path | None = None,
) -> Figure:
    """Genereer Figuur 4: 2-fasen stuksgewijze regressie van woordlengte vs. reactietijd."""
    settings = JeffreyPlotSettings(figsize=(11.0, 6.0), title="")

    fig, ax = PiecewiseRegPlot(settings).plot(
        x_grid=model_res.x_grid,
        y_pred_j=model_res.y_pred_j,
        y_pred_r=model_res.y_pred_r,
        binned_df=model_res.binned_df,
        knot=model_res.knot_words,
    )

    ax.text(
        5.5,
        1.37,
        "REFLEXZONE (1–10w)",
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#475569",
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "#F1F5F9",
            "edgecolor": "#CBD5E0",
            "lw": 0.9,
        },
        zorder=5,
    )
    ax.text(
        23.5,
        1.37,
        "DENKZONE (11–36w)",
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#475569",
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "#F8FAFC",
            "edgecolor": "#E2E8F0",
            "lw": 0.9,
        },
        zorder=5,
    )

    j_ref = model_res.stats_res["Student"].med_reflex
    r_ref = model_res.stats_res["Partner"].med_reflex
    ax.annotate(
        (
            f"Snelle, vlakke reflex:\n"
            f"• Jeffrey (oranje): ~{j_ref:.1f} min\n"
            f"• Rick (blauw): ~{r_ref:.1f} min"
        ).replace(".", ","),
        xy=(4.5, 0.35),
        xytext=(2.5, 0.98),
        arrowprops={"arrowstyle": "->", "color": "#475569", "lw": 1.2},
        fontsize=8.8,
        fontweight="bold",
        color="#1E293B",
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "#FFFFFF",
            "edgecolor": "#CBD5E0",
        },
        zorder=6,
    )

    ax.set_xlim(0, 36)
    ax.set_ylim(-0.02, 1.45)

    x_ticks = [1, 5, 10, 15, 20, 25, 30, 35]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x) for x in x_ticks], fontsize=9.5, color="#4A5568")
    ax.set_xlabel(
        "Lengte ontvangen bericht van partner (aantal woorden)",
        fontsize=10.5,
        fontweight="bold",
        color="#2D3748",
        labelpad=8,
    )

    log_ticks = [
        float(np.log10(1)),
        float(np.log10(2)),
        float(np.log10(5)),
        float(np.log10(10)),
        float(np.log10(20)),
    ]
    log_labels = ["1 min", "2 min", "5 min", "10 min", "20 min"]
    ax.set_yticks(log_ticks)
    ax.set_yticklabels(log_labels, fontsize=9.5, color="#4A5568")
    ax.set_ylabel(
        "Reactietijd ontvanger (minuten, log-schaal)",
        fontsize=10.5,
        fontweight="bold",
        color="#2D3748",
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35, color="#CBD5E0")

    ax.set_title(
        "Langere berichten leiden tot langere reactietijd",
        fontsize=13.5,
        fontweight="bold",
        color="#1A202C",
        pad=38,
        loc="left",
    )
    ax.text(
        0.0,
        1.055,
        "Tot 10 woorden reageren we reflexmatig binnen 1 à 2 minuten; daarboven treedt lineaire vertraging op",
        transform=ax.transAxes,
        fontsize=9.0,
        color="#4A5568",
        ha="left",
    )
    ax.text(
        0.0,
        1.018,
        "― Jeffrey",
        transform=ax.transAxes,
        fontsize=9.0,
        fontweight="bold",
        color=settings.highlight_color,
        ha="left",
    )
    ax.text(
        0.082,
        1.018,
        "― Rick",
        transform=ax.transAxes,
        fontsize=9.0,
        fontweight="bold",
        color=settings.partner_blue,
        ha="left",
    )
    ax.text(
        0.148,
        1.018,
        "┆ Omslagpunt bij 10 woorden",
        transform=ax.transAxes,
        fontsize=9.0,
        color="#718096",
        ha="left",
    )

    n_pairs_fmt = f"{model_res.total_pairs:,}".replace(",", ".")
    j_s = model_res.stats_res["Student"]
    r_s = model_res.stats_res["Partner"]
    j_n_fmt = f"{j_s.n:,}".replace(",", ".")
    r_n_fmt = f"{r_s.n:,}".replace(",", ".")

    footnote_text = (
        f"* Noot: N = {n_pairs_fmt} directe interacties over 4 jaar WhatsApp-geschiedenis. Schone woordtelling via regex (excl. emoticons en media).\n"
        f"Statistische zekerheid (Pearson correlatie op log10-tijd): Jeffrey (n = {j_n_fmt}, {j_s.r_str}, {j_s.p_str}) en Rick (n = {r_n_fmt}, {r_s.r_str}, {r_s.p_str}).\n"
        "Bollen tonen de werkelijke mediane reactietijd over 9 woordgroepen."
    )

    fig.text(
        0.12,
        -0.035,
        footnote_text,
        fontsize=8,
        color="#718096",
        style="italic",
    )

    plt.tight_layout()

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fig
