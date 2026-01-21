CREATE OR REPLACE VIEW `game-lifecycle-analytics.game_lifecycle_analytics.vw_daily_retention` AS
WITH cohort AS (
    SELECT uid, DATE(TIMESTAMP_SECONDS(reg_ts)) as cohort_date
    FROM `game-lifecycle-analytics.game_lifecycle_analytics.reg_data`
),
activity AS (
    SELECT uid, DATE(TIMESTAMP_SECONDS(auth_ts)) as activity_date
    FROM `game-lifecycle-analytics.game_lifecycle_analytics.auth_data`
)
SELECT
    c.cohort_date,
    DATE_DIFF(a.activity_date, c.cohort_date, DAY) as day_diff,
    COUNT(DISTINCT c.uid) as user_count
FROM cohort c
JOIN activity a ON c.uid = a.uid
WHERE a.activity_date >= c.cohort_date
GROUP BY 1, 2
ORDER BY 1, 2;