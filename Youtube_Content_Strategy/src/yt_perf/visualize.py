import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_cohort_curves(cohort_views_curve: pd.DataFrame, out_path: str, max_cohorts: int = 8):
    if cohort_views_curve is None or cohort_views_curve.empty:
        return None
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.figure()
    cohorts_to_plot = cohort_views_curve["cohort_month"].unique()[:max_cohorts]
    for cohort in cohorts_to_plot:
        subset = cohort_views_curve[cohort_views_curve["cohort_month"] == cohort]
        plt.plot(subset["age_day"], subset["avg_cum_views_est"], label=str(cohort))
    plt.xlabel("Age (days since publish)")
    plt.ylabel("Estimated Avg Cumulative Views")
    plt.title("Cohort Trajectories (Estimated)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path

def plot_keyword_controversy(keyword_controversy_df: pd.DataFrame, out_path: str, top_k: int = 10):
    if keyword_controversy_df is None or keyword_controversy_df.empty:
        return None
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    topk = keyword_controversy_df.head(top_k)
    plt.figure()
    plt.bar(topk["keyword"].astype(str), topk["avg_controversy"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Average Controversy Score")
    plt.title("Top Keywords by Controversy")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path