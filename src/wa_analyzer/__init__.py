"""wa_analyzer: Modulaire, Atlas-proof Data & Visualisatie Pipeline (MADS-DAV)."""

from wa_analyzer.config import PipelineConfig
from wa_analyzer.pipeline import (
    build_message_pipeline,
    load_chat_data,
    load_sessions_data,
    run_feature_pipeline,
)
from wa_analyzer.preprocess import parse_raw_chat
from wa_analyzer.visualizer import (
    ChordComparisonPlot,
    ConceptNetworkPlot,
    JeffreyPlotSettings,
    NegativeBinomialPlot,
    PiecewiseRegPlot,
    ResidualCurvePlot,
    StylometryTimelinePlot,
    annotate_badge,
    annotate_callout,
    annotate_context_badge,
    apply_dav_theme,
    format_footnote,
    format_header,
    plot_residual_curve,
    save_figure,
    setup_dayparts_axis,
)

__all__ = [
    "ChordComparisonPlot",
    "ConceptNetworkPlot",
    "JeffreyPlotSettings",
    "NegativeBinomialPlot",
    "PiecewiseRegPlot",
    "PipelineConfig",
    "ResidualCurvePlot",
    "StylometryTimelinePlot",
    "annotate_badge",
    "annotate_callout",
    "annotate_context_badge",
    "apply_dav_theme",
    "build_message_pipeline",
    "format_footnote",
    "format_header",
    "load_chat_data",
    "load_sessions_data",
    "parse_raw_chat",
    "plot_residual_curve",
    "run_feature_pipeline",
    "save_figure",
    "setup_dayparts_axis",
]
