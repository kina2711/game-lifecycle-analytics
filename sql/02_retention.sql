CREATE OR REPLACE VIEW `game-lifecycle-analytics.game_lifecycle_analytics.vw_daily_retention_curve` AS
WITH user_activity AS (
    SELECT 
        t1.uid,
        DATE_DIFF(DATE(TIMESTAMP_SECONDS(t2.auth_ts)), DATE(TIMESTAMP_SECONDS(t1.reg_ts)), DAY) as days_since_reg
    FROM `game-lifecycle-analytics.game_lifecycle_analytics.reg_data` t1
    JOIN `game-lifecycle-analytics.game_lifecycle_analytics.auth_data` t2 ON t1.uid = t2.uid
    WHERE t2.auth_ts >= t1.reg_ts -- Chỉ lấy log sau khi đăng ký
),
daily_stats AS (
    SELECT 
        days_since_reg,
        COUNT(DISTINCT uid) as retained_users
    FROM user_activity
    GROUP BY 1
),
total_users AS (
    SELECT COUNT(DISTINCT uid) as total_count 
    FROM `game-lifecycle-analytics.game_lifecycle_analytics.reg_data`
)
SELECT 
    d.days_since_reg,
    d.retained_users,
    t.total_count,
    -- Tính % Retention: (User còn lại / Tổng User ban đầu) * 100
    ROUND((d.retained_users / t.total_count) * 100,2) as retention_percent
FROM daily_stats d
CROSS JOIN total_users t
ORDER BY 1;
