"""Visuele huisstijl & BasePlot-architectuur: JeffreyPlotSettings, DAV-thema, headers en plotklassen."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from goad_toolkit.visualizer import BasePlot, PlotSettings
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from wa_analyzer.config import (
    COLOR_TEXT_MAIN,
    THEME_COLORS,
)


@dataclass
class JeffreyPlotSettings(PlotSettings):
    """PlotSettings met het beproefde kleurenpalet en afmetingen uit Les 2 t/m 7."""

    base_color: str = "#4A5568"  # Leisteengrijs (neutrale context / Partner / baseline)
    highlight_color: str = "#C2410C"  # Terracotta oranje (pop-out / Student / event)
    accent_soft: str = "#FB923C"  # Zacht oranje (spillover / intervallen)
    partner_blue: str = (
        "#1E40AF"  # Klassiek marineblauw (Partner in vergelijkende lijndiagrammen)
    )
    dark_text: str = "#1A202C"  # Donker antraciet voor titels
    muted_text: str = "#718096"  # Gedimd grijs voor voetnoten en ticks
    line_color: str = "#CBD5E0"  # Rustige as- en gridlijnen
    figsize: tuple[int | float, int | float] = (9, 5)  # type: ignore[assignment]


def apply_dav_theme(ax: Axes | None = None) -> Axes | None:
    """Volledig Tufte-ontwerp: open spines en zachte as-lijnen conform 3.3 & 4.4."""
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    if ax is not None:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#CBD5E0")
        ax.spines["bottom"].set_color("#CBD5E0")
        ax.tick_params(colors="#718096", labelsize=9)
    return ax


def format_header(
    ax: Axes,
    title: str,
    subtitle: str | None = None,
) -> Axes:
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


def format_footnote(
    ax: Axes,
    text: str,
    y_offset: float = -0.22,
) -> Axes:
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
    ax: Axes,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    settings: JeffreyPlotSettings | None = None,
    ha: str = "left",
) -> Axes:
    """Gerichte pop-out callout-badge in terracotta huisstijlkleur."""
    hl_color = settings.highlight_color if settings else "#C2410C"
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        ha=ha,
        arrowprops={"arrowstyle": "->", "color": hl_color, "lw": 1.5},
        fontsize=9.2,
        fontweight="bold",
        color=hl_color,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#FFF7ED",
            "edgecolor": "#FDBA74",
            "lw": 1.2,
        },
        zorder=6,
    )
    return ax


def annotate_context_badge(
    ax: Axes,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    settings: JeffreyPlotSettings | None = None,
    ha: str = "left",
) -> Axes:
    """Neutrale context-badge in leisteengrijs voor baseline-verantwoording."""
    base_color = settings.base_color if settings else "#4A5568"
    line_color = settings.line_color if settings else "#CBD5E0"
    dark_color = settings.dark_text if settings else "#1A202C"
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        ha=ha,
        arrowprops={"arrowstyle": "->", "color": base_color, "lw": 1.5},
        fontsize=9.2,
        fontweight="bold",
        color=dark_color,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#F7FAFC",
            "edgecolor": line_color,
            "lw": 1.2,
        },
        zorder=6,
    )
    return ax


def annotate_callout(
    ax: Axes,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    color: str = "#C2410C",
) -> Axes:
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


def setup_dayparts_axis(
    ax: Axes,
    settings: JeffreyPlotSettings | None = None,
) -> Axes:
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
    ax: Axes,
    hours: np.ndarray,
    diff_pct: pd.Series | np.ndarray,
    boot_lower: np.ndarray | None = None,
    boot_upper: np.ndarray | None = None,
    settings: JeffreyPlotSettings | None = None,
) -> Axes:
    """Tekent een volledige residu-curve met nullijn, surplus/deficiet en bootstrap 95% CI."""
    base_color = settings.base_color if settings else "#4A5568"
    hl_color = settings.highlight_color if settings else "#C2410C"
    line_color = settings.line_color if settings else "#CBD5E0"

    ax.axhline(0, color=base_color, linestyle="-", linewidth=1.2, zorder=2)

    ax.fill_between(
        hours,
        0,
        diff_pct,
        where=np.asarray(diff_pct >= 0, dtype=bool).tolist(),
        interpolate=True,
        color="#FED7AA",
        alpha=0.40,
        zorder=2,
    )
    ax.fill_between(
        hours,
        0,
        diff_pct,
        where=np.asarray(diff_pct < 0, dtype=bool).tolist(),
        interpolate=True,
        color=line_color,
        alpha=0.30,
        zorder=2,
    )

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

    for h, val in zip(hours, diff_pct):
        if float(val) >= 5.0:
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
        elif float(val) <= -5.0:
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


class ResidualCurvePlot(BasePlot):
    """Herbruikbare BasePlot-klasse voor Figuur 2 (Uur-residu met 95% Bootstrap CI)."""

    def build(
        self,
        hours: np.ndarray,
        diff_pct: pd.Series | np.ndarray,
        boot_lower: np.ndarray | None = None,
        boot_upper: np.ndarray | None = None,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
        cfg = (
            self.settings
            if isinstance(self.settings, JeffreyPlotSettings)
            else JeffreyPlotSettings()
        )
        apply_dav_theme(self.ax)
        setup_dayparts_axis(self.ax, cfg)
        plot_residual_curve(
            self.ax,
            hours=hours,
            diff_pct=diff_pct,
            boot_lower=boot_lower,
            boot_upper=boot_upper,
            settings=cfg,
        )
        return self.fig, self.ax


class NegativeBinomialPlot(BasePlot):
    """Herbruikbare BasePlot-klasse voor Figuur 3 (Kansdichtheid & nbinom-verdelingscurven)."""

    def build(
        self,
        base_messages: pd.Series | np.ndarray,
        th_messages: pd.Series | np.ndarray,
        x_support: np.ndarray,
        y_base: np.ndarray,
        y_th: np.ndarray,
        bins: np.ndarray,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
        cfg = (
            self.settings
            if isinstance(self.settings, JeffreyPlotSettings)
            else JeffreyPlotSettings()
        )
        apply_dav_theme(self.ax)

        self.ax.hist(
            base_messages,
            bins=bins.tolist(),
            density=True,
            color="#CBD5E0",
            alpha=0.55,
            edgecolor="white",
            zorder=2,
            label="Thuisbasis (werkelijk)",
        )
        self.ax.hist(
            th_messages,
            bins=bins.tolist(),
            density=True,
            color="#FDBA74",
            alpha=0.60,
            edgecolor="white",
            zorder=2,
            label="Thailand (werkelijk)",
        )
        self.ax.plot(
            x_support,
            y_base,
            color=cfg.base_color,
            linewidth=3.2,
            zorder=3,
            label="Fit: Thuisbasis",
        )
        self.ax.plot(
            x_support,
            y_th,
            color=cfg.highlight_color,
            linewidth=3.2,
            zorder=3,
            label="Fit: Thailand",
        )
        return self.fig, self.ax


class PiecewiseRegPlot(BasePlot):
    """Herbruikbare BasePlot-klasse voor Figuur 4 (Aaneengesloten 2-fasen regressie)."""

    def build(
        self,
        x_grid: np.ndarray,
        y_pred_j: np.ndarray,
        y_pred_r: np.ndarray,
        binned_df: pd.DataFrame,
        knot: float = 10.5,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
        cfg = (
            self.settings
            if isinstance(self.settings, JeffreyPlotSettings)
            else JeffreyPlotSettings()
        )
        apply_dav_theme(self.ax)

        color_jeffrey = cfg.highlight_color
        color_rick = cfg.partner_blue

        self.ax.axvspan(0.5, knot, color="#F8FAFC", alpha=0.9, zorder=0)
        self.ax.axvline(knot, color="#CBD5E0", linestyle=":", linewidth=1.2, zorder=2)

        self.ax.plot(
            x_grid,
            y_pred_j,
            color=color_jeffrey,
            linewidth=3.4,
            zorder=4,
            label="Jeffrey",
        )
        self.ax.plot(
            x_grid,
            y_pred_r,
            color=color_rick,
            linewidth=3.4,
            zorder=4,
            label="Rick",
        )

        b_jeffrey = binned_df[binned_df["author"] == "Student"]
        b_rick = binned_df[binned_df["author"] == "Partner"]
        self.ax.scatter(
            b_jeffrey["med_words"],
            b_jeffrey["med_log"],
            color=color_jeffrey,
            s=45,
            alpha=0.55,
            zorder=3,
        )
        self.ax.scatter(
            b_rick["med_words"],
            b_rick["med_log"],
            color=color_rick,
            s=45,
            alpha=0.55,
            zorder=3,
        )
        return self.fig, self.ax


class SemanticPCAPlot(BasePlot):
    """Herbruikbare BasePlot-klasse voor Figuur 5 (2D PCA van 384D Hugging Face embeddings)."""

    def build(
        self,
        units: pd.DataFrame,
        cx_food: float,
        cy_food: float,
        cx_work: float,
        cy_work: float,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
        apply_dav_theme(self.ax)

        self.ax.scatter(
            units.loc[units["theme"] == "Overig", "pca_x"],
            units.loc[units["theme"] == "Overig", "pca_y"],
            color="#CBD5E1",
            alpha=0.18,
            s=16,
            edgecolors="none",
            zorder=2,
        )
        self.ax.scatter(
            units.loc[units["theme"] == "Huisdieren", "pca_x"],
            units.loc[units["theme"] == "Huisdieren", "pca_y"],
            color="#94A3B8",
            alpha=0.25,
            s=20,
            edgecolors="none",
            zorder=2,
        )
        self.ax.scatter(
            units.loc[units["theme"] == "Zorg & Familie", "pca_x"],
            units.loc[units["theme"] == "Zorg & Familie", "pca_y"],
            color="#94A3B8",
            alpha=0.25,
            s=20,
            edgecolors="none",
            zorder=2,
        )

        food_jeffrey = units[
            (units["theme"] == "Huishouden en Voeding") & (units["author"] == "Student")
        ]
        food_rick = units[
            (units["theme"] == "Huishouden en Voeding") & (units["author"] == "Partner")
        ]
        self.ax.scatter(
            food_jeffrey["pca_x"],
            food_jeffrey["pca_y"],
            marker="o",
            color="#D97706",
            alpha=0.35,
            s=28,
            edgecolors="none",
            zorder=3,
        )
        self.ax.scatter(
            food_rick["pca_x"],
            food_rick["pca_y"],
            marker="^",
            color="#D97706",
            alpha=0.35,
            s=30,
            edgecolors="none",
            zorder=3,
        )

        work_jeffrey = units[
            (units["theme"] == "Werk en Mobiliteit") & (units["author"] == "Student")
        ]
        work_rick = units[
            (units["theme"] == "Werk en Mobiliteit") & (units["author"] == "Partner")
        ]
        self.ax.scatter(
            work_jeffrey["pca_x"],
            work_jeffrey["pca_y"],
            marker="o",
            color="#2563EB",
            alpha=0.35,
            s=28,
            edgecolors="none",
            zorder=3,
        )
        self.ax.scatter(
            work_rick["pca_x"],
            work_rick["pca_y"],
            marker="^",
            color="#2563EB",
            alpha=0.35,
            s=30,
            edgecolors="none",
            zorder=3,
        )

        self.ax.scatter(
            cx_food,
            cy_food,
            s=120,
            facecolor="#FFFFFF",
            edgecolor="#D97706",
            linewidth=2.4,
            zorder=5,
        )
        self.ax.scatter(cx_food, cy_food, s=36, color="#D97706", zorder=6)

        self.ax.scatter(
            cx_work,
            cy_work,
            s=120,
            facecolor="#FFFFFF",
            edgecolor="#2563EB",
            linewidth=2.4,
            zorder=5,
        )
        self.ax.scatter(cx_work, cy_work, s=36, color="#2563EB", zorder=6)
        return self.fig, self.ax


class TopicNetworkPlot(BasePlot):
    """Herbruikbare BasePlot-klasse voor Figuur 6 (Co-occurrencenetwerk van 16 subthema's)."""

    def build(
        self,
        graph: nx.Graph,
        pos: dict[str, tuple[float, float]],
        node_metadata: dict[str, tuple[str, str]],
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
        apply_dav_theme(self.ax)

        max_weight = max((d["weight"] for _, _, d in graph.edges(data=True)), default=1)
        for u, v, data in graph.edges(data=True):
            w = int(data["weight"])
            if w < 5:
                continue
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            same_domain = node_metadata[u][1] == node_metadata[v][1]
            lw = 0.8 + 4.8 * (w / max_weight)
            alpha = 0.55 if w >= 25 else 0.22
            edge_color = (
                THEME_COLORS[node_metadata[u][1]]
                if same_domain
                else ("#2C3E50" if w >= 25 else "#95A5A6")
            )
            self.ax.plot(
                [x0, x1],
                [y0, y1],
                color=edge_color,
                linewidth=lw,
                alpha=alpha,
                linestyle="-" if same_domain or w >= 25 else "--",
                zorder=2 if w < 25 else 3,
            )

        for node, data in graph.nodes(data=True):
            nx_x, nx_y = pos[node]
            domain = str(data["domain"])
            freq = int(data["sessions_count"])
            node_size = 240.0 + freq * 3.8
            color = THEME_COLORS[domain]
            self.ax.scatter(
                nx_x,
                nx_y,
                s=node_size,
                color=color,
                edgecolor="white",
                linewidth=2.2,
                zorder=5,
            )
            self.ax.text(
                nx_x,
                nx_y - 0.11,
                f"{data['label']}\n(n={freq})",
                ha="center",
                va="top",
                fontsize=8.5,
                fontweight="bold" if freq >= 100 else "normal",
                color=COLOR_TEXT_MAIN,
                bbox={
                    "boxstyle": "round,pad=0.2",
                    "facecolor": "white",
                    "edgecolor": "none",
                    "alpha": 0.85,
                },
                zorder=6,
            )
        return self.fig, self.ax


class BarPlot(BasePlot):
    """Staafdiagram gebouwd op `goad_toolkit.visualizer.BasePlot`."""

    def build(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        *_args: object,
        **kwargs: object,
    ) -> tuple[Figure | None, Axes | None]:
        sns.barplot(data=data, x=x, y=y, ax=self.ax, **kwargs)  # type: ignore[arg-type]
        return self.fig, self.ax


class BarPlotWithError(BasePlot):
    """Staafdiagram met foutbalken (errorbars) gebouwd op `goad_toolkit.visualizer.BasePlot`."""

    def build(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: str,
        error: str,
        hue_order: list[str],
        *_args: object,
        **kwargs: object,
    ) -> tuple[Figure | None, Axes | None]:
        kwargs.setdefault(
            "palette",
            [self.settings.base_color] * (len(hue_order) - 1)
            + [self.settings.highlight_color],
        )
        sns.barplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            hue_order=hue_order,
            ax=self.ax,
            **kwargs,  # type: ignore[arg-type]
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
            for patch, category in zip(container, categories):  # type: ignore[arg-type]
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
