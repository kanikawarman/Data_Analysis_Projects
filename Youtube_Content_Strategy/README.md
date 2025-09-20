# YouTube Content Strategy Optimization – End-to-End Project

This project builds a **content performance framework** for YouTube using the Kaggle dataset (videos-stats.csv and comments.csv). It computes:

1. **Performance percentiles** (7-day, 30-day, all-time) using calendar windows around publish dates.  
2. **Cohort analysis**: group by publish month and estimate average cumulative views over the first N days (default 180).  
3. **Comment controversy score** from comment sentiment mix and comment-like variability.  
4. **Engagement quality** correlations between sentiment/controversy signals and performance metrics.  
5. Reports, plots, and CSV exports.

See `config.yaml` and `main.py --help` for usage.