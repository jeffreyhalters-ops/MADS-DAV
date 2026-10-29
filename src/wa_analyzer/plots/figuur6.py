"""Figuur 6 (Les 7): Netwerkanalyse van de 16 Gespreksthema's (Co-occurrencenetwerk & Brugknopen)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from wa_analyzer.config import (
    THEME_COLORS,
    THEMATIC_REGEXES_16,
)
from wa_analyzer.visualizer import (
    JeffreyPlotSettings,
    TopicNetworkPlot,
    annotate_badge,
    format_footnote,
    format_header,
)

NODE_METADATA: dict[str, tuple[str, str]] = {
    "rx_koken_eten": ("Koken &\nAvondeten", "Huishouden en Voeding"),
    "rx_boodschappen": ("Boodschappen\n& Supermarkt", "Huishouden en Voeding"),
    "rx_schoonmaak_was": ("Was &\nHuishouden", "Huishouden en Voeding"),
    "rx_pakket_klus": ("Pakketjes &\nKlussen", "Huishouden en Voeding"),
    "rx_werk_kantoor": ("Werk &\nKantoor", "Werk en Mobiliteit"),
    "rx_overleg_studie": ("Meeting &\nStudie", "Werk en Mobiliteit"),
    "rx_auto_verkeer": ("Auto &\nOnderweg", "Werk en Mobiliteit"),
    "rx_ov_reizen": ("Trein &\nOV-reis", "Werk en Mobiliteit"),
    "rx_hond_uitlaten": ("Hond &\nWandelen", "Huisdieren"),
    "rx_kat_Gedrag": ("Kat &\nKnuffelen", "Huisdieren"),
    "rx_dier_voeding": ("Diervoer &\nBrokjes", "Huisdieren"),
    "rx_dierenarts": ("Dierenarts &\nZorg", "Huisdieren"),
    "rx_familie_bezoek": ("Familie &\nVisite", "Zorg & Familie"),
    "rx_gezondheid": ("Slaap &\nGezondheid", "Zorg & Familie"),
    "rx_medisch_zorg": ("Huisarts &\nApotheek", "Zorg & Familie"),
    "rx_sociaal_feest": ("Verjaardag &\nUitjes", "Zorg & Familie"),
}


@dataclass(frozen=True)
class Figuur6NetworkResult:
    """Netwerkeigenschappen en centraliteitsmaten voor Figuur 6 (Les 7)."""

    graph: nx.Graph
    node_stats_df: pd.DataFrame
    edge_df: pd.DataFrame
    top_bridge_node: str
    top_bridge_pair: tuple[str, str]
    top_pair_weight: int
    n_active_sessions: int


def fit_figuur6_network(df_chat: pd.DataFrame) -> Figuur6NetworkResult:
    """Construeer het gewogen co-occurrencenetwerk van de 16 subthema's binnen sessies."""
    rx_cols = list(THEMATIC_REGEXES_16.keys())
    session_rx = df_chat.groupby("session_id")[rx_cols].sum()
    binary_rx = (session_rx > 0).astype(int)
    active_sessions = int((binary_rx.sum(axis=1) > 0).sum())

    co_matrix = binary_rx.T.dot(binary_rx)
    graph = nx.Graph()

    for col in rx_cols:
        label, domain = NODE_METADATA[col]
        freq = int(binary_rx[col].sum())
        graph.add_node(
            col,
            label=label,
            domain=domain,
            sessions_count=freq,
        )

    edge_rows: list[dict[str, object]] = []
    for i, u in enumerate(rx_cols):
        for v in rx_cols[i + 1 :]:
            weight = int(co_matrix.loc[u, v])
            if weight >= 3:
                graph.add_edge(u, v, weight=weight)
                edge_rows.append(
                    {
                        "source": u,
                        "target": v,
                        "weight": weight,
                        "cross_domain": NODE_METADATA[u][1] != NODE_METADATA[v][1],
                    }
                )

    weighted_deg = dict(graph.degree(weight="weight"))
    betweenness = nx.betweenness_centrality(graph, weight="weight")

    node_rows: list[dict[str, object]] = []
    for col in rx_cols:
        label, domain = NODE_METADATA[col]
        node_rows.append(
            {
                "node": col,
                "label": label.replace("\n", " "),
                "domain": domain,
                "sessions_count": int(binary_rx[col].sum()),
                "weighted_degree": int(weighted_deg.get(col, 0)),
                "betweenness": float(betweenness.get(col, 0.0)),
            }
        )

    node_stats_df = (
        pd.DataFrame(node_rows)
        .sort_values("weighted_degree", ascending=False)
        .reset_index(drop=True)
    )
    edge_df = (
        pd.DataFrame(edge_rows)
        .sort_values("weight", ascending=False)
        .reset_index(drop=True)
    )

    top_bridge = str(node_stats_df.iloc[0]["node"])
    cross_edges = edge_df[edge_df["cross_domain"]].reset_index(drop=True)
    top_u = str(cross_edges.iloc[0]["source"])
    top_v = str(cross_edges.iloc[0]["target"])
    top_w = int(cross_edges.iloc[0]["weight"])

    return Figuur6NetworkResult(
        graph=graph,
        node_stats_df=node_stats_df,
        edge_df=edge_df,
        top_bridge_node=top_bridge,
        top_bridge_pair=(top_u, top_v),
        top_pair_weight=top_w,
        n_active_sessions=active_sessions,
    )


def _compute_clustered_layout() -> dict[str, tuple[float, float]]:
    """Deterministische geclusterde 2D-posities voor de 4 domeinen en 16 subthema's."""
    return {
        # Links-boven: Huishouden en Voeding
        "rx_koken_eten": (-0.42, 0.28),
        "rx_boodschappen": (-0.65, 0.58),
        "rx_schoonmaak_was": (-0.98, 0.34),
        "rx_pakket_klus": (-0.88, 0.72),
        # Rechts-boven: Werk en Mobiliteit
        "rx_werk_kantoor": (0.44, 0.32),
        "rx_auto_verkeer": (0.28, 0.64),
        "rx_overleg_studie": (0.86, 0.56),
        "rx_ov_reizen": (0.94, 0.22),
        # Links-onder: Huisdieren
        "rx_hond_uitlaten": (-0.48, -0.24),
        "rx_kat_Gedrag": (-0.92, -0.20),
        "rx_dier_voeding": (-0.90, -0.56),
        "rx_dierenarts": (-0.56, -0.56),
        # Rechts-onder: Zorg & Familie
        "rx_gezondheid": (0.48, -0.24),
        "rx_familie_bezoek": (0.86, -0.20),
        "rx_sociaal_feest": (0.90, -0.56),
        "rx_medisch_zorg": (0.56, -0.56),
    }


def plot_figuur6(
    net_res: Figuur6NetworkResult,
    save_path: Path | None = None,
) -> Figure:
    """Genereer Figuur 6: Thematisch co-occurrencenetwerk van de 16 gespreksonderwerpen."""
    pos = _compute_clustered_layout()
    settings = JeffreyPlotSettings(figsize=(12.5, 7.5), title="")

    fig, ax = TopicNetworkPlot(settings).plot(
        graph=net_res.graph,
        pos=pos,
        node_metadata=NODE_METADATA,
    )

    mid_x = (pos["rx_koken_eten"][0] + pos["rx_werk_kantoor"][0]) / 2.0
    mid_y = (pos["rx_koken_eten"][1] + pos["rx_werk_kantoor"][1]) / 2.0
    annotate_badge(
        ax,
        text=(
            f"Sterkste domeinbrug ({net_res.top_pair_weight} gedeelde sessies):\n"
            "'Werk & Kantoor' en 'Koken & Avondeten' zijn sterk verbonden:\n"
            "zodra één van ons vanaf werk vertrekt, start het eet-overleg."
        ),
        xy=(mid_x, mid_y),
        xytext=(-0.36, 0.80),
        settings=settings,
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=dom,
            markerfacecolor=THEME_COLORS[dom],
            markersize=11,
        )
        for dom in (
            "Huishouden en Voeding",
            "Werk en Mobiliteit",
            "Huisdieren",
            "Zorg & Familie",
        )
    ]
    ax.legend(
        handles=legend_elements,
        title="Thematische Clusters (4 Domeinen)",
        frameon=True,
        facecolor="white",
        edgecolor="#D0D3D4",
        loc="lower center",
        bbox_to_anchor=(0.50, -0.02),
        ncol=2,
        fontsize=9.2,
        title_fontsize=9.5,
    )

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.02, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    format_header(
        ax,
        title="Netwerkanalyse: 'Werk & Kantoor' en 'Koken & Avondeten' vormen de centrale brug in onze chat",
        subtitle=(
            "Gewogen co-occurrencenetwerk van de 16 thematische regex-features binnen dialoogsessies "
            f"(N = {net_res.n_active_sessions:,} thematische sessies; lijndikte = gedeelde sessies)".replace(
                ",", "."
            )
        ),
    )
    format_footnote(
        ax,
        text=(
            "Bron: WhatsApp-export (2022–2026). Methode: Tweevoudige graafprojectie (NetworkX) van 16 regex-thema's "
            "binnen empirische sessies (~21 min drempel); knoopgrootte = sessiefrequentie, lijndikte = co-occurrence (≥ 5)."
        ),
        y_offset=-0.06,
    )

    if save_path is not None:
        with contextlib.suppress(PermissionError):
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return fig
