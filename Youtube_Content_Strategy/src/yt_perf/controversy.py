import numpy as np
import pandas as pd

def _minmax(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    mn, mx = np.nanmin(s), np.nanmax(s)
    if not np.isfinite(mn) or not np.isfinite(mx) or mn == mx:
        return pd.Series([np.nan]*len(s), index=s.index)
    return (s - mn) / (mx - mn)

def compute_controversy(videos: pd.DataFrame, comments: pd.DataFrame) -> pd.DataFrame:
    videos = videos.copy()
    if comments is None or comments.empty:
        for col, val in [
            ("controversy_score", np.nan), ("n_comments", 0),
            ("frac_neg", np.nan), ("frac_neu", np.nan), ("frac_pos", np.nan),
            ("mean_comment_likes", np.nan), ("sentiment_entropy", np.nan)
        ]:
            videos[col] = val
        return videos

    def entropy(x: pd.Series) -> float:
        p = np.array([(x==k).mean() for k in [0,1,2]], dtype=float)
        return float(-np.nansum(p * np.log2(p + 1e-12)))

    com_grp = comments.groupby("video_id").agg(
        sentiment_var=("sentiment", lambda x: np.nan if len(x.dropna())<=1 else np.nanvar(x.dropna())),
        sentiment_entropy=("sentiment", entropy),
        comment_likes_var=("comment_likes", lambda x: np.nan if len(x.dropna())<=1 else np.nanvar(x.dropna())),
        n_comments=("sentiment", "count"),
        frac_neg=("sentiment", lambda x: (x==0).mean() if len(x)>0 else np.nan),
        frac_neu=("sentiment", lambda x: (x==1).mean() if len(x)>0 else np.nan),
        frac_pos=("sentiment", lambda x: (x==2).mean() if len(x)>0 else np.nan),
        mean_comment_likes=("comment_likes", "mean")
    ).reset_index()

    com_grp["sentiment_var_norm"] = _minmax(com_grp["sentiment_var"])
    com_grp["comment_likes_var_norm"] = _minmax(com_grp["comment_likes_var"])
    com_grp["sentiment_entropy_norm"] = _minmax(com_grp["sentiment_entropy"])
    com_grp["controversy_score"] = com_grp[["sentiment_var_norm","comment_likes_var_norm","sentiment_entropy_norm"]].mean(axis=1, skipna=True)

    return videos.merge(com_grp, on="video_id", how="left")