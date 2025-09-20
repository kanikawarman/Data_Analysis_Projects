
# Project: YouTube Content Strategy Optimization

## 🎯 Objective
To design a framework that helps creators and analysts understand **what types of content perform well**, **why they perform well**, and **how to replicate success across videos**.

---

## 🔧 What I Did
1. **Data Acquisition & Preparation**
   - Used the Kaggle dataset (`videos-stats.csv`, `comments.csv`).
   - Cleaned raw data (handled `-1` values for hidden likes/comments, parsed dates, ensured numeric typing).
   - Standardized schema for integration across video-level and comment-level datasets.

2. **Feature Engineering & Metrics**
   - **Performance Percentiles**: Computed 7-day, 30-day, and all-time view percentiles using rolling calendar windows.
   - **Engagement Rates**: Calculated like_rate (likes/views) and comment_rate (comments/views).
   - **Cohort Analysis**: Grouped videos by publish month, estimated cumulative views/day, and plotted growth curves.
   - **Comment Controversy Score**: Combined variance of sentiments, entropy of sentiment distribution, and variance in comment likes → normalized to a 0–1 score.
   - **Keyword Aggregation**: Rolled up controversy scores at keyword level to identify polarizing topics.

3. **Analysis & Insights**
   - Identified **consistently high performers** (≥80th percentile across all timeframes).
   - Correlated sentiment signals with video metrics to measure **engagement quality**.
   - Generated keyword-level controversy rankings and visualizations.

4. **Outputs & Deliverables**
   - CSV reports: enriched video metrics, cohort curves, keyword controversy, correlation matrices.
   - Plots: cohort trajectories, keyword controversy bar chart, correlation heatmap, most controversial videos, consistent high performers.
   - Packaged as a **modular Python project** with config, pipeline, and CLI for reproducibility.

---

## 🛠️ How I Did It
- **Tech Stack**: Python (Pandas, NumPy, Matplotlib, Seaborn), YAML for config.
- **Architecture**: Modular project with components:
  - `percentiles.py` → rolling percentiles
  - `cohorts.py` → cohort curves
  - `controversy.py` → controversy score
  - `analytics.py` → correlations, high performers, keyword analysis
  - `visualize.py` → plots
- **Pipeline**: Automated end-to-end run via `main.py` CLI, outputs CSVs & plots.
- **Design Choice**: Since dataset provided only snapshot totals (not daily timeseries), cohort analysis estimated cumulative growth by normalizing *views/day*.

---

## 💡 Why It Matters
- **For Creators**: Understand which content consistently wins, how controversy drives discussion, and when to post for long-term traction.
- **For Analysts/Brands**: Build repeatable benchmarks for content strategy optimization.
- **For Recruiters**: Demonstrates end-to-end data science workflow — data cleaning, feature engineering, analytics, visualization, reproducible code structure.

---

## 🎤 Interview Q&A with Answers and Follow-ups

### Q1. How did you calculate the 7-day and 30-day percentiles without daily views data?
**Answer**:  
The dataset only provides total views per video. To approximate short-term performance, I built **calendar-based peer groups**: for each video, I compared its total views at the snapshot against all other videos published in the **previous 7 or 30 calendar days**. The percentile is its relative standing within that peer set.

**Follow-ups**:  
- How would results differ if daily view counts were available?  
  → With daily counts, I could compute true growth curves (cumulative views at day 7, day 30) instead of approximations.  
- What biases could this introduce?  
  → Videos with longer lifetimes might look better in 30-day comparisons; fresh videos may seem weaker without daily breakdowns.  

---

### Q2. Why did you choose variance & entropy for the controversy score? Could you have used other measures?
**Answer**:  
- **Variance** of sentiment scores captures how spread-out opinions are.  
- **Entropy** measures disorder: higher when negative, neutral, and positive are equally likely → more polarized discussion.  
- **Variance in comment likes** adds another dimension: if some comments get extreme attention, it signals heated debate.  
These were combined and normalized to form a balanced score.

**Follow-ups**:  
- What alternatives could you use?  
  → Gini index, KL divergence, or topic modeling for semantic controversy.  
- Why average them instead of weighting?  
  → Averaging avoids overweighting one signal. Weighted schemes could be tuned if validated against ground truth.  

---

### Q3. How did you handle missing or hidden likes/comments?
**Answer**:  
In `videos-stats.csv`, `-1` indicated hidden counts. I converted these to `NaN` so they don’t distort averages or ratios. For rates (likes/views, comments/views), I only computed them if both numerator and denominator were valid.

**Follow-ups**:  
- What’s the risk of excluding too many rows?  
  → Reduced sample size and potential bias if creators who hide metrics systematically differ.  
- How could you mitigate?  
  → Imputation, median substitution, or treat “hidden” as a feature itself.  

---

### Q4. What are the limitations of the cohort analysis given the dataset?
**Answer**:  
The dataset only has total views at snapshot time. To simulate growth, I estimated **views/day** = total views ÷ age (days since publish). Then projected cumulative growth curves. This assumes stable growth, which is unrealistic but useful for relative comparison.

**Follow-ups**:  
- How would you improve it?  
  → With daily view data, compute true cumulative curves and retention metrics.  
- Could you still use proxy features?  
  → Yes, engagement velocity proxies: likes/day, comments/day.  

---

### Q5. Explain correlation results — did controversy positively or negatively affect views?
**Answer**:  
Controversy score showed a **moderate positive correlation with views** — suggesting polarizing videos often get more exposure. However, controversy correlated negatively with like_rate, implying divisive content attracts attention but may reduce approval.

**Follow-ups**:  
- Could correlation imply causation?  
  → Not necessarily; external promotion might drive both views and controversial comments.  
- How would you test causality?  
  → Time-series data or A/B testing.  

---

### Q6. What’s the difference between high-performing and consistently high-performing content?
**Answer**:  
- High-performing = videos in top percentiles in *one timeframe*.  
- Consistently high-performing = videos in ≥80th percentile in 7-day, 30-day, **and all-time**.  

**Follow-ups**:  
- Why is consistency important?  
  → It signals evergreen appeal, not just short-term virality.  

---

### Q7. How would you extend this framework to predict future video performance?
**Answer**:  
Add **predictive modeling**:  
- Features: early engagement velocity, sentiment distribution, keyword/topic.  
- Models: regression or gradient boosting to predict long-term views.

**Follow-ups**:  
- What metric would you predict?  
  → Views at day 30 or day 90.  
- How would you evaluate?  
  → MAE/RMSE for regression, rank correlation for relative prediction.  

---

### Q8. How do sentiment distributions affect different engagement metrics?
**Answer**:  
- Higher **positive sentiment fraction** → correlated with like_rate.  
- Higher **negative sentiment fraction** → correlated with comment_rate.  
- Mixed entropy → correlated with views.  

**Follow-ups**:  
- How would you prove this robustly?  
  → Stratify analysis by keyword/category, run statistical tests.  

---

### Q9. What real-world business applications do you see?
**Answer**:  
- For creators: Identify repeatable success.  
- For brands: Benchmark campaigns and avoid PR risks.  
- For platforms: Recommend balanced content strategies.

**Follow-ups**:  
- How would you turn this into a product?  
  → Build a dashboard (Streamlit/PowerBI) with cohort plots, controversy heatmaps, alerts.  

---

### Q10. How would you productize this as a dashboard?
**Answer**:  
- Backend: automated ETL from YouTube API.  
- Frontend: dashboard with cohorts, high performers, controversy, keyword rankings.  
- Alerts: notify when controversy > threshold or engagement velocity > baseline.

**Follow-ups**:  
- Which stack would you use?  
  → Streamlit for MVP; Airflow + dbt for pipelines; Tableau/PowerBI for enterprise.

---

## ✅ Takeaway
This project demonstrates **end-to-end data science ownership**: from cleaning raw data, engineering custom metrics, applying statistical methods, generating actionable insights, and preparing reproducible outputs — all while being interview-ready.
