import os
import pandas as pd

def load_data(data_dir: str, videos_csv: str, comments_csv: str):
    videos_path = os.path.join(data_dir, videos_csv)
    comments_path = os.path.join(data_dir, comments_csv)
    videos = pd.read_csv(videos_path)
    comments = pd.read_csv(comments_path)
    return videos, comments