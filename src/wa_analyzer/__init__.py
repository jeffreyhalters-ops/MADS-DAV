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
    BarPlot,
    BarPlotWithError,
    JeffreyPlotSettings,
    NegativeBinomialPlot,
    PiecewiseRegPlot,
    ResidualCurvePlot,
    SemanticPCAPlot,
    TopicNetworkPlot,
    annotate_badge,
    annotate_callout,
    annotate_context_badge,
    apply_dav_theme,
    format_footnote,
    format_header,
    plot_residual_curve,
    setup_dayparts_axis,
)

__all__ = [
    "BarPlot",
    "BarPlotWithError",
    "JeffreyPlotSettings",
    "NegativeBinomialPlot",
    "PiecewiseRegPlot",
    "PipelineConfig",
    "ResidualCurvePlot",
    "SemanticPCAPlot",
    "TopicNetworkPlot",
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
    "setup_dayparts_axis",
]
