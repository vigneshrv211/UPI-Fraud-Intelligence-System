WITH user_baselines AS (
    SELECT
        user_id,
        round(AVG(amount),2) AS mean_amt,
        round(STDDEV(amount),2) AS std_amt
    FROM upi_transactions
    GROUP BY user_id
),
anomaly_check AS (
    SELECT
        t.txn_id,
        t.user_id,
        t.amount,
        b.mean_amt,
        b.std_amt,
        ROUND(((t.amount - b.mean_amt)/NULLIF(b.std_amt,0))::numeric,2) AS amount_zscore
    FROM upi_transactions t
    JOIN user_baselines b
        ON t.user_id = b.user_id
)
SELECT *
FROM anomaly_check
where amount_Zscore > 3
ORDER BY amount_zscore DESC;