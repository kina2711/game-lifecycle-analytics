CREATE OR REPLACE VIEW `game-lifecycle-analytics.game_lifecycle_analytics.vw_master_user_stats` AS
SELECT
    t1.uid,
    TIMESTAMP_SECONDS(t1.reg_ts) AS reg_datetime,
    DATE(TIMESTAMP_SECONDS(t1.reg_ts)) AS reg_date,
    t2.testgroup,
    COALESCE(t2.revenue, 0) AS total_revenue
FROM `game-lifecycle-analytics.game_lifecycle_analytics.reg_data` t1
LEFT JOIN `game-lifecycle-analytics.game_lifecycle_analytics.ab_test` t2 ON t1.uid = t2.user_id;