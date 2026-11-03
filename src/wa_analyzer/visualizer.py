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
    figsize: tuple[int, int] = (9, 5)


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

        # Contextuele achtergrondthema's (gedimd)
        bg_styles: dict[str, tuple[str, float, int]] = {
            "Overig": ("#CBD5E1", 0.18, 16),
            "Huisdieren": ("#94A3B8", 0.25, 20),
            "Zorg & Familie": ("#94A3B8", 0.25, 20),
        }
        for theme_name, (color, alpha, s) in bg_styles.items():
            pts = units[units["theme"] == theme_name]
            self.ax.scatter(
                pts["pca_x"],
                pts["pca_y"],
                color=color,
                alpha=alpha,
                s=s,
                edgecolors="none",
                zorder=2,
            )

        # Focus-kernthema's per auteur (oranje voor huishouden, blauw voor werk)
        theme_colors: dict[str, str] = {
            "Huishouden en Voeding": "#D97706",
            "Werk en Mobiliteit": "#2563EB",
        }
        author_markers: dict[str, tuple[str, int]] = {
            "Student": ("o", 28),
            "Partner": ("^", 30),
        }
        for theme_name, t_color in theme_colors.items():
            for author_name, (marker, size) in author_markers.items():
                pts = units[
                    (units["theme"] == theme_name) & (units["author"] == author_name)
                ]
                self.ax.scatter(
                    pts["pca_x"],
                    pts["pca_y"],
                    marker=marker,
                    color=t_color,
                    alpha=0.35,
                    s=size,
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


class StylometryTimelinePlot(BasePlot):
    """2x2 visualisatie van de 2D PCA schrijfstijl-vectorruimte per kalenderjaar via BasePlot."""

    def __init__(
        self,
        settings: PlotSettings | None = None,
        n_plots: int | None = 4,
    ) -> None:
        if settings is None:
            settings = JeffreyPlotSettings(
                figsize=(12, 11.5),
                max_cols=2,
                sharex=True,
                sharey=True,
                title="",
            )
        super().__init__(settings=settings, n_plots=n_plots)

    def build(
        self,
        df: pd.DataFrame,
        deltas: pd.DataFrame | dict[int, float] | None = None,
        years: list[int] | None = None,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        active_years = years if years is not None else [2022, 2023, 2024, 2025]
        self.fig, axes_list = self.create_figure(n_plots=len(active_years))
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")

        deltas_dict: dict[int, float] = {}
        if isinstance(deltas, pd.DataFrame):
            deltas_dict = dict(
                zip(deltas["year"].astype(int), deltas["delta"].astype(float))
            )
        elif isinstance(deltas, dict):
            deltas_dict = deltas

        self.fig.set_layout_engine(None)
        self.fig.subplots_adjust(
            top=0.84, bottom=0.19, left=0.10, right=0.95, hspace=0.18, wspace=0.12
        )

        c_jeff = "#C2410C"  # Terracotta oranje
        c_rick_fill = "#3B82F6"  # Zacht kobaltblauw voor de hoogtelijnen
        c_rick_node = "#1E3A8A"  # Diep marineblauw voor de centroid

        for i, yr in enumerate(active_years):
            ax = axes_list[i]
            apply_dav_theme(ax)
            ax.axhline(0, color="#E2E8F0", linestyle="-", linewidth=1.0, zorder=1)
            ax.axvline(0, color="#E2E8F0", linestyle="-", linewidth=1.0, zorder=1)

            sub = df[df["year"] == yr]
            p_pts = sub[sub["author"] == "Partner"]
            s_pts = sub[sub["author"] == "Student"]

            # Continue benadering via Hoogtelijnen (KDE-contouren) i.p.v. losse stipjes
            if len(p_pts) >= 5:
                sns.kdeplot(
                    data=p_pts,
                    x="pca_x",
                    y="pca_y",
                    ax=ax,
                    fill=True,
                    levels=[0.20, 0.50, 0.80, 1.0],
                    color=c_rick_fill,
                    alpha=0.20,
                    thresh=0.20,
                    zorder=2,
                )
                sns.kdeplot(
                    data=p_pts,
                    x="pca_x",
                    y="pca_y",
                    ax=ax,
                    fill=False,
                    levels=[0.20, 0.50, 0.80],
                    color=c_rick_fill,
                    linewidths=1.0,
                    alpha=0.45,
                    zorder=2,
                )

            if len(s_pts) >= 5:
                sns.kdeplot(
                    data=s_pts,
                    x="pca_x",
                    y="pca_y",
                    ax=ax,
                    fill=True,
                    levels=[0.20, 0.50, 0.80, 1.0],
                    color=c_jeff,
                    alpha=0.20,
                    thresh=0.20,
                    zorder=3,
                )
                sns.kdeplot(
                    data=s_pts,
                    x="pca_x",
                    y="pca_y",
                    ax=ax,
                    fill=False,
                    levels=[0.20, 0.50, 0.80],
                    color=c_jeff,
                    linewidths=1.0,
                    alpha=0.45,
                    zorder=3,
                )

            # Verwijder automatische Seaborn as-labels ('pca_x' / 'pca_y') op de deelvlakken
            ax.set_xlabel("")
            ax.set_ylabel("")

            # Zwaartepunten & Stijlafstand (Δ)
            cx_j, cy_j = float(s_pts["pca_x"].mean()), float(s_pts["pca_y"].mean())
            cx_r, cy_r = float(p_pts["pca_x"].mean()), float(p_pts["pca_y"].mean())
            dist = (
                deltas_dict[yr]
                if yr in deltas_dict
                else float(np.sqrt((cx_j - cx_r) ** 2 + (cy_j - cy_r) ** 2))
            )

            is_focus_year = yr in (2024, 2025)
            ax.plot(
                [cx_j, cx_r],
                [cy_j, cy_r],
                color="#0F172A" if is_focus_year else "#475569",
                linestyle="-",
                linewidth=2.8 if is_focus_year else 2.0,
                zorder=5,
            )

            # Centroid Rick (grote stip met witte rand)
            ax.scatter(
                [cx_r],
                [cy_r],
                s=195,
                color=c_rick_node,
                edgecolor="white",
                linewidth=2.5,
                zorder=6,
            )

            # Centroid Jeffrey (grote stip met witte rand)
            ax.scatter(
                [cx_j],
                [cy_j],
                s=195,
                color=c_jeff,
                edgecolor="white",
                linewidth=2.5,
                zorder=6,
            )

            # Directe Δ-badge op de verbindingslijn
            mx = (cx_j + cx_r) / 2.0
            my = (cy_j + cy_r) / 2.0
            if yr == 2025:
                mx += 0.95  # Naast de korte verbindingslijn zodat beide centroids 100% vrij zichtbaar blijven

            dist_str = f"Δ = {dist:.2f}".replace(".", ",")
            if yr == 2024:
                dist_str += " (piek)"
            elif yr == 2025:
                dist_str += " (convergentie)"

            ax.text(
                mx,
                my,
                dist_str,
                ha="center",
                va="center",
                fontsize=9.2 if is_focus_year else 8.6,
                fontweight="bold",
                color="#FFFFFF" if yr == 2025 else "#0F172A",
                bbox={
                    "boxstyle": "round,pad=0.28",
                    "facecolor": "#C2410C"
                    if yr == 2025
                    else ("#FEF3C7" if yr == 2024 else "#F8FAFC"),
                    "edgecolor": "#9A3412"
                    if yr == 2025
                    else ("#D97706" if yr == 2024 else "#CBD5E1"),
                    "lw": 1.2,
                    "alpha": 0.96,
                },
                zorder=7,
            )

            # Rustig jaartal linksboven in het vlak (geen drukke paneeltitels)
            ax.text(
                0.05,
                0.92,
                str(yr),
                transform=ax.transAxes,
                fontsize=14,
                fontweight="bold",
                color="#1E293B",
                va="top",
                ha="left",
                zorder=7,
            )

            # Subtiele eenmalige directe naam-annotatie in het eerste paneel (2022)
            if i == 0:
                ax.text(
                    cx_r + 0.22,
                    cy_r + 0.18,
                    "Rick",
                    fontsize=9.2,
                    fontweight="bold",
                    color=c_rick_node,
                    ha="left",
                    va="bottom",
                    zorder=7,
                )
                ax.text(
                    cx_j + 0.22,
                    cy_j - 0.18,
                    "Jeffrey",
                    fontsize=9.2,
                    fontweight="bold",
                    color=c_jeff,
                    ha="left",
                    va="top",
                    zorder=7,
                )

            ax.set_xlim(-3.2, 3.8)
            ax.set_ylim(-2.8, 3.2)

        # Centrale aslabels (1 strakke regel per as voor minder clutter)
        self.fig.supylabel(
            "← Veel komma's & bijzinnen   |   Zinsbouw & Expressie (PC2: 12,4%)   |   Punten & smileys →",
            fontsize=9.5,
            fontweight="bold",
            color="#1A202C",
            x=0.035,
        )

        self.fig.supxlabel(
            "← Korte reacties ('ok', 'top')   |   Woordlengte & Detail (PC1: 24,5%)   |   Lange woorden & cijfers →",
            fontsize=9.5,
            fontweight="bold",
            color="#1A202C",
            y=0.115,
        )

        # Schwabish Header met extra leeswijzer-regel in de subtitel (zodat een losse legenda-box overbodig is)
        self.fig.text(
            0.08,
            0.955,
            "Van eigen gewoontes naar een gedeelde taal: na een piek in 2024 trekt onze schrijfstijl in 2025 naar elkaar toe",
            fontsize=12.4,
            fontweight="bold",
            color="#1A202C",
            ha="left",
            va="bottom",
        )

        subtitle = (
            "In de eerste jaren schommelt het verschil in zinsbouw en woordkeuze (met een piek in afstand in 2024), "
            "maar in 2025 halveert het stijlverschil (Δ van 1,59 naar 0,63) en ontstaat een gezamenlijke toon.\n"
            "Leeswijzer: Grote stippen tonen de jaarlijkse centroids van Jeffrey (oranje) en Rick (blauw) met de stijlafstand (Δ) ertussen; "
            "de hoogtelijnen (20%–80% KDE-dichtheid) tonen de spreiding."
        )
        self.fig.text(
            0.08,
            0.942,
            subtitle,
            fontsize=8.9,
            style="italic",
            color="#4A5568",
            ha="left",
            va="top",
            linespacing=1.35,
        )

        # Methodologische voetnoot onderaan
        footnote = (
            f"* Methodologie & Verantwoording (100% data-dekking, complete kalenderjaren 2022–2025; 2026 uitgesloten wegens incompleetheid):\n"
            f"  Vaste tekstfragmenten van 600 tekens (N = {len(df)}), gescoord op 13 stijlkenmerken en gestandaardiseerd met StandardScaler (z-scores).\n"
            "  Centrale 2D PCA verklaart 36,9% van de totale variantie (PC1: 24,5%, PC2: 12,4%; eigenwaarden λ1 = 3,19, λ2 = 1,62).\n"
            "  Interne structuur: 1-NN cross-validation baseline = 68,9% (kansniveau = 50,0%) | Silhouette = 0,038 (geschudde nulcontrole = -0,002).\n"
            f"  Stijlafstand tussen zwaartepunten (Δ): 2022: {deltas_dict.get(2022, 1.45):.2f} | 2023: {deltas_dict.get(2023, 1.32):.2f} | 2024: {deltas_dict.get(2024, 1.59):.2f} | 2025: {deltas_dict.get(2025, 0.63):.2f} (sterke taalconvergentie in 2025)."
        )
        self.fig.text(
            0.08,
            0.015,
            footnote,
            fontsize=7.8,
            color="#4A5568",
            style="italic",
            va="bottom",
            ha="left",
            linespacing=1.3,
        )

        return self.fig, self.ax


class ConceptNetworkPlot(BasePlot):
    """Gewogen concept-netwerkgraaf met instelbare edge-drempel via BasePlot."""

    def __init__(
        self,
        settings: PlotSettings | None = None,
        n_plots: int | None = 1,
    ) -> None:
        if settings is None:
            settings = JeffreyPlotSettings(figsize=(13.5, 10.5), title="")
        super().__init__(settings=settings, n_plots=n_plots)

    def build(
        self,
        graph: nx.Graph,
        min_edge_weight: int = 15,
        highlight_weight: int = 35,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            self.create_figure()
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must initialize self.fig and self.ax")

        from matplotlib.lines import Line2D
        from matplotlib.patches import Circle, FancyArrowPatch
        from wa_analyzer.features.concept_graph import THEME_COLORS_4

        self.fig.patch.set_facecolor("white")
        self.ax.set_facecolor("white")
        self.ax.axis("off")

        # Handmatig verfijnde, deterministische 2D-posities:
        # 'thuis', 'eten & koken' en 'Nusa & Indy' in de centrale driehoek,
        # met de 4 leefwerelden organisch gegroepeerd zonder tekst-overlap.
        pos: dict[str, tuple[float, float]] = {
            # Voeding & Huishouden (Links / Centrum-Links)
            "thuis": (-0.18, 0.16),
            "eten & koken": (-0.20, -0.26),
            "horeca": (-0.75, -0.45),
            "sporten": (-0.78, -0.05),
            # Huisdieren (Onder / Rechts-Onder)
            "Nusa & Indy": (0.25, -0.28),
            "uitlaten": (0.04, -0.74),
            "dierenarts": (0.50, -0.52),
            "eten honden": (0.50, -0.68),
            # Werk & Mobiliteit (Links-Boven / Boven)
            "werken algemeen": (-0.28, 0.65),
            "vervoersmiddelen": (0.22, 0.68),
            "Avans": (-0.76, 0.52),
            "Rabobank & Gemeente": (-0.78, 0.84),
            # Zorg & Familie (Rechts / Rechts-Boven)
            "onze ouders": (0.58, 0.22),
            "medisch & zorg": (0.72, -0.14),
            "familie": (0.82, 0.56),
            "Feesten": (0.88, 0.84),
        }

        # Bereken totale node-strength (op het volledige netwerk >= 3) en actieve graad (>= min_edge_weight)
        node_strength: dict[str, int] = {}
        active_degree: dict[str, int] = dict.fromkeys(graph.nodes(), 0)
        for u in graph.nodes():
            node_strength[u] = sum(
                int(d.get("weight", 0)) for _, _, d in graph.edges(u, data=True)
            )

        filtered_edges: list[tuple[str, str, int]] = []
        for u, v, d in graph.edges(data=True):
            w = int(d.get("weight", 0))
            if w >= min_edge_weight:
                filtered_edges.append((u, v, w))
                active_degree[u] += 1
                active_degree[v] += 1

        # Sorteer edges zodat de zwaarste lijnen en labels bovenop liggen
        filtered_edges.sort(key=lambda item: item[2])
        max_w = max((w for _, _, w in filtered_edges), default=125)

        # 1. Subtiele achtergrond-halo voor de centrale 'keukentafel'-driehoek
        hub_circle = Circle(
            (-0.04, -0.12),
            0.44,
            facecolor="#FFFBEB",
            edgecolor="#FDE68A",
            linewidth=1.5,
            linestyle="--",
            alpha=0.65,
            zorder=1,
        )
        self.ax.add_patch(hub_circle)
        self.ax.text(
            0.00,
            -0.38,
            "Dagelijkse spil\n('keukentafel')",
            ha="center",
            va="center",
            fontsize=8.5,
            fontstyle="italic",
            fontweight="bold",
            color="#92400E",
            alpha=0.85,
            zorder=2,
        )

        # 2. Teken gewogen edges boven de drempelwaarde
        for u, v, w in filtered_edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            same_theme = graph.nodes[u].get("theme") == graph.nodes[v].get("theme")
            is_backbone = w >= highlight_weight

            if is_backbone:
                lw = 2.4 + 5.2 * (w / max_w)
                alpha = 0.82
                edge_col = (
                    THEME_COLORS_4.get(str(graph.nodes[u].get("theme")), "#334155")
                    if same_theme
                    else "#1E293B"
                )
                z_ord = 4
            else:
                lw = 1.0 + 2.2 * (w / max_w)
                alpha = 0.35
                edge_col = "#64748B" if same_theme else "#94A3B8"
                z_ord = 3

            # Gebruik een hele lichte kromming voor lange brug-lijnen zodat ze niet door andere nodes snijden
            rad = 0.08 if not same_theme and not is_backbone else 0.0
            arrow = FancyArrowPatch(
                (x0, y0),
                (x1, y1),
                connectionstyle=f"arc3,rad={rad}",
                arrowstyle="-",
                linewidth=lw,
                color=edge_col,
                alpha=alpha,
                linestyle="-" if (same_theme or is_backbone) else "--",
                zorder=z_ord,
            )
            self.ax.add_patch(arrow)

            # Label de gewichten op de belangrijkste ruggengraat-verbindingen (w >= highlight_weight)
            if is_backbone:
                mx = (x0 + x1) / 2.0
                my = (y0 + y1) / 2.0
                # Kleine offset voor leesbaarheid zodat geen enkel label overlapt
                if {u, v} == {"thuis", "eten & koken"}:
                    mx -= 0.07
                elif {u, v} == {"thuis", "Nusa & Indy"}:
                    mx = 0.01
                    my = -0.02
                elif {u, v} == {"eten & koken", "Nusa & Indy"}:
                    my -= 0.05
                elif {u, v} == {"eten & koken", "onze ouders"}:
                    mx = 0.25
                    my = 0.02
                elif {u, v} == {"thuis", "horeca"}:
                    mx = -0.40
                    my = -0.08
                elif {u, v} == {"eten & koken", "sporten"}:
                    mx = -0.58
                    my = -0.13

                self.ax.text(
                    mx,
                    my,
                    str(w),
                    ha="center",
                    va="center",
                    fontsize=8.4,
                    fontweight="bold",
                    color="#0F172A" if w < 80 else "#FFFFFF",
                    bbox={
                        "boxstyle": "round,pad=0.22",
                        "facecolor": "#1E293B" if w >= 80 else "#F8FAFC",
                        "edgecolor": "#CBD5E1" if w < 80 else "#0F172A",
                        "lw": 1.0,
                        "alpha": 0.94,
                    },
                    zorder=6,
                )

        # 3. Teken de 16 concept-nodes (geschaald op totale interactiekracht)
        label_offsets: dict[str, tuple[float, float, str, str]] = {
            "thuis": (-0.06, 0.09, "right", "bottom"),
            "eten & koken": (-0.06, -0.09, "right", "top"),
            "Nusa & Indy": (0.06, -0.08, "left", "top"),
            "onze ouders": (0.06, 0.07, "left", "bottom"),
            "werken algemeen": (0.0, 0.09, "center", "bottom"),
            "vervoersmiddelen": (0.0, 0.08, "center", "bottom"),
            "medisch & zorg": (0.06, 0.0, "left", "center"),
            "horeca": (0.0, -0.07, "center", "top"),
            "sporten": (-0.06, 0.0, "right", "center"),
            "uitlaten": (0.0, -0.07, "center", "top"),
            "Avans": (-0.06, 0.0, "right", "center"),
            "Rabobank & Gemeente": (-0.05, 0.0, "right", "center"),
            "familie": (0.05, 0.0, "left", "center"),
            "Feesten": (0.05, 0.0, "left", "center"),
            "dierenarts": (0.05, 0.0, "left", "center"),
            "eten honden": (-0.04, 0.0, "right", "center"),
        }

        for node in graph.nodes():
            is_active = active_degree.get(node, 0) > 0
            if not is_active:
                continue

            nx_x, nx_y = pos[node]
            theme = str(graph.nodes[node].get("theme", ""))
            col = THEME_COLORS_4.get(theme, "#475569")
            strength = node_strength.get(node, 0)

            # Schaal node-oppervlak op basis van gewogen graad (strength)
            s_size = 180.0 + (strength * 2.35)

            self.ax.scatter(
                nx_x,
                nx_y,
                s=s_size,
                color=col,
                edgecolor="white",
                linewidth=2.4,
                alpha=0.95,
                zorder=5,
            )

            dx, dy, ha_align, va_align = label_offsets.get(
                node, (0.0, -0.07, "center", "top")
            )
            label_str = (
                f"{node}\n(s={strength})" if strength >= 150 else f"{node} ({strength})"
            )
            self.ax.text(
                nx_x + dx,
                nx_y + dy,
                label_str,
                ha=ha_align,
                va=va_align,
                fontsize=9.2 if strength >= 200 else 8.4,
                fontweight="bold",
                fontstyle="normal",
                color="#0F172A",
                bbox={
                    "boxstyle": "round,pad=0.22",
                    "facecolor": "white",
                    "edgecolor": col if strength >= 240 else "none",
                    "lw": 1.1 if strength >= 240 else 0.0,
                    "alpha": 0.88,
                },
                zorder=7,
            )

        # 4. Verhalende annotaties voor de 2 kerninzichten
        annotate_badge(
            self.ax,
            "1. De 'keukentafel'-driehoek:\nSterkste verbindingen tussen thuis,\neten & koken (125) en de honden (99)",
            xy=(-0.19, -0.05),
            xytext=(-1.12, -0.78),
            settings=self.settings
            if isinstance(self.settings, JeffreyPlotSettings)
            else None,
        )
        annotate_context_badge(
            self.ax,
            "2. Bruggen naar buitenwereld:\nWerk (64) en onze ouders (45)\nhaken direct aan op thuis & eten",
            xy=(0.20, 0.20),
            xytext=(0.38, 0.92),
            settings=self.settings
            if isinstance(self.settings, JeffreyPlotSettings)
            else None,
        )

        # 5. Legenda voor de 4 leefwerelden en de verbindingsdrempel
        legend_handles = [
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label=theme_name,
                markerfacecolor=theme_col,
                markersize=10,
            )
            for theme_name, theme_col in THEME_COLORS_4.items()
        ]
        legend_handles.extend(
            [
                Line2D(
                    [0],
                    [0],
                    color="#1E293B",
                    lw=3.2,
                    linestyle="-",
                    label=f"Hoofdader (gewicht ≥ {highlight_weight})",
                ),
                Line2D(
                    [0],
                    [0],
                    color="#94A3B8",
                    lw=1.6,
                    linestyle="--",
                    label=f"Nevenverbinding ({min_edge_weight} ≤ gewicht < {highlight_weight})",
                ),
            ]
        )
        self.ax.legend(
            handles=legend_handles,
            loc="lower right",
            frameon=True,
            facecolor="#F8FAFC",
            edgecolor="#CBD5E1",
            fontsize=8.4,
            title="Leefwerelden & Verbindingen",
            title_fontsize=8.8,
        )

        self.ax.set_xlim(-1.22, 1.25)
        self.ax.set_ylim(-0.98, 1.08)

        # 6. Pakkende Schwabish-header & statistische voetnoot
        main_title = (
            "Van werk en familie altijd weer terug naar huis: "
            "de centrale driehoek die onze WhatsApp-gesprekken verbindt"
        )
        subtitle = (
            f"Netwerkgraaf van 16 onderwerpen (gefilterd op ≥ {min_edge_weight} interacties binnen 10 min): "
            "knoopgrootte toont hoe vaak een onderwerp meespeelt, lijndikte toont de sterkste gespreksroutes."
        )

        self.fig.text(
            0.05,
            0.955,
            main_title,
            fontsize=12.6,
            fontweight="bold",
            color="#1A202C",
            va="bottom",
            ha="left",
        )
        self.fig.text(
            0.05,
            0.930,
            subtitle,
            fontsize=9.2,
            fontstyle="italic",
            color="#475569",
            va="bottom",
            ha="left",
        )

        n_active_edges = len(filtered_edges)
        footnote_text = (
            f"- Toelichting & Statistische verantwoording: Bij drempelwaarde ≥ {min_edge_weight} blijven de {n_active_edges} sterkste verbindingen zichtbaar.\n"
            "- Brugfunctie (Betweenness Centrality): 'thuis' (0,36), 'eten & koken' (0,35) en 'Nusa & Indy' (0,32) vormen het centrale knooppunt waar alle domeinen samenkomen.\n"
            "- Modulariteitstoets (volledige graaf ≥ 3): De 4 deductieve leefwerelden clusteren significant sterker dan toeval (Q = 0,068, z = +5,32, p < 0,001; 1.000 permutaties), "
            "terwijl 64,3% van het gewicht een brug slaat tussen domeinen."
        )
        self.fig.text(
            0.05,
            0.02,
            footnote_text,
            fontsize=7.8,
            color="#475569",
            va="bottom",
            ha="left",
            linespacing=1.35,
        )

        self.fig.subplots_adjust(top=0.90, bottom=0.10, left=0.04, right=0.96)
        return self.fig, self.ax


class ConceptMatrixPlot(BasePlot):
    """Hiërarchische 16x16 concept-adjacency matrix met themakaders via BasePlot."""

    def __init__(
        self,
        settings: PlotSettings | None = None,
        n_plots: int | None = 1,
    ) -> None:
        if settings is None:
            settings = JeffreyPlotSettings(figsize=(12.8, 12.0), title="")
        super().__init__(settings=settings, n_plots=n_plots)

    def build(
        self,
        matrix_df: pd.DataFrame,
        summary_df: pd.DataFrame | None = None,
        *_args: object,
        **_kwargs: object,
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            self.create_figure()
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must initialize self.fig and self.ax")

        import matplotlib.colors as mcolors
        from wa_analyzer.features.concept_graph import CONCEPTS_16, THEME_COLORS_4

        self.fig.patch.set_facecolor("white")
        self.ax.set_facecolor("white")

        ordered_concepts = list(matrix_df.columns)
        adj_clean = matrix_df.values
        n_c = len(ordered_concepts)

        theme_slices: dict[str, tuple[int, int]] = {}
        curr = 0
        for theme, subdict in CONCEPTS_16.items():
            start = curr
            curr += len(subdict)
            theme_slices[theme] = (start, curr)

        norm = mcolors.PowerNorm(gamma=0.42, vmin=3, vmax=130)
        cmap = sns.color_palette("Blues", as_cmap=True)

        im = self.ax.imshow(adj_clean, cmap=cmap, norm=norm, interpolation="nearest")

        for i in range(n_c):
            for j in range(n_c):
                val = int(adj_clean[i, j])
                if i == j:
                    self.ax.text(
                        j,
                        i,
                        "—",
                        ha="center",
                        va="center",
                        color="#CBD5E1",
                        fontsize=10,
                        fontweight="bold",
                    )
                elif val >= 3:
                    text_color = "white" if val > 35 else "#0F172A"
                    self.ax.text(
                        j,
                        i,
                        str(val),
                        ha="center",
                        va="center",
                        color=text_color,
                        fontsize=8.6,
                        fontweight="bold",
                    )

        # Rasterlijnen tussen domeinen
        for idx in [4, 8, 12]:
            self.ax.axhline(idx - 0.5, color="#334155", lw=1.6, zorder=3)
            self.ax.axvline(idx - 0.5, color="#334155", lw=1.6, zorder=3)

        # Themakaders
        for theme, (start, end) in theme_slices.items():
            col = THEME_COLORS_4.get(theme, "#334155")
            rect = plt.Rectangle(
                (start - 0.5, start - 0.5),
                end - start,
                end - start,
                fill=False,
                edgecolor=col,
                linewidth=3.2,
                linestyle="-",
                zorder=4,
            )
            self.ax.add_patch(rect)

        self.ax.set_xticks(range(n_c))
        self.ax.set_yticks(range(n_c))
        self.ax.set_xticklabels(
            ordered_concepts,
            rotation=45,
            ha="left",
            fontsize=9.2,
            color="#1E293B",
            fontweight="bold",
        )
        self.ax.set_yticklabels(
            ordered_concepts, fontsize=9.2, color="#1E293B", fontweight="bold"
        )
        self.ax.xaxis.tick_top()
        self.ax.tick_params(axis="both", which="both", length=0, pad=6)

        # Subklassen-haken boven X-as en rechts van Y-as
        for theme, (start, end) in theme_slices.items():
            col = THEME_COLORS_4.get(theme, "#334155")
            x_mid = (start + end - 1) / 2.0
            x_left = start - 0.45
            x_right = end - 0.55
            bracket_y = -1.45

            self.ax.plot(
                [x_left, x_right],
                [bracket_y, bracket_y],
                color=col,
                lw=3.8,
                clip_on=False,
                solid_capstyle="round",
            )
            self.ax.text(
                x_mid,
                bracket_y - 0.35,
                theme,
                ha="center",
                va="bottom",
                fontsize=9.6,
                fontweight="bold",
                color=col,
                clip_on=False,
            )

            y_mid = (start + end - 1) / 2.0
            y_top = start - 0.45
            y_bottom = end - 0.55
            bracket_x = n_c + 0.35
            self.ax.plot(
                [bracket_x, bracket_x],
                [y_top, y_bottom],
                color=col,
                lw=3.8,
                clip_on=False,
                solid_capstyle="round",
            )
            self.ax.text(
                bracket_x + 0.35,
                y_mid,
                theme,
                ha="left",
                va="center",
                fontsize=9.6,
                fontweight="bold",
                color=col,
                rotation=270,
                clip_on=False,
            )

        # Main title, subtitle en footnote conform Les 7
        main_title = (
            "Interactiedichtheid over 4 themagebieden: Thuis, eten en de honden "
            "vormen de basis voor de meeste gespreksonderwerpen"
        )
        subtitle = (
            "Hiërarchische burenmatrix van 16 kernconcepten (4×4 modulair, Δt = 10 min, interacties ≥ 3). "
            "Kaders tonen thema-clusters; getallen tonen interactiekracht."
        )

        self.fig.text(
            0.18,
            0.965,
            main_title,
            fontsize=12.0,
            fontweight="bold",
            color="#1A202C",
            va="bottom",
            ha="left",
        )
        self.fig.text(
            0.18,
            0.942,
            subtitle,
            fontsize=9.2,
            fontweight="normal",
            color="#475569",
            va="bottom",
            ha="left",
        )

        footnote_text = (
            "* Toelichting & Statistische verantwoording (Les 7.1–7.3): Getallen tonen het interactiegewicht binnen Δt = 10 min (dubbel gewogen bij dialoog).\n"
            "  Incidentele ruis (1 of 2 interacties in 4 jaar) is gefilterd; '—' sluit zelf-lussen uit. Op auteursniveau is een 1-op-1 chat triviaal (N=2, E=1), vandaar de overstap naar concepten.\n"
            "  Statistische toetsing: De 4 themagroepen zijn deductief gekozen (a-priori model); de interne dichtheid is significant sterker dan toeval\n"
            "  (Q = 0,065, z = +4,92, p < 0,001 t.o.v. 1.000 netwerk-permutaties). Cellen buiten kaders tonen de verwevenheid: 63,9% van het gewicht slaat een brug tussen de domeinen."
        )

        self.fig.text(
            0.18,
            0.025,
            footnote_text,
            fontsize=7.8,
            color="#475569",
            va="bottom",
            ha="left",
            linespacing=1.35,
        )

        cbar = self.fig.colorbar(im, ax=self.ax, fraction=0.028, pad=0.08, shrink=0.7)
        cbar.set_label(
            "Interactiegewicht binnen 10 min (≥ 3)", fontsize=8.5, color="#475569"
        )
        cbar.ax.tick_params(labelsize=8, colors="#475569")

        self.fig.subplots_adjust(top=0.82, bottom=0.15, left=0.18, right=0.88)
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
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
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
    ) -> tuple[Figure, Axes]:
        if self.fig is None or self.ax is None:
            raise ValueError("create_figure() must run before build()")
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
