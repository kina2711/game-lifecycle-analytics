# 🎮 Gamelytics: Mobile Game Lifecycle Analytics

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![BigQuery](https://img.shields.io/badge/Google_Cloud-BigQuery-4285F4.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

> **Portfolio Project** solving the [Gamelytics Mobile Analytics Challenge](https://www.kaggle.com/datasets/debs2x/gamelytics-mobile-analytics-challenge) on Kaggle.

## 📖 Overview

**Gamelytics** is an end-to-end data analytics project that simulates the workflow of a Data Analyst in the Gaming Industry. The project analyzes a dataset of **1 million users** to evaluate game health, user stickiness, and monetization strategies.

**Key Objectives:**
1.  **Retention Analysis:** Analyzing user lifecycle via Daily Retention Curves to pinpoint drop-off moments.
2.  **A/B Testing:** Evaluating a monetization experiment (Group A vs. Group B) using Statistical Hypothesis Testing.
3.  **Whale Analysis:** Identifying high-value players driving the revenue.

## 🏗️ Tech Stack & Architecture

This project moves beyond simple CSV analysis by implementing a scalable cloud data pipeline:

* **Cloud Data Warehouse:** Google BigQuery (SQL Views for data transformation).
* **ETL Pipeline:** Python (`src/etl_pipeline.py`) for automated data ingestion and schema detection.
* **Interactive Dashboard:** Streamlit.
* **Advanced Analytics:** Pandas, Scipy (T-Test), Seaborn.

## 📂 Project Structure

```text
game-lifecycle-analytics/
│
├── .streamlit/             # Application secrets (GCP Credentials)
│   └── app.py              # Main Dashboard Application
├── .venv/                  # Python Virtual Environment
├── assets/                 # Screenshots for Documentation
│   ├── game-health-overview.png
│   ├── daily-retention-curve.png
│   └── AB-testing-monetization.png
│   └── whale-analysis.png
├── data/                   # Data storage
│   ├── processed/
│   └── raw/                # Source CSV files
├── notebooks/              # Jupyter Notebooks for deep-dive analysis
│   └── advanced_game_analytics.ipynb
├── sql/                    # SQL Transformation Logic (BigQuery Views)
│   ├── 01_cleaning.sql
│   ├── 02_retention.sql
│   └── 03_monetization.sql
├── src/                    # Source Code
│   ├── __init__.py
│   └── etl_pipeline.py     # Script to load CSV to BigQuery
├── requirements.txt        # Project Dependencies
└── README.md               # Project Documentation

```

## 📊 Dashboard & Analytics Insights

### 1. Game Health Overview

The dashboard provides a real-time snapshot of the game's core performance metrics using BigQuery aggregations.

![Game Health Overview](https://github.com/kina2711/game-lifecycle-analytics/blob/main/assets/game-health-overview.png)

**💡 Key Insights:**

* **Scale:** The game has reached a milestone of **1,000,000 Users** with a total revenue of **~$9.7 Million**.
* **Monetization Challenge:** The overall Paying Rate is only **0.33%**, indicating that while user acquisition is strong, the conversion funnel needs significant optimization.
* **Growth Trend:** The "New Users Trend" chart shows exponential growth in user acquisition in recent years (2020+).

---

### 2. Retention Analysis (The "Drop-off" Curve)

We analyzed how well the game retains users over specific time intervals (every 10 days).

![Daily Retention Curve](https://github.com/kina2711/game-lifecycle-analytics/blob/main/assets/daily-retention-curve.png)

**💡 Key Insights:**

* **Steep Initial Churn:** There is a critical drop-off in the first 10 days. Retention falls from **100% (Day 0)** to **~5.1% (Day 10)**. This suggests significant friction during the **Onboarding Experience** or First-Time User Experience (FTUE).
* **Stabilization:** After Day 40, the curve flattens. The retention rate stabilizes around **1%**, representing the "Hardcore" player base that remains loyal long-term.

---

### 3. Monetization & A/B Testing Results

We conducted an A/B Test to compare two monetization strategies:

* **Group A (Control):** 202,103 users.
* **Group B (Test):** 202,667 users.

![A/B Testing & Monetization](https://github.com/kina2711/game-lifecycle-analytics/blob/main/assets/AB-testing-monetization.png)

**💡 Key Insights:**

* **Observed Data:** Group B showed a slightly higher ARPU (**$26.75**) compared to Group A (**$25.41**). However, Group B's conversion rate (**0.89%**) was lower than Group A (**0.95%**).
* **Statistical Significance (T-Test):** The P-Value returned is **0.533** (> 0.05).
* **Conclusion:** We **fail to reject the null hypothesis**. The difference in revenue between Group A and Group B is **not statistically significant** and is likely due to random chance.
* **Recommendation:** Do not roll out the Group B changes globally as they do not provide a guaranteed lift in revenue and negatively impact the conversion rate.

---

### 4. Whale Analysis (High-Value Users)

We defined "Whales" as the top **1%** of paying users to understand revenue concentration.

![Whale Analysis](https://github.com/kina2711/game-lifecycle-analytics/blob/main/assets/whale-analysis.png)

**💡 Key Insights:**

* **High Threshold:** To enter the Top 1% "Whale" club, a user must spend at least **$37,323**. This indicates an extremely high ceiling for individual spending.
* **Revenue Contribution:** This small group of elite players contributes **13.1%** (~$1.27M) of the total revenue.
* **Economy Balance:** Unlike many RPG/Gacha games where whales contribute 80-90% of revenue, this game has a relatively distributed economy (86.9% revenue comes from non-whales), reducing the risk of relying too heavily on a few individuals.

## 🚀 How to Run Locally

### Prerequisites

* Python 3.8+
* Google Cloud Platform Account (with BigQuery enabled)

### Step 1: Clone the Repository

```bash
git clone https://github.com/kina2711/game-lifecycle-analytics.git
cd game-lifecycle-analytics

```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt

```

### Step 3: Configure Credentials

Create a `.streamlit/secrets.toml` file and add your Google Service Account key:

```toml
[gcp_service_account]
project_id = "your-project-id"
private_key = "-----BEGIN PRIVATE KEY-----..."
client_email = "your-email@..."
# ... (other fields from your json key)

```

### Step 4: Launch the App

```bash
streamlit run app.py

```

## 👤 Author

**Thai Trung Kien (Rabbit)**
*Data Analyst / Analytics Engineer*

* **Email:** [kienthai2711@gmail.com](mailto:kienthai2711@gmail.com)
* **LinkedIn:** [linkedin.com/in/trungkienthai2711](https://www.linkedin.com/in/trungkienthai2711/)

---

*This project is created for educational purposes as part of a personal portfolio.*
