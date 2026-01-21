CREATE OR REPLACE VIEW `game-lifecycle-analytics.game_lifecycle_analytics.vw_ab_test_results` AS
SELECT
    testgroup,
    COUNT(uid) as total_users,
    COUNTIF(revenue > 0) as paying_users,
    SUM(revenue) as total_revenue,
    SUM(revenue) / COUNT(uid) as ARPU,
    SUM(revenue) / NULLIF(COUNTIF(revenue > 0), 0) as ARPPU
FROM `game-lifecycle-analytics.game_lifecycle_analytics.ab_test`
GROUP BY testgroup;