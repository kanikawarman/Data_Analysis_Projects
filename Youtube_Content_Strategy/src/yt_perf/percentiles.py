import numpy as np
import pandas as pd
from datetime import timedelta

def compute_performance_percentiles(videos: pd.DataFrame) -> pd.DataFrame:
    videos = videos.sort_values("published_at").reset_index(drop=True).copy()

    p7, p30 = [], []
    pub_dates = videos["published_at"].tolist()
    views_arr = videos["views"].tolist()

    for d, v in zip(pub_dates, views_arr):
        w7_start = d - timedelta(days=6)
        w30_start = d - timedelta(days=29)
        mask7 = (videos["published_at"] >= w7_start) & (videos["published_at"] <= d)
        mask30 = (videos["published_at"] >= w30_start) & (videos["published_at"] <= d)
        w7_views = videos.loc[mask7, "views"]
        w30_views = videos.loc[mask30, "views"]
        p7_val = np.nan if len(w7_views) == 0 else 100.0 * ((w7_views <= v).sum() / len(w7_views))
        p30_val = np.nan if len(w30_views) == 0 else 100.0 * ((w30_views <= v).sum() / len(w30_views))
        p7.append(p7_val)
        p30.append(p30_val)

    videos["pctile_7d_views"] = p7
    videos["pctile_30d_views"] = p30
    videos["pctile_alltime_views"] = 100.0 * (videos["views"].rank(pct=True, method="average"))
    return videos

def add_engagement_rates(videos: pd.DataFrame) -> pd.DataFrame:
    videos = videos.copy()
    videos["like_rate"] = videos.apply(lambda r: (r["likes"] / r["views"]) if pd.notnull(r["likes"]) and r["views"] > 0 else np.nan, axis=1)
    videos["comment_rate"] = videos.apply(lambda r: (r["comments"] / r["views"]) if pd.notnull(r["comments"]) and r["views"] > 0 else np.nan, axis=1)
    return videos