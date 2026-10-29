"""Figuur 3 (Les 4): Kansverdeling voor & tijdens Thailand-reis (Negatief-Binomiaal & Permutatietoets)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from goad_toolkit.analytics import (
    DistributionFitter,
    FitResult,
    NullDistribution,
    NullResult,
)
from goad_toolkit.distributions import DistributionRegistry
from matplotlib.figure import Figure

from wa_analyzer.config import (
    THAILAND_END,
    THAILAND_START,
)
from wa_analyzer.visualizer import (
    JeffreyPlotSettings,
    NegativeBinomialPlot,
    annotate_badge,
    annotate_context_badge,
    format_footnote,
    format_header,
)


@dataclass(frozen=True)
class Figuur3DistributionResult:
    """Statistische en distributie-fit resultaten voor Figuur 3 (Les 4)."""

    daily_df: pd.DataFrame
    counts_base: np.ndarray
    counts_thai: np.ndarray
    fit_base: FitResult
    fit_thai: FitResult
    null_result: NullResult
    mean_base: float
    mean_thai: float
    diff_mean: float
    quiet_days_base_pct: float
    peak_thai: int
    n_days_base: int
    n_days_thai: int
    p_perm: float


def _mean_diff_stat(frame: pd.DataFrame) -> float:
    """Verschil in daggemiddelde tussen Thailand-reis en de 4-jarige baseline."""
    means = frame.groupby("is_thailand")["messages"].mean()
    return float(means[True] - means[False])


def fit_figuur3_distributions(
    df_chat: pd.DataFrame,
    n_iter: int = 2000,
    seed: int = 42,
) -> Figuur3DistributionResult:
    """Fit discrete Negatief-Binomiale verdelingen en voer de permutatietoets uit."""
    daily = (
        df_chat.set_index("timestamp")
        .resample("D")
        .size()
        .rename("messages")
        .reset_index()
    )
    daily["is_thailand"] = (daily["timestamp"] >= THAILAND_START) & (
        daily["timestamp"] <= THAILAND_END
    )

    th_days = daily[daily["is_thailand"]].copy()
    base_days = daily[~daily["is_thailand"]].copy()

    counts_base = base_days["messages"].to_numpy(dtype=float)
    counts_thai = th_days["messages"].to_numpy(dtype=float)

    fitter = DistributionFitter(DistributionRegistry(), seed=seed)
    fit_base = fitter.fit_distribution("nbinom", counts_base)
    fit_thai = fitter.fit_distribution("nbinom", counts_thai)
    if not isinstance(fit_base, FitResult) or not isinstance(fit_thai, FitResult):
        raise RuntimeError("Negative binomial fit failed on daily message counts.")

    null_res = NullDistribution(_mean_diff_stat, n_iter=n_iter, seed=seed).run(
        daily,
        label="is_thailand",
    )

    mean_base = float(base_days["messages"].mean())
    mean_thai = float(th_days["messages"].mean())
    diff_mean = mean_thai - mean_base
    quiet_days_base_pct = float((base_days["messages"] < 3).mean() * 100.0)
    peak_thai = int(th_days["messages"].max())

    rng = np.random.default_rng(seed)
    all_messages = daily["messages"].to_numpy(dtype=float)
    n_th = len(th_days)
    perm_diffs = [
        float(perm[:n_th].mean() - perm[n_th:].mean())
        for perm in (rng.permutation(all_messages) for _ in range(n_iter))
    ]
    p_perm = float((np.array(perm_diffs) >= diff_mean).mean())

    return Figuur3DistributionResult(
        daily_df=daily,
        counts_base=counts_base,
        counts_thai=counts_thai,
        fit_base=fit_base,
        fit_thai=fit_thai,
        null_result=null_res,
        mean_base=mean_base,
        mean_thai=mean_thai,
        diff_mean=diff_mean,
        quiet_days_base_pct=quiet_days_base_pct,
        peak_thai=peak_thai,
        n_days_base=len(base_days),
        n_days_thai=len(th_days),
        p_perm=p_perm,
    )


def plot_figuur3(
    dist_res: Figuur3DistributionResult,
    save_path: Path | None = None,
) -> Figure:
    """Genereer Figuur 3: Kansdichtheid & Negatief-Binomiale fit voor en tijdens Thailand."""
    settings = JeffreyPlotSettings(figsize=(11.8, 6.0), title="")
    bins = np.arange(0, 108, 3)
    x_support = np.arange(0, 106)
    y_base = dist_res.fit_base.frozen_dist.pmf(x_support)
    y_th = dist_res.fit_thai.frozen_dist.pmf(x_support)

    fig, ax = NegativeBinomialPlot(settings).plot(
        base_messages=dist_res.counts_base,
        th_messages=dist_res.counts_thai,
        x_support=x_support,
        y_base=y_base,
        y_th=y_th,
        bins=bins,
    )

    ax.set_xlim(-1, 106)
    ax.set_ylim(0, 0.26)
    ax.set_xlabel(
        "Aantal WhatsApp-berichten per dag",
        fontsize=12,
        fontweight="bold",
        color=settings.dark_text,
        labelpad=10,
    )
    ax.set_ylabel(
        "Dichtheid (Density)",
        fontsize=12,
        fontweight="bold",
        color=settings.dark_text,
        labelpad=10,
    )
    ax.grid(axis="y", color="#E2E8F0", linestyle="--", linewidth=1.0, alpha=0.7)

    mean_base_str = f"{dist_res.mean_base:.1f}".replace(".", ",")
    mean_th_str = f"{dist_res.mean_thai:.1f}".replace(".", ",")
    p_val = dist_res.p_perm
    p_str = "p < 0,001" if p_val < 0.001 else f"p = {p_val:.3f}".replace(".", ",")

    annotate_context_badge(
        ax,
        text=(
            f"Thuisbasis:\n{dist_res.quiet_days_base_pct:.0f}% van de dagen ≤ 3 berichten\n"
            "(hoge dichtheid bij nul, daalt steil)"
        ),
        xy=(1.5, 0.178),
        xytext=(20.0, 0.22),
        settings=settings,
    )

    annotate_badge(
        ax,
        text=(
            "Thailand-reis:\nDichtheid vlakt af en spreidt ver uit\n"
            f"(gemiddelde verschuift van {mean_base_str} naar {mean_th_str})"
        ),
        xy=(26.0, 0.016),
        xytext=(40.0, 0.09),
        settings=settings,
    )

    annotate_badge(
        ax,
        text=f"Piekdag Thailand:\n{dist_res.peak_thai} berichten",
        xy=(float(dist_res.peak_thai), 0.005),
        xytext=(72.0, 0.05),
        settings=settings,
    )

    n_base_fmt = f"{dist_res.n_days_base:,}".replace(",", ".")

    format_header(
        ax,
        title="Van radiostilte naar berichtenregen: Thailand blaast stille WhatsApp-chat op",
        subtitle=(
            f"Kansdichtheid van dagelijkse berichten: Thuisbasis ({n_base_fmt} dagen, grijs) "
            f"versus Thailand-reis ({dist_res.n_days_thai} dagen, oranje)"
        ),
    )

    n_iter_fmt = f"{dist_res.null_result.n_iter:,}".replace(",", ".")
    footnote_text = (
        f"Werkelijke chatdagen (staven) gemodelleerd als dichtheid tegen de wiskundige nbinom-verdeling (lijnen): thuisbasis gem. {mean_base_str} ber/dag → Thailand gem. {mean_th_str} ber/dag.\n"
        f"Met {p_str} (Nulplot met {n_iter_fmt} iteraties) is toeval uitgesloten: de reis naar Thailand veranderde ons appgedrag compleet."
    )
    format_footnote(ax, text=footnote_text, y_offset=-0.18)

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fig
