import argparse
import os
import yaml
from src.yt_perf.pipeline import run_pipeline

def parse_args():
    ap = argparse.ArgumentParser(description="YouTube Content Strategy Optimization Pipeline")
    ap.add_argument("--config", default="config.yaml", help="Path to YAML config")
    ap.add_argument("--data-dir", help="Data directory containing CSVs")
    ap.add_argument("--videos-csv", help="Videos CSV filename")
    ap.add_argument("--comments-csv", help="Comments CSV filename")
    ap.add_argument("--outputs-dir", help="Directory to write outputs")
    ap.add_argument("--plots-dir", help="Directory to write plots")
    ap.add_argument("--horizon", type=int, help="Cohort horizon in days")
    ap.add_argument("--percentile-thresh", type=float, help="Threshold for consistent high performers")
    ap.add_argument("--max-cohorts-to-plot", type=int, help="Max cohorts in plot legend")
    ap.add_argument("--top-keywords-to-plot", type=int, help="Top keywords for controversy plot")
    return ap.parse_args()

def load_config(cfg_path):
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg

def merge_cli_overrides(cfg, args):
    overrides = {}
    if args.data_dir: overrides["data_dir"] = args.data_dir
    if args.videos_csv: overrides["videos_csv"] = args.videos_csv
    if args.comments_csv: overrides["comments_csv"] = args.comments_csv
    if args.outputs_dir: overrides["outputs_dir"] = args.outputs_dir
    if args.plots_dir: overrides["plots_dir"] = args.plots_dir
    if args.horizon is not None: overrides["horizon_days"] = args.horizon
    if args.percentile_thresh is not None: overrides["consistent_percentile_threshold"] = args.percentile_thresh
    if args.max_cohorts_to_plot is not None: overrides["max_cohorts_to_plot"] = args.max_cohorts_to_plot
    if args.top_keywords_to_plot is not None: overrides["top_keywords_to_plot"] = args.top_keywords_to_plot
    cfg.update(overrides)
    return cfg

def main():
    args = parse_args()
    cfg = load_config(args.config)
    cfg = merge_cli_overrides(cfg, args)
    for key in ["data_dir","outputs_dir","plots_dir"]:
        if key in cfg:
            cfg[key] = os.path.normpath(cfg[key])
    print("Running pipeline with config:", cfg)
    outputs = run_pipeline(cfg)
    print("Artifacts written:")
    for k, v in outputs.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()