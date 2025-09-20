import pandas as pd

def consistent_high_performers(videos_enriched: pd.DataFrame, threshold: float = 80.0) -> pd.DataFrame:
    df = videos_enriched.copy()
    mask = (
        (df["pctile_7d_views"] >= threshold) &
        (df["pctile_30d_views"] >= threshold) &
        (df["pctile_alltime_views"] >= threshold)
    )
    cols = ["video_id","title","keyword","views","likes","comments",
            "pctile_7d_views","pctile_30d_views","pctile_alltime_views","controversy_score"]
    return df.loc[mask, cols].sort_values(
        ["pctile_alltime_views","pctile_30d_views","pctile_7d_views"], ascending=False
    )

def engagement_quality_correlations(videos_enriched: pd.DataFrame) -> pd.DataFrame:
    corr_cols = [
        "views","likes","comments","like_rate","comment_rate",
        "pctile_7d_views","pctile_30d_views","pctile_alltime_views",
        "controversy_score","sentiment_entropy","frac_neg","frac_neu","frac_pos","mean_comment_likes"
    ]
    available = [c for c in corr_cols if c in videos_enriched.columns]
    return videos_enriched[available].corr(numeric_only=True)

def keyword_controversy(videos_enriched: pd.DataFrame) -> pd.DataFrame:
    if "keyword" not in videos_enriched.columns:
        return pd.DataFrame(columns=["keyword","avg_controversy","videos","avg_views"])
    return (videos_enriched.groupby("keyword")
            .agg(avg_controversy=("controversy_score","mean"),
                 videos=("video_id","nunique"),
                 avg_views=("views","mean"))
            .reset_index()
            .sort_values("avg_controversy", ascending=False))

def insights_correlations(corr_df: pd.DataFrame):
    target_metrics = ["views","like_rate","comment_rate","pctile_alltime_views"]
    signal_metrics = ["controversy_score","sentiment_entropy","frac_neg","frac_pos","frac_neu","mean_comment_likes"]
    insights = []
    for sig in signal_metrics:
        if sig not in corr_df.index:
            continue
        for tgt in target_metrics:
            if tgt not in corr_df.columns:
                continue
            val = corr_df.loc[sig, tgt]
            if pd.notnull(val):
                insights.append({"signal": sig, "target_metric": tgt, "pearson_corr": val})
    return pd.DataFrame(insights).sort_values("pearson_corr", key=lambda s: s.abs(), ascending=False)