import numpy as np
import pandas as pd

def build_cohort_curves(videos: pd.DataFrame, horizon: int = 180) -> pd.DataFrame:
    videos = videos.copy()
    max_date = videos["published_at"].max()
    videos["age_days"] = (max_date - videos["published_at"]).dt.days.clip(lower=1)
    videos["views_per_day"] = videos["views"] / videos["age_days"]
    videos["cohort_month"] = videos["published_at"].dt.to_period("M").astype(str)

    ages = np.arange(1, horizon + 1)
    curves = []
    for cohort, dfc in videos.groupby("cohort_month"):
        if len(dfc) == 0:
            continue
        mean_vpd = dfc["views_per_day"].mean()
        curves.append(pd.DataFrame({
            "cohort_month": cohort,
            "age_day": ages,
            "avg_cum_views_est": mean_vpd * ages
        }))
    return pd.concat(curves, ignore_index=True) if curves else pd.DataFrame(columns=["cohort_month","age_day","avg_cum_views_est"])