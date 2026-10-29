"""Centrale CLI/orchestrator: draait preprocess -> pipeline -> plots -> img/."""

from __future__ import annotations

from pathlib import Path

import click
from loguru import logger
from matplotlib.figure import Figure

from wa_analyzer.config import PipelineConfig
from wa_analyzer.pipeline import run_feature_pipeline
from wa_analyzer.plots import (
    fit_figuur1_stats,
    fit_figuur2_bootstrap,
    fit_figuur3_distributions,
    fit_figuur4_piecewise,
    fit_figuur5_pca,
    fit_figuur6_network,
    plot_figuur1,
    plot_figuur2,
    plot_figuur3,
    plot_figuur4,
    plot_figuur5,
    plot_figuur6,
)


def run_all(root_dir: Path | None = None) -> dict[str, Figure]:
    """Voer de gehele Source-to-Sinks pijplijn uit en sla alle 6 figuren op in `img/`."""
    base_dir = root_dir if root_dir is not None else Path(__file__).resolve().parent
    cfg = PipelineConfig.from_root(base_dir)

    logger.info("Stap 1/3: Preprocessing & Centrale Feature Pipeline uitvoeren...")
    df_chat, df_sessions = run_feature_pipeline(cfg)

    logger.info("Stap 2/3: Statistische modellen fitten en Figure 1 t/m 6 renderen...")
    figures: dict[str, Figure] = {}

    stats_fig1 = fit_figuur1_stats(df_chat)
    figures["figuur1"] = plot_figuur1(
        stats_fig1, save_path=cfg.img_dir / "figuur1_reactietijd_barbell.png"
    )

    boot_fig2 = fit_figuur2_bootstrap(df_chat)
    figures["figuur2"] = plot_figuur2(
        boot_fig2, save_path=cfg.img_dir / "figuur2_dagritme_residu.png"
    )

    dist_fig3 = fit_figuur3_distributions(df_chat)
    figures["figuur3"] = plot_figuur3(
        dist_fig3, save_path=cfg.img_dir / "figuur3_verdelingen_voor_na.png"
    )

    model_fig4 = fit_figuur4_piecewise(df_chat)
    figures["figuur4"] = plot_figuur4(
        model_fig4,
        save_path=cfg.img_dir / "figuur4_relatie_woordlengte_reactietijd.png",
    )

    pca_fig5 = fit_figuur5_pca(df_sessions)
    figures["figuur5"] = plot_figuur5(
        pca_fig5, save_path=cfg.img_dir / "figuur5_vectorruimte_gesprek.png"
    )

    net_fig6 = fit_figuur6_network(df_chat)
    figures["figuur6"] = plot_figuur6(
        net_fig6, save_path=cfg.img_dir / "figuur6_netwerkanalyse.png"
    )

    logger.info(f"Stap 3/3: Voltooid! Alle 6 figuren zijn opgeslagen in {cfg.img_dir}.")
    return figures


@click.command()
@click.option(
    "--root-dir",
    type=click.Path(path_type=Path),
    default=Path(__file__).resolve().parent,
    help="Project root directory",
)
def main(root_dir: Path) -> None:
    """CLI-entrypoint voor wa-analyzer."""
    run_all(root_dir)


if __name__ == "__main__":
    main()
