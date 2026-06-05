WITH merchant_stats AS (
    SELECT
        t.merchant_id,
        m.merchant_name,
        m.category,
        m.city,

        COUNT(*) AS total_txns,

        COUNT(
            CASE
                WHEN t.is_fraud = TRUE THEN 1
            END
        ) AS fraud_txns,

        ROUND(AVG(t.amount), 2) AS avg_txn_amount,

        m.refund_rate_pct,
        m.chargeback_count,
        m.registration_days,

        ROUND(
            COUNT(
                CASE
                    WHEN t.is_fraud = TRUE THEN 1
                END
            ) * 100.0 / COUNT(*),
            2
        ) AS merchant_fraud_rate

    FROM upi_transactions t
    JOIN merchant_profiles m
        ON t.merchant_id = m.merchant_id

    GROUP BY
        t.merchant_id,
        m.merchant_name,
        m.category,
        m.city,
        m.refund_rate_pct,
        m.chargeback_count,
        m.registration_days
),

merchant_scored AS (

    SELECT *,

        ROUND(
            (
                merchant_fraud_rate /
                NULLIF(MAX(merchant_fraud_rate) OVER(),0)
            ) * 50

            +

            (
                refund_rate_pct /
                NULLIF(MAX(refund_rate_pct) OVER(),0)
            ) * 30

            +

            (
                chargeback_count /
                NULLIF(MAX(chargeback_count) OVER(),0)
            ) * 20

        ,1) AS merchant_risk_score

    FROM merchant_stats
)

SELECT
    RANK() OVER (
        ORDER BY merchant_risk_score DESC
    ) AS risk_rank,

    merchant_name,
    category,
    city,
    total_txns,
    fraud_txns,
    merchant_fraud_rate,
    refund_rate_pct,
    chargeback_count,
    merchant_risk_score

FROM merchant_scored
ORDER BY risk_rank
LIMIT 20;