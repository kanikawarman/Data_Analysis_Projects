import numpy as np
import pandas as pd

def standardize_columns(videos: pd.DataFrame, comments: pd.DataFrame):
    videos = videos.rename(columns={
        "Title": "title",
        "Video ID": "video_id",
        "Published At": "published_at",
        "Keyword": "keyword",
        "Likes": "likes",
        "Comments": "comments",
        "Views": "views"
    })
    comments = comments.rename(columns={
        "Video ID": "video_id",
        "Comment": "comment",
        "Likes": "comment_likes",
        "Sentiment": "sentiment"
    })
    return videos, comments

def clean_and_type(videos: pd.DataFrame, comments: pd.DataFrame):
    videos = videos.copy()
    comments = comments.copy()

    videos["published_at"] = pd.to_datetime(videos["published_at"], errors="coerce")

    for col in ["likes", "comments"]:
        if col in videos.columns:
            videos[col] = videos[col].replace(-1, np.nan)

    for col in ["views", "likes", "comments"]:
        videos[col] = pd.to_numeric(videos[col], errors="coerce")

    comments["comment_likes"] = pd.to_numeric(comments.get("comment_likes"), errors="coerce")
    comments["sentiment"] = pd.to_numeric(comments.get("sentiment"), errors="coerce")

    videos = videos.dropna(subset=["video_id", "published_at", "views"]).copy()
    comments = comments.dropna(subset=["video_id"]).copy()

    return videos, comments