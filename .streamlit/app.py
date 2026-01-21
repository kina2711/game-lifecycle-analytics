import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Game Lifecycle Analytics", page_icon="🎮", layout="wide")

# --- 2. DATA LOADER ---
@st.cache_data
def load_raw_data():
    base_path = "../data/raw/"

    # Đọc CSV với dấu chấm phẩy (;)
    try:
        df_reg = pd.read_csv(os.path.join(base_path, "reg_data.csv"), sep=';')
        df_auth = pd.read_csv(os.path.join(base_path, "auth_data.csv"), sep=';')
        df_ab = pd.read_csv(os.path.join(base_path, "ab_test.csv"), sep=';')
    except Exception as e:
        st.error(f"❌ Lỗi đọc file: {e}")
        st.stop()

    # --- XỬ LÝ QUAN TRỌNG: TIME CONVERSION ---
    # Ép kiểu về numeric để tránh lỗi string, sau đó convert từ Unix Seconds -> Datetime
    df_reg['reg_ts'] = pd.to_numeric(df_reg['reg_ts'], errors='coerce')
    df_auth['auth_ts'] = pd.to_numeric(df_auth['auth_ts'], errors='coerce')

    df_reg['reg_date'] = pd.to_datetime(df_reg['reg_ts'], unit='s').dt.date
    df_auth['auth_date'] = pd.to_datetime(df_auth['auth_ts'], unit='s').dt.date

    # Merge bảng Master
    df_master = pd.merge(df_reg, df_ab, on='uid', how='left')
    df_master['revenue'] = df_master['revenue'].fillna(0)
    df_master['testgroup'] = df_master['testgroup'].fillna('unknown')

    return df_reg, df_auth, df_master

# Load Data
df_reg, df_auth, df_master = load_raw_data()

# --- 3. SIDEBAR ---
st.sidebar.title("🎮 Game Analytics")
st.sidebar.info("**Author:** Rabbit (Thai Trung Kien)\n\n**Data Source:** Kaggle Game Analytics")

# --- 4. DASHBOARD TABS ---
tab1, tab2, tab3 = st.tabs(["📈 Overview", "🔄 Retention", "💰 Monetization"])

with tab1:
    st.header("Game Health Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", f"{df_master['uid'].nunique():,}")
    col2.metric("Total Revenue", f"${df_master['revenue'].sum():,.0f}")
    col3.metric("Paying User Rate", f"{(df_master[df_master['revenue'] > 0].shape[0] / df_master.shape[0]) * 100:.2f}%")

    # Biểu đồ User mới theo ngày
    daily_users = df_master.groupby('reg_date')['uid'].count().reset_index()
    fig = px.line(daily_users, x='reg_date', y='uid', title="New Users Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Cohort Retention Analysis")

    # Logic tính Retention chuẩn Pandas
    # Bước 1: Join Auth với Reg để lấy ngày đăng ký của từng lần đăng nhập
    merged = pd.merge(df_auth, df_reg[['uid', 'reg_date']], on='uid', how='inner')

    # Bước 2: Tính số ngày quay lại (Auth Date - Reg Date)
    merged['day_diff'] = (pd.to_datetime(merged['auth_date']) - pd.to_datetime(merged['reg_date'])).dt.days

    # Bước 3: Chỉ lấy các mốc quan trọng (Day 0, 1, 3, 7, 14, 30)
    cohort_days = [0, 1, 3, 7, 14, 30]
    retention_data = merged[merged['day_diff'].isin(cohort_days)]

    # Bước 4: Đếm số user unique theo từng cohort và day_diff
    cohort_counts = retention_data.groupby(['reg_date', 'day_diff'])['uid'].nunique().reset_index()

    # Bước 5: Pivot bảng
    cohort_pivot = cohort_counts.pivot(index='reg_date', columns='day_diff', values='uid')

    # Bước 6: Tính % Retention (Chia cho cột Day 0)
    cohort_size = cohort_pivot[0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)

    # Vẽ Heatmap
    fig_heat = px.imshow(retention_matrix, text_auto='.1%', color_continuous_scale='RdBu', aspect="auto")
    st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    st.header("A/B Testing: Monetization")

    # Group theo nhóm A/B
    ab_stats = df_master.groupby('testgroup').agg(
        Users=('uid', 'count'),
        Revenue=('revenue', 'sum'),
        Paying_Users=('revenue', lambda x: (x > 0).sum())
    ).reset_index()

    ab_stats['ARPU'] = ab_stats['Revenue'] / ab_stats['Users']
    st.dataframe(ab_stats.style.format({'Revenue': '${:,.2f}', 'ARPU': '${:.4f}'}))

    # T-Test kiểm định thống kê
    st.subheader("Statistical Test (T-Test)")
    group_a = df_master[df_master['testgroup'] == 'a']['revenue']
    group_b = df_master[df_master['testgroup'] == 'b']['revenue']

    t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)
    st.write(f"**P-Value:** {p_val:.5f}")
    if p_val < 0.05:
        st.success("✅ Kết quả có ý nghĩa thống kê (Significant Difference).")
    else:
        st.warning("⚠️ Kết quả ngẫu nhiên, không có ý nghĩa thống kê.")