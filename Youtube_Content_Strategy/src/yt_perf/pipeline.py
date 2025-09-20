import os
import pandas as pd
from .data_loader import load_data
from .preprocessing import standardize_columns, clean_and_type
from .percentiles import compute_performance_percentiles, add_engagement_rates
from .cohorts import build_cohort_curves
from .controversy import compute_controversy
from .analytics import (
    consistent_high_performers,
    engagement_quality_correlations,
    keyword_controversy as kw_controversy,
    insights_correlations,
)
from .visualize import plot_cohort_curves, plot_keyword_controversy

def run_pipeline(cfg: dict):
    data_dir = cfg.get("data_dir", "data")
    videos_csv = cfg.get("videos_csv", "videos-stats.csv")
    comments_csv = cfg.get("comments_csv", "comments.csv")
    outputs_dir = cfg.get("outputs_dir", "outputs")
    plots_dir = cfg.get("plots_dir", "plots")
    horizon = int(cfg.get("horizon_days", 180))
    pctl_thresh = float(cfg.get("consistent_percentile_threshold", 80))
    max_cohorts = int(cfg.get("max_cohorts_to_plot", 8))
    top_keywords = int(cfg.get("top_keywords_to_plot", 10))

    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    videos, comments = load_data(data_dir, videos_csv, comments_csv)
    videos, comments = standardize_columns(videos, comments)
    videos, comments = clean_and_type(videos, comments)

    videos = compute_performance_percentiles(videos)
    videos = add_engagement_rates(videos)

    cohort_views_curve = build_cohort_curves(videos, horizon=horizon)

    videos_enriched = compute_controversy(videos, comments)

    top_consistent = consistent_high_performers(videos_enriched, threshold=pctl_thresh)
    corr_df = engagement_quality_correlations(videos_enriched)
    kw_df = kw_controversy(videos_enriched)
    insights_df = insights_correlations(corr_df)

    videos_enriched_out = os.path.join(outputs_dir, "videos_enriched_metrics.csv")
    keyword_controversy_out = os.path.join(outputs_dir, "keyword_controversy.csv")
    cohort_curve_out = os.path.join(outputs_dir, "cohort_views_curve.csv")
    consistent_out = os.path.join(outputs_dir, "consistent_high_performers.csv")
    corr_out = os.path.join(outputs_dir, "engagement_quality_correlations.csv")
    insights_out = os.path.join(outputs_dir, "engagement_quality_insights.csv")

    videos_enriched.to_csv(videos_enriched_out, index=False)
    kw_df.to_csv(keyword_controversy_out, index=False)
    cohort_views_curve.to_csv(cohort_curve_out, index=False)
    top_consistent.to_csv(consistent_out, index=False)
    corr_df.to_csv(corr_out, index=True)
    insights_df.to_csv(insights_out, index=False)

    cohort_png = plot_cohort_curves(cohort_views_curve, os.path.join(plots_dir, "cohort_trajectories.png"), max_cohorts=max_cohorts)
    kw_png = plot_keyword_controversy(kw_df, os.path.join(plots_dir, "top_keywords_controversy.png"), top_k=top_keywords)

    return {
        "videos_enriched": videos_enriched_out,
        "keyword_controversy": keyword_controversy_out,
        "cohort_views_curve": cohort_curve_out,
        "consistent_high_performers": consistent_out,
        "engagement_quality_correlations": corr_out,
        "engagement_quality_insights": insights_out,
        "cohort_plot": cohort_png,
        "keyword_plot": kw_png
    }