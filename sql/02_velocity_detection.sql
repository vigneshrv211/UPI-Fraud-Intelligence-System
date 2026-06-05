WITH txn_velocity AS (
    SELECT
        txn_id,
        user_id,
        txn_timestamp,
        amount,

        COUNT(*) OVER (
            PARTITION BY user_id
            ORDER BY txn_timestamp
            RANGE BETWEEN INTERVAL '60 minutes' PRECEDING
            AND CURRENT ROW
        ) AS txn_count_last_1h

    FROM upi_transactions
)

SELECT *
FROM txn_velocity
ORDER BY txn_count_last_1h DESC;