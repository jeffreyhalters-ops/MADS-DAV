"""Publicatie-waardige plotmodules voor Figuur 1 t/m Figuur 6."""

from wa_analyzer.plots.figuur1 import Figuur1Stats, fit_figuur1_stats, plot_figuur1
from wa_analyzer.plots.figuur2 import (
    Figuur2BootstrapResult,
    fit_figuur2_bootstrap,
    plot_figuur2,
)
from wa_analyzer.plots.figuur3 import (
    Figuur3DistributionResult,
    fit_figuur3_distributions,
    plot_figuur3,
)
from wa_analyzer.plots.figuur4 import (
    Figuur4PiecewiseResult,
    fit_figuur4_piecewise,
    plot_figuur4,
)
from wa_analyzer.plots.figuur5 import Figuur5PCAResult, fit_figuur5_pca, plot_figuur5
from wa_analyzer.plots.figuur6 import (
    Figuur6NetworkResult,
    fit_figuur6_network,
    plot_figuur6,
)

__all__ = [
    "Figuur1Stats",
    "Figuur2BootstrapResult",
    "Figuur3DistributionResult",
    "Figuur4PiecewiseResult",
    "Figuur5PCAResult",
    "Figuur6NetworkResult",
    "fit_figuur1_stats",
    "fit_figuur2_bootstrap",
    "fit_figuur3_distributions",
    "fit_figuur4_piecewise",
    "fit_figuur5_pca",
    "fit_figuur6_network",
    "plot_figuur1",
    "plot_figuur2",
    "plot_figuur3",
    "plot_figuur4",
    "plot_figuur5",
    "plot_figuur6",
]
