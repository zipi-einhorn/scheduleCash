
--  By placing "deleted = 0" before "documents.creationTime > 01.04.2024,"
--  the query filters out records with "deleted = 0" first.
--  This reduces the number of records that need to be processed further,
--  potentially improving overall query performance.
where deleted = 0 and documents.creationTime > 01.04.2024
-- Creating an index on the "deleted" and "creationTime" columns,
-- as demonstrated by "CREATE INDEX idx_multi_column ON table_name (deleted, creationTime);
-- ," can speed up data retrieval. Indexing allows the database to quickly locate relevant records based on
-- the indexed columns, resulting in faster query execution.
CREATE INDEX idx_multi_column ON table_name (deleted, creationTime);
-- The use of the EXISTS clause in the query ensures that only records meeting the specified conditions
-- are considered. This prevents unnecessary scans of columns where the condition does not apply,
-- leading to more efficient query processing
SELECT d.*
FROM buyPrice.documents AS d
WHERE EXISTS (
    SELECT 1
    FROM BuyPrice.routes AS r
    WHERE r.document_id = d.id AND r.deleted = 0 AND r.creationTime > '2024-04-01'
);



