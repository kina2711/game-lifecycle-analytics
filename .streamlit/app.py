import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px
from scipy import stats

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Game Lifecycle Analytics", page_icon="🎮", layout="wide")

# Lấy thông tin Project ID từ secrets
try:
    PROJECT_ID = st.secrets["gcp_service_account"]["project_id"]
    DATASET_ID = "game_lifecycle_analytics"
except:
    st.error("Chưa cấu hình secrets.toml hoặc thiếu Project ID.")
    st.stop()

# --- 2. BIGQUERY CONNECTION ---
@st.cache_resource
def get_bq_client():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return bigquery.Client(credentials=creds, project=creds.project_id)

@st.cache_data(ttl=3600)
def run_query(query):
    client = get_bq_client()
    return client.query(query).to_dataframe()

# --- 3. SIDEBAR ---
st.sidebar.title("🎮 Game Analytics")
st.sidebar.caption(f"Source: `{PROJECT_ID}.{DATASET_ID}`")
st.sidebar.info("**Analyst:** Rabbit (Thai Trung Kien)\n\n**Tech:** BigQuery + Streamlit")

# --- 4. DATA PROCESSING (SQL LOGIC) ---
tab1, tab2, tab3 = st.tabs(["📈 Overview", "🔄 Retention", "💰 Monetization"])

# === TAB 1: OVERVIEW ===
with tab1:
    st.header("Game Health Overview")

    # Query tổng hợp:
    sql_overview = f"""
        SELECT 
            COUNT(DISTINCT t1.uid) as total_users,
            SUM(t2.revenue) as total_revenue,
            COUNT(DISTINCT CASE WHEN t2.revenue > 0 THEN t1.uid END) as paying_users
        FROM `{PROJECT_ID}.{DATASET_ID}.reg_data` t1
        LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.ab_test` t2 ON t1.uid = t2.user_id
    """
    df_overview = run_query(sql_overview)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", f"{df_overview['total_users'][0]:,}")
    col2.metric("Total Revenue", f"${df_overview['total_revenue'][0]:,.0f}")
    if df_overview['total_users'][0] > 0:
        rate = (df_overview['paying_users'][0] / df_overview['total_users'][0]) * 100
        col3.metric("Paying Rate", f"{rate:.2f}%")

    st.divider()

    # Biểu đồ User mới
    sql_trend = f"""
        SELECT 
            DATE(TIMESTAMP_SECONDS(reg_ts)) as reg_date,
            COUNT(uid) as new_users
        FROM `{PROJECT_ID}.{DATASET_ID}.reg_data`
        GROUP BY 1 ORDER BY 1
    """
    df_trend = run_query(sql_trend)
    fig_trend = px.line(df_trend, x='reg_date', y='new_users', markers=True,
                        title="New Users Trend", template="plotly_dark")
    st.plotly_chart(fig_trend, use_container_width=True)

# === TAB 2: RETENTION ===
with tab2:
    st.header("Daily Retention Curve")
    st.markdown("Tỷ lệ người dùng quay lại theo số ngày sau khi đăng ký (Chu kỳ 10 ngày).")

    # Query lấy toàn bộ dữ liệu retention theo ngày
    sql_retention = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.vw_daily_retention_curve`
        ORDER BY days_since_reg
    """
    
    try:
        df_ret = run_query(sql_retention)
        
        if not df_ret.empty:
            # 1. Lọc theo chu kỳ 10 ngày (0, 10, 20, 30...)
            # Logic: Lấy dòng mà days_since_reg chia hết cho 10
            df_filtered = df_ret[df_ret['days_since_reg'] % 10 == 0].reset_index(drop=True)
            
            # Chỉ lấy 38 mốc đầu tiên
            df_display = df_filtered.head(38)

            # 2. Hiển thị Table
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                st.subheader("Data Table")
                st.dataframe(
                    df_display[['days_since_reg', 'retention_percent']].style.format({
                        'retention_percent': '{:.4f}%'
                    }),
                    height=500
                )
            
            # 3. Hiển thị Chart (Retention Curve)
            with col_right:
                st.subheader("Retention Chart")
                # Vẽ biểu đồ đường
                fig_line = px.line(
                    df_display, 
                    x='days_since_reg', 
                    y='retention_percent',
                    markers=True,
                    title="Retention Rate (%) over Time",
                    labels={'days_since_reg': 'Days Since Registration', 'retention_percent': 'Retention (%)'}
                )
                fig_line.update_traces(line_color='#1f77b4', marker=dict(size=8))
                st.plotly_chart(fig_line, use_container_width=True)
                
        else:
            st.warning("Chưa có dữ liệu Retention.")
            
    except Exception as e:
        st.error(f"Lỗi truy vấn SQL: {e}")

# === TAB 3: MONETIZATION ===
with tab3:
    st.header("A/B Testing & Monetization")

    # Query A/B Test:
    sql_ab = f"""
        SELECT 
            testgroup,
            COUNT(user_id) as users,
            SUM(revenue) as total_rev,
            COUNTIF(revenue > 0) as paying_users
        FROM `{PROJECT_ID}.{DATASET_ID}.ab_test`
        GROUP BY 1
    """
    df_ab = run_query(sql_ab)

    df_ab['ARPU'] = df_ab['total_rev'] / df_ab['users']
    df_ab['ARPPU'] = df_ab['total_rev'] / df_ab['paying_users']
    df_ab['Conv_Rate'] = (df_ab['paying_users'] / df_ab['users']) * 100

    st.dataframe(df_ab.style.format({
        'total_rev': '${:,.2f}', 'ARPU': '${:.4f}', 'ARPPU': '${:.2f}', 'Conv_Rate': '{:.2f}%'
    }))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(df_ab, x='testgroup', y='ARPU', color='testgroup', title="ARPU", text_auto='.4f'),
                        use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(df_ab, x='testgroup', y='Conv_Rate', color='testgroup', title="Conversion Rate (%)",
                               text_auto='.2f'), use_container_width=True)

    st.divider()

    # --- T-TEST ---
    if st.button("Chạy kiểm định T-Test"):
        with st.spinner("Đang tính toán..."):
            # Lấy mẫu revenue theo group
            sql_ttest = f"SELECT testgroup, revenue FROM `{PROJECT_ID}.{DATASET_ID}.ab_test`"
            df_raw_test = run_query(sql_ttest)

            group_a = df_raw_test[df_raw_test['testgroup'] == 'a']['revenue']
            group_b = df_raw_test[df_raw_test['testgroup'] == 'b']['revenue']

            t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)

            st.write(f"**P-Value:** {p_val:.5f}")
            if p_val < 0.05:
                st.success(f"✅ Kết quả có ý nghĩa thống kê.")
            else:
                st.warning("⚠️ Kết quả ngẫu nhiên.")
