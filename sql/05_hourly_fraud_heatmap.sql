SELECT
    txn_hour,
    txn_day_of_week,

    COUNT(*) AS total_txns,

    COUNT(
        CASE
            WHEN is_fraud = TRUE THEN 1
        END
    ) AS fraud_txns,

    ROUND(
        COUNT(
            CASE
                WHEN is_fraud = TRUE THEN 1
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate_pct,

    ROUND(AVG(amount), 2) AS avg_amount

FROM upi_transactions

GROUP BY
    txn_hour,
    txn_day_of_week

ORDER BY
    txn_hour,
    txn_day_of_week;