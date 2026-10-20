"""scripts.plots - Centrale 'Serve'-laag visualisatie-engine (MADS-DAV).

INHOUDSOPGAVE:
=============
1. HUISSTIJL & PALET (DNA)
   - JeffreyPlotSettings : Paletkleuren, canvas-afmetingen en typografie
   - apply_dav_theme     : Tufte-stijl open spines en zachte as-lijnen

2. TYPOGRAFIE & ANNOTATIES (COMMUNICATIE)
   - format_header       : Schwabish 2-laags header (bold titel + context-subtitel)
   - format_footnote     : Methodologische verantwoording & steekproefgroottes
   - annotate_badge      : Callout-badge met pijl en afgerond tekstkader
   - annotate_callout    : Subtiele directe annotatiepijl zonder kader

3. SPECIALISTISCHE PLOTS & ASSEN
   - setup_dayparts_axis : 24-uurs X-as macro-indeling in 4 dagdelen
   - plot_residual_curve : Residu-analyse met baseline, surplus/deficiet en 95% CI

4. LESSON 2 CURSUSKLASSEN (HISTORISCH FUNDAMENT)
   - BarPlot             : Horizontale/verticale staafdiagrammen
   - BarPlotWithError    : Staafdiagram met error-bars
"""

from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import seaborn as sns
from goad_toolkit.visualizer import BasePlot, PlotSettings


# =============================================================================
# 1. HUISSTIJL & PALET (DNA)
# =============================================================================


@dataclass
class JeffreyPlotSettings(PlotSettings):
    """PlotSettings met het beproefde kleurenpalet en afmetingen uit 3.3 en 4.4."""

    base_color: str = "#4A5568"  # Leisteengrijs (neutrale context / Partner / baseline)
    highlight_color: str = "#C2410C"  # Terracotta oranje (pop-out / Student / event)
    accent_soft: str = "#FB923C"  # Zacht oranje (spillover / intervallen)
    partner_blue: str = (
        "#1E40AF"  # Klassiek marineblauw (Partner in vergelijkende lijndiagrammen)
    )
    dark_text: str = "#1A202C"  # Donker antraciet voor titels
    muted_text: str = "#718096"  # Gedimd grijs voor voetnoten en ticks
    line_color: str = "#CBD5E0"  # Rustige as- en gridlijnen
    figsize: tuple[int, int] = (9, 5)


def apply_dav_theme(ax):
    """Volledig Tufte-ontwerp: open spines en zachte as-lijnen conform 3.3 & 4.4."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E0")
    ax.spines["bottom"].set_color("#CBD5E0")
    ax.tick_params(colors="#718096", labelsize=9)
    return ax


# =============================================================================
# 2. TYPOGRAFIE & ANNOTATIES (COMMUNICATIE)
# =============================================================================


def format_header(ax, title: str, subtitle: str | None = None):
    """De beproefde 2-laags header: 13pt bold titel met 9pt cursieve context-subtitel."""
    ax.set_title(title, fontsize=13, fontweight="bold", pad=22, color="#1A202C")
    if subtitle:
        ax.text(
            0.0,
            1.02,
            subtitle,
            transform=ax.transAxes,
            fontsize=9.0,
            style="italic",
            color="#4A5568",
            va="bottom",
            ha="left",
        )
    return ax


def format_footnote(ax, text: str, y_offset: float = -0.22):
    """Methodologische verantwoording onder de as conform de inleverstandaard."""
    ax.text(
        0.0,
        y_offset,
        text,
        transform=ax.transAxes,
        fontsize=8.0,
        style="italic",
        color="#718096",
        va="top",
        ha="left",
    )
    return ax


def annotate_badge(
    ax,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    highlight: bool = True,
    settings: JeffreyPlotSettings | None = None,
    ha: str = "left",
):
    """Gerichte callout-badge met afgerond kader en pijl in DAV-huisstijl."""
    hl_color = settings.highlight_color if settings else "#C2410C"
    base_color = settings.base_color if settings else "#4A5568"
    line_color = settings.line_color if settings else "#CBD5E0"
    dark_color = settings.dark_text if settings else "#1A202C"

    if highlight:
        box_face = "#FFF7ED"
        box_edge = "#FDBA74"
        text_color = hl_color
        arrow_color = hl_color
    else:
        box_face = "#F7FAFC"
        box_edge = line_color
        text_color = dark_color
        arrow_color = base_color

    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        ha=ha,
        arrowprops={"arrowstyle": "->", "color": arrow_color, "lw": 1.5},
        fontsize=9.2,
        fontweight="bold",
        color=text_color,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": box_face,
            "edgecolor": box_edge,
            "lw": 1.2,
        },
        zorder=6,
    )
    return ax


def annotate_callout(
    ax,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    color: str = "#C2410C",
):
    """Directe annotatie met elegante pijl in huisstijlkleur (geen losse legenda nodig)."""
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        arrowprops={"arrowstyle": "->", "color": color, "lw": 1.1},
        fontsize=8.5,
        fontweight="bold",
        color=color,
    )
    return ax


# =============================================================================
# 3. SPECIALISTISCHE PLOTS & ASSEN
# =============================================================================


def setup_dayparts_axis(ax, settings: JeffreyPlotSettings | None = None):
    """Deelt een 24-uurs X-as macro-gewijs in 4 dagdelen conform Tufte."""
    base_color = settings.base_color if settings else "#4A5568"
    for split_hour in [6, 12, 18]:
        ax.axvline(split_hour, color="#E2E8F0", linestyle=":", linewidth=1.2, zorder=1)

    zone_mids = [3, 9, 15, 21]
    zone_labels = [
        "Nacht\n(00:00 – 06:00)",
        "Ochtend\n(06:00 – 12:00)",
        "Middag\n(12:00 – 18:00)",
        "Avond\n(18:00 – 24:00)",
    ]
    ax.set_xlim(-0.5, 23.5)
    ax.set_xticks(zone_mids)
    ax.set_xticklabels(zone_labels, fontsize=10, color=base_color, fontweight="bold")
    ax.tick_params(axis="x", length=0)
    return ax


def plot_residual_curve(
    ax,
    hours,
    diff_pct,
    boot_lower=None,
    boot_upper=None,
    settings: JeffreyPlotSettings | None = None,
):
    """Tekent een volledige residu-curve met nullijn, surplus/deficiet en bootstrap 95% CI."""
    base_color = settings.base_color if settings else "#4A5568"
    hl_color = settings.highlight_color if settings else "#C2410C"
    line_color = settings.line_color if settings else "#CBD5E0"

    # Nullijn (de normale baseline)
    ax.axhline(0, color=base_color, linestyle="-", linewidth=1.2, zorder=2)

    # Surplus (oranje) vs. Deficiet (leisteengrijs)
    ax.fill_between(
        hours,
        0,
        diff_pct,
        where=(diff_pct >= 0),
        interpolate=True,
        color="#FED7AA",
        alpha=0.40,
        zorder=2,
    )
    ax.fill_between(
        hours,
        0,
        diff_pct,
        where=(diff_pct < 0),
        interpolate=True,
        color=line_color,
        alpha=0.30,
        zorder=2,
    )

    # 95% Betrouwbaarheidsband (indien bootstrap meegegeven)
    if boot_lower is not None and boot_upper is not None:
        ax.fill_between(
            range(len(hours)),
            boot_lower,
            boot_upper,
            color="#2B6CB0",
            alpha=0.09,
            zorder=3,
            label="95% Betrouwbaarheidsband (1.000 bootstraps)",
        )
        ax.plot(
            range(len(hours)),
            boot_lower,
            color="#2B6CB0",
            linestyle="--",
            linewidth=0.7,
            alpha=0.25,
            zorder=3,
        )
        ax.plot(
            range(len(hours)),
            boot_upper,
            color="#2B6CB0",
            linestyle="--",
            linewidth=0.7,
            alpha=0.25,
            zorder=3,
        )

    # Werkelijke Residu-lijn
    ax.plot(
        hours,
        diff_pct,
        color="#2B6CB0",
        linewidth=2.4,
        marker="o",
        markersize=6.5,
        markerfacecolor="white",
        markeredgewidth=2,
        markeredgecolor="#2B6CB0",
        label="Residu",
        zorder=4,
    )

    # Geaccentueerde pieken (>= 5% surplus) en dalen (<= -5% deficiet)
    for h, val in zip(hours, diff_pct):
        if val >= 5.0:
            ax.plot(
                h,
                val,
                marker="o",
                markersize=7.5,
                markerfacecolor=hl_color,
                markeredgecolor="white",
                markeredgewidth=1.8,
                zorder=5,
            )
        elif val <= -5.0:
            ax.plot(
                h,
                val,
                marker="o",
                markersize=7.5,
                markerfacecolor=base_color,
                markeredgecolor="white",
                markeredgewidth=1.8,
                zorder=5,
            )

    return ax


# =============================================================================
# 4. LESSON 2 CURSUSKLASSEN (HISTORISCH FUNDAMENT)
# =============================================================================


class BarPlot(BasePlot):
    """A bar chart. All the styling lives in PlotSettings."""

    def build(self, data: pd.DataFrame, x: str, y: str, **kwargs):
        sns.barplot(data=data, x=x, y=y, ax=self.ax, **kwargs)
        return self.fig, self.ax


class BarPlotWithError(BasePlot):
    """A grouped bar chart carrying intervals that were computed elsewhere.

    `GroupedBarPlot` cannot do this: seaborn derives its intervals from raw
    observations, and these are already-summarised means with intervals of their own.

    Each bar is looked up by (category, hue level) rather than by position. Seaborn
    draws one container per hue level in `hue_order`, and the categories along the
    x-axis in tick order — so those two are what the lookup keys on, and the check
    turns a layout change into a failure rather than a silently misplaced error bar.

    Colour comes from the settings, following 02.2's grey-first rule: every hue
    level but the last is `settings.base_color`, the last — the one the plot is
    about — is `settings.highlight_color`. Pass `palette=` to override.
    """

    def build(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: str,
        error: str,
        hue_order: list[str],
        **kwargs,
    ):
        kwargs.setdefault(
            "palette",
            [self.settings.base_color] * (len(hue_order) - 1)
            + [self.settings.highlight_color],
        )
        sns.barplot(
            data=data, x=x, y=y, hue=hue, hue_order=hue_order, ax=self.ax, **kwargs
        )
        if self.ax is None:
            raise ValueError("create_figure() must run before build()")

        intervals = data.set_index([x, hue])[error]
        categories = [label.get_text() for label in self.ax.get_xticklabels()]
        if len(self.ax.containers) != len(hue_order):
            raise ValueError(
                f"seaborn drew {len(self.ax.containers)} containers for "
                f"{len(hue_order)} hue levels; the error bars would be misplaced"
            )

        for container, level in zip(self.ax.containers, hue_order):
            for patch, category in zip(container, categories):
                self.ax.errorbar(
                    patch.get_x() + patch.get_width() / 2,
                    patch.get_height(),
                    yerr=intervals[(category, level)],
                    fmt="none",
                    ecolor="black",
                    capsize=4,
                )

        self.ax.legend(loc="lower right", framealpha=1)
        return self.fig, self.ax
