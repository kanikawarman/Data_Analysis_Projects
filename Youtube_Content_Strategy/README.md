# YouTube Content Strategy Optimization – End-to-End Project

This project develops a content performance framework to help creators, analysts, or agencies understand what performs well on YouTube, why it performs well, and how to replicate success.

It uses the Kaggle dataset videos-stats.csv & comments.csv and provides metrics, analytics, and visualizations. It computes:

1. **Performance percentiles** (7-day, 30-day, all-time) using calendar windows around publish dates.  
2. **Cohort analysis**: group by publish month and estimate average cumulative views over the first N days (default 180).  
3. **Comment controversy score** from comment sentiment mix and comment-like variability.  
4. **Engagement quality** correlations between sentiment/controversy signals and performance metrics.  
5. Reports, plots, and CSV exports.

## 🔍 Key Features & Metrics
### 1. Performance Percentiles
- Calculates 7-day, 30-day, and all-time percentiles of views for each video.
- Percentiles are computed relative to calendar-based peers (videos uploaded in the last 7 or 30 days).
- *Helps answer:* “Is this video a short-term hit, a slow burner, or consistently strong across timeframes?”

###  2. Cohort Analysis
- Groups videos by publish month.
- Estimates average cumulative views per cohort over the first N days (default: 180).
- Reveals long-term audience growth trends and identifies which months (or campaigns) produced the strongest performers.
- *Example:* “Do videos launched in December cohorts sustain more views than those in July?”

### 3. Comment Controversy Score
- Measures how polarized or heated discussions are under each video.
- Built from: Variance in comment sentiment (negative, neutral, positive)
- Variance in comment likes
- Entropy of sentiment distribution (higher = more mixed opinions)
- Normalized and combined into a 0–1 score.
- Helps identify: “Which videos drive debate vs. which videos are universally liked?”

### 4. Engagement Quality Correlations
- Correlation analysis between sentiment signals and performance metrics such as:
- Views
- Like rate (likes / views)
- Comment rate (comments / views)
- Percentile ranks
- Example insights: “Do controversial videos actually get more views?”, “Does positive sentiment correlate with long-term retention?”

### 5. Keyword-Level Controversy
- Aggregates controversy scores by video keyword.
- Identifies which topics or themes spark the most polarizing discussions.
- Example: “Are political videos more controversial than gaming or entertainment?”

## 📊 Outputs

After running, you’ll find:

1. CSV Reports (outputs/)
- videos_enriched_metrics.csv → All videos with computed metrics (percentiles, engagement rates, controversy).
- keyword_controversy.csv → Average controversy score per keyword.
- cohort_views_curve.csv → Cohort growth trajectories.
- consistent_high_performers.csv → Videos ≥80th percentile across all timeframes.
- engagement_quality_correlations.csv → Pearson correlation matrix.
- engagement_quality_insights.csv → Ranked signal–metric correlations.

2. Visualizations (plots/)

- cohort_trajectories.png → Cohort performance curves (average cumulative views vs. age).
- top_keywords_controversy.png → Top 10 most controversial keywords.

## 🛠️ How to Use
1. Install dependencies

- pip install -r requirements.txt

3. Add data

- Place the Kaggle CSVs into the data/ folder:

   -- data/videos-stats.csv

   -- data/comments.csv

3. Run pipeline

- python main.py --horizon 180 --percentile-thresh 80

4. Explore results

- Open CSVs in outputs/
- View charts in plots/

## ⚙️ Configuration

- You can modify config.yaml or override via CLI:

python main.py \
  --data-dir data \
  --outputs-dir outputs \
  --plots-dir plots \
  --horizon 120 \
  --percentile-thresh 85

### Parameters:

- horizon_days → Cohort horizon (default: 180 days)
- consistent_percentile_threshold → Consistency threshold (default: 80)
- max_cohorts_to_plot → Max cohorts in plots (default: 8)
- top_keywords_to_plot → Top controversial keywords in chart (default: 10)

## 📈 Example Insights

1. Consistently High Performers
- Videos above the 80th percentile in 7-day, 30-day, and all-time performance.
- These are “benchmark” videos to replicate.

| Video ID | Title                     | Views | 7d %ile | 30d %ile | All-time %ile |
| -------- | ------------------------- | ----- | ------- | -------- | ------------- |
| vid123   | *Top 10 AI Tools of 2024* | 2.3M  | 96      | 94       | 95            |
| vid456   | *How to Edit Shorts Fast* | 1.8M  | 92      | 91       | 93            |

  
2. Engagement Quality
- Correlation between controversy_score and views often highlights whether debate drives virality.
- Positive sentiment vs. like_rate shows whether audience approval translates to stronger engagement.

3. Comment Controversy Score

- High controversy (0.85+): “Political Debate Highlights” (mixed sentiment, polarized likes).

Low controversy (<0.2): “Relaxing Study Music” (positive consensus, stable likes).
| Video Title                 | Controversy Score | % Negative | % Neutral | % Positive |
| --------------------------- | ----------------- | ---------- | --------- | ---------- |
| Political Debate Highlights | 0.87              | 0.42       | 0.18      | 0.40       |
| Relaxing Study Music        | 0.15              | 0.05       | 0.12      | 0.83       |


4. Cohorts
- Some publish-month cohorts sustain views much longer, signaling timing and seasonal impact.

5. Keywords
- Identifies which topics consistently spark polarized discussions (e.g., politics vs. lifestyle).

| Keyword    | Avg Controversy | Avg Views |
| ---------- | --------------- | --------- |
| politics   | 0.78            | 1.2M      |
| technology | 0.42            | 950K      |
| lifestyle  | 0.19            | 600K      |


## 🚀 Why This Matters

This framework helps creators and brands:

- Benchmark their video’s relative performance quickly.
- Identify repeatable success patterns.
- Detect whether controversy fuels engagement or harms growth.
- Optimize content strategy by cohort and keyword trends.

This helps to answer the following questions:

- Percentiles (7d/30d): For each video, we benchmark its current views against videos published in the prior 7 or 30 calendar days up to its publish date. All-time is across the entire dataset. This answers, “How did it stack up versus its time-peer set?”

- Cohorts: We approximate average cumulative growth by computing views/day within each publish-month cohort, then projecting cumulative curves. It’s a pragmatic approach given we have snapshot totals (not day-by-day histories).

- Controversy score: Mix of (a) variance and (b) entropy in sentiment (0=neg,1=neu,2=pos) and (c) variance in comment likes—each min-max normalized and averaged. Entropy captures how “split” the audience is; likes variance captures uneven attention across comments.
