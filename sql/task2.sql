WITH ranked_features AS (
    SELECT email, feature, value_, amount,
        ROW_NUMBER() OVER(PARTITION BY email, feature ORDER BY amount DESC) AS rn
    FROM
        ranked_features
)
SELECT email, feature, value_, amount
FROM ranked_feature WHERE rn = 1;

