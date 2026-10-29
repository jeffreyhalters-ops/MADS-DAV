"""Figuur 1 (Les 1 & 2): Reactietijd per dagdeel (Barbell plot & Mann-Whitney U-toets)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from goad_toolkit.visualizer import BarbellPlot
from matplotlib.figure import Figure
from scipy.stats import mannwhitneyu

from wa_analyzer.visualizer import (
    JeffreyPlotSettings,
    apply_dav_theme,
    format_footnote,
    format_header,
)


@dataclass(frozen=True)
class Figuur1Stats:
    """Statistische resultaten voor Figuur 1 (Barbell-vergelijking per dagdeel)."""

    summary_df: pd.DataFrame
    counts_per_dp: dict[str, int]
    n_replies: int
    total_messages: int
    u_stat_evening: float
    p_val_evening: float
    toevalskans_pct: float
    q75_student: float
    q75_partner: float
    med_student_evening: float
    med_partner_evening: float
    n_student_evening: int
    n_partner_evening: int


def fit_figuur1_stats(df_chat: pd.DataFrame) -> Figuur1Stats:
    """Bereken de mediane reactietijd per dagdeel en toets het avondverschil (Mann-Whitney U)."""
    valid = df_chat[
        df_chat["response_time_min"].notna()
        & (df_chat["response_time_min"] > 0.0)
        & (df_chat["response_time_min"] <= 480.0)
    ].copy()

    total_replies = len(valid)
    counts_series = valid.groupby("day_part", observed=True).size()
    counts_per_dp = {str(k): int(v) for k, v in counts_series.items()}

    agg = (
        valid.groupby(["day_part", "author"], observed=True)["response_time_min"]
        .median()
        .reset_index(name="median_min")
    )

    day_order = ["Avond", "Middag", "Ochtend"]
    wide = (
        agg.pivot(index="day_part", columns="author", values="median_min")
        .reindex(day_order)
        .reset_index()
    )
    wide["gap"] = (wide["Student"] - wide["Partner"]).round(2)

    avond_student = valid[
        (valid["day_part"] == "Avond") & (valid["author"] == "Student")
    ]["response_time_min"]
    avond_partner = valid[
        (valid["day_part"] == "Avond") & (valid["author"] == "Partner")
    ]["response_time_min"]

    u_stat, p_val = mannwhitneyu(avond_student, avond_partner, alternative="two-sided")

    return Figuur1Stats(
        summary_df=wide,
        counts_per_dp=counts_per_dp,
        n_replies=total_replies,
        total_messages=len(df_chat),
        u_stat_evening=float(u_stat),
        p_val_evening=float(p_val),
        toevalskans_pct=float(p_val * 100.0),
        q75_student=float(avond_student.quantile(0.75)),
        q75_partner=float(avond_partner.quantile(0.75)),
        med_student_evening=float(avond_student.median()),
        med_partner_evening=float(avond_partner.median()),
        n_student_evening=len(avond_student),
        n_partner_evening=len(avond_partner),
    )


def plot_figuur1(
    stats_res: Figuur1Stats,
    save_path: Path | None = None,
) -> Figure:
    """Genereer Figuur 1: Barbell-plot van mediane reactietijd per dagdeel."""
    wide = stats_res.summary_df
    p_str = f"p = {stats_res.p_val_evening:.3f}".replace(".", ",")
    toeval_str = f"{stats_res.toevalskans_pct:.1f}%".replace(".", ",")

    settings = JeffreyPlotSettings(
        figsize=(8.5, 4.8),
        xlabel="Mediaan reactietijd (minuten)",
        ylabel="",
    )

    fig, ax = BarbellPlot(settings).plot(
        data=wide,
        category="day_part",
        start="Partner",
        end="Student",
        start_label="Partner",
        end_label="Student",
        start_color=settings.base_color,
        end_color=settings.highlight_color,
        line_color=settings.line_color,
        markersize=95,
    )

    apply_dav_theme(ax)

    format_header(
        ax,
        title="Jeffrey reageert beduidend langzamer dan zijn partner",
        subtitle=(
            "Overdag zorgen docenttaken voor vertraging, maar 's avonds is de responskloof "
            "maximaal doordat de telefoon vaker blijft liggen"
        ),
    )

    for idx, (_, row) in enumerate(wide.iterrows()):
        idx_f = float(idx)
        p_val_lbl = f"{row['Partner']:.1f} min".replace(".", ",")
        s_val_lbl = f"{row['Student']:.1f} min".replace(".", ",")

        ax.text(
            float(row["Partner"]) - 0.14,
            idx_f,
            p_val_lbl,
            va="center",
            ha="right",
            fontsize=9.5,
            color=settings.base_color,
        )
        ax.text(
            float(row["Student"]) + 0.14,
            idx_f,
            s_val_lbl,
            va="center",
            ha="left",
            fontsize=9.5,
            fontweight="bold",
            color=settings.highlight_color,
        )

        if row["day_part"] == "Avond":
            gap_lbl = f"kloof: {row['gap']:.1f} min* ({p_str})".replace(".", ",")
        else:
            gap_lbl = f"kloof: {row['gap']:.1f} min".replace(".", ",")

        mid_x = (float(row["Partner"]) + float(row["Student"])) / 2.0
        y_pos = idx_f - 0.10 if row["day_part"] == "Ochtend" else idx_f + 0.08
        v_align = "top" if row["day_part"] == "Ochtend" else "bottom"

        ax.text(
            mid_x,
            y_pos,
            gap_lbl,
            va=v_align,
            ha="center",
            fontsize=8,
            style="italic",
            color=settings.muted_text,
        )

    ax.set_xlim(-0.6, 4.4)

    n_ochtend = f"{stats_res.counts_per_dp.get('Ochtend', 0):,}".replace(",", ".")
    n_middag = f"{stats_res.counts_per_dp.get('Middag', 0):,}".replace(",", ".")
    n_avond = f"{stats_res.counts_per_dp.get('Avond', 0):,}".replace(",", ".")
    n_tot = f"{stats_res.n_replies:,}".replace(",", ".")
    total_chat_messages = f"{stats_res.total_messages:,}".replace(",", ".")

    footnote_text = (
        f"Noot: Mediaan berekend over {n_tot} directe reacties (wisseling van auteur, binnen dezelfde dag en max. 8 uur) uit {total_chat_messages} berichten:\n"
        f"Ochtend (n={n_ochtend}), Middag (n={n_middag}), Avond (n={n_avond}).\n"
        f"* Het avondverschil is statistisch significant getoetst via Mann-Whitney U ({p_str}, toevalskans {toeval_str}).\n"
        f"  Bij Jeffrey blijft 's avonds 25% van de berichten langer dan {stats_res.q75_student:.0f} minuten liggen (tegenover {stats_res.q75_partner:.0f} min bij Rick)."
    )

    format_footnote(ax, text=footnote_text, y_offset=-0.25)

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fig
