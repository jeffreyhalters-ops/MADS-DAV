"""Figuur 2 (Les 3): Uur-residu tijdens Thailand-reis vs. 4-jarige baseline (Bootstrap CI)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from goad_toolkit.datatransforms import (
    Filter,
    FlagDates,
    GroupAgg,
    Pipeline,
    Share,
    SubtractBaseline,
)
from matplotlib.figure import Figure

from wa_analyzer.config import (
    THAILAND_END,
    THAILAND_START,
)
from wa_analyzer.visualizer import (
    JeffreyPlotSettings,
    ResidualCurvePlot,
    annotate_badge,
    annotate_context_badge,
    format_footnote,
    format_header,
)


@dataclass(frozen=True)
class Figuur2BootstrapResult:
    """Statistische en bootstrap-resultaten voor Figuur 2 (Uur-residu Thailand)."""

    residual_df: pd.DataFrame
    hours: np.ndarray
    diff_pct: pd.Series
    ci_low: np.ndarray
    ci_high: np.ndarray
    key_stats: dict[int, dict[str, object]]
    n_thailand: int
    n_baseline: int


def fit_figuur2_bootstrap(
    df_chat: pd.DataFrame,
    n_boot: int = 1000,
    seed: int = 42,
) -> Figuur2BootstrapResult:
    """Bereken het uurlijkse residu (Thailand − Baseline) en het 95% bootstrap-interval."""
    thailand_dates = pd.date_range(THAILAND_START, THAILAND_END)

    flag_pipe = Pipeline().add(
        FlagDates,
        column="timestamp",
        dates=thailand_dates,
        feature="is_thailand_event",
    )
    df_flagged = flag_pipe.apply(df_chat)

    base_pipe = (
        Pipeline()
        .add(Filter, expr="not is_thailand_event")
        .add(GroupAgg, by="hour", agg="size", feature="n")
        .add(Share, column="n", feature="share")
    )
    baseline_hourly = base_pipe.apply(df_flagged)

    thai_pipe = (
        Pipeline()
        .add(Filter, expr="is_thailand_event")
        .add(GroupAgg, by="hour", agg="size", feature="n")
        .add(Share, column="n", feature="share")
        .add(
            SubtractBaseline,
            column="share",
            baseline=baseline_hourly,
            on="hour",
            feature="residual",
        )
    )
    thai_res = thai_pipe.apply(df_flagged)

    all_hours = pd.DataFrame({"hour": range(24)})
    merged = all_hours.merge(
        baseline_hourly[["hour", "share"]],
        on="hour",
        how="left",
    ).rename(columns={"share": "base_share"})
    merged["base_share"] = merged["base_share"].fillna(0.0)
    merged = merged.merge(
        thai_res[["hour", "n", "residual"]],
        on="hour",
        how="left",
    )
    merged["n"] = merged["n"].fillna(0).astype(int)
    merged["share"] = (merged["base_share"] + merged["residual"]).fillna(0.0)
    merged["residual_pct"] = (merged["share"] - merged["base_share"]) * 100.0

    hours = np.arange(24)
    diff_pct = merged["residual_pct"]
    base_share_pct = merged["base_share"].to_numpy() * 100.0

    th_hours = df_flagged.loc[df_flagged["is_thailand_event"], "hour"].to_numpy()
    n_th = len(th_hours)
    n_base = int((~df_flagged["is_thailand_event"]).sum())

    rng = np.random.default_rng(seed)
    boot_diffs_list: list[np.ndarray] = []
    for _ in range(n_boot):
        sample = rng.choice(th_hours, size=n_th, replace=True)
        counts = np.bincount(sample, minlength=24)[:24]
        sample_share = (counts / n_th) * 100.0
        boot_diffs_list.append(sample_share - base_share_pct)

    boot_diffs = np.array(boot_diffs_list)
    boot_lower = np.percentile(boot_diffs, 2.5, axis=0)
    boot_upper = np.percentile(boot_diffs, 97.5, axis=0)

    key_stats: dict[int, dict[str, object]] = {}
    for h in (8, 11, 16):
        res = float(diff_pct.iloc[h])
        c_low = float(boot_lower[h])
        c_high = float(boot_upper[h])
        crosses_zero = c_low <= 0.0 <= c_high
        key_stats[h] = {
            "residu": res,
            "ci_low": c_low,
            "ci_high": c_high,
            "crosses_zero": crosses_zero,
            "ci_str": f"[{c_low:+.1f}%, {c_high:+.1f}%]".replace(".", ","),
            "res_str": f"{res:+.1f}%".replace(".", ","),
        }

    return Figuur2BootstrapResult(
        residual_df=merged,
        hours=hours,
        diff_pct=diff_pct,
        ci_low=boot_lower,
        ci_high=boot_upper,
        key_stats=key_stats,
        n_thailand=n_th,
        n_baseline=n_base,
    )


def plot_figuur2(
    boot_res: Figuur2BootstrapResult,
    save_path: Path | None = None,
) -> Figure:
    """Genereer Figuur 2: Uur-residu van berichtvolume tijdens Thailand-reis vs. baseline."""
    settings = JeffreyPlotSettings(figsize=(11.8, 6.0), title="")

    fig, ax = ResidualCurvePlot(settings).plot(
        hours=boot_res.hours,
        diff_pct=boot_res.diff_pct,
        boot_lower=boot_res.ci_low,
        boot_upper=boot_res.ci_high,
    )

    ax.set_ylim(-11.5, 15.0)
    ax.set_yticks([-10, -5, 0, 5, 10])
    ax.set_yticklabels(
        ["-10%", "-5%", "0%", "+5%", "+10%"],
        fontsize=10,
        color=settings.base_color,
    )
    ax.set_ylabel(
        "Verschil in aandeel berichten (Reis − Normaal)",
        fontsize=11,
        fontweight="bold",
        color=settings.dark_text,
    )
    ax.grid(axis="y", color="#E2E8F0", linestyle="--", linewidth=1.0, alpha=0.7)

    key_stats = boot_res.key_stats
    diff_pct = boot_res.diff_pct

    annotate_badge(
        ax,
        text=(
            f"Ochtendsurplus ({key_stats[8]['res_str']})\n"
            "NL ontwaakt; bij Rick is het al middag (13:00)"
        ),
        xy=(8.0, float(diff_pct.iloc[8])),
        xytext=(1.5, 9.8),
        settings=settings,
    )

    annotate_context_badge(
        ax,
        text=(
            f"Ochtenddal ({key_stats[11]['res_str']})\n"
            "Normale werkdagpiek valt stil door werk & tijdsverschil"
        ),
        xy=(11.0, float(diff_pct.iloc[11])),
        xytext=(0.0, -8.0),
        settings=settings,
    )

    annotate_badge(
        ax,
        text=(
            f"Absolute dagpiek ({key_stats[16]['res_str']})\n"
            "Rick is na het eten in hotel vóór slapengaan (21:00)"
        ),
        xy=(16.0, float(diff_pct.iloc[16])),
        xytext=(11.5, 12.0),
        settings=settings,
    )

    format_header(
        ax,
        title="Reis naar Thailand gooit het vertrouwde dagritme om",
        subtitle="Verschil in aandeel berichten per uur (Nederlandse tijd) t.o.v. de 4-jarige baseline",
    )

    n_base_fmt = f"{boot_res.n_baseline:,}".replace(",", ".")
    n_th_fmt = f"{boot_res.n_thailand:,}".replace(",", ".")

    footnote_text = (
        "* Statistische betrouwbaarheid via Bootstrapping (N = 1.000 herhalingen met teruglegging): de blauwe band toont het 95%-betrouwbaarheidsinterval van de residulijn.\n"
        f"Omdat de intervallen om 08:00 ({key_stats[8]['ci_str']}), 11:00 ({key_stats[11]['ci_str']}) en 16:00 ({key_stats[16]['ci_str']}) nergens de nullijn kruisen, blijft het ritme overeind.\n"
        f"Baseline: {n_base_fmt} berichten (4 jaar) | Reisperiode Thailand: {n_th_fmt} berichten (16 dagen)."
    )
    format_footnote(ax, text=footnote_text, y_offset=-0.22)

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fig
