Yes. At Read Committed, after an ordinary `SELECT` it will get its own snapshot. If another session commits changes between your two queries, your second query will be able to see it even though it's one query from one transaction.

Start a transaction with `ISOLATION_LEVEL REPEATABLE READ`:  `BEGIN ISOLATION LEVEL REPEATABLE READ;`.

Its snapshot is based on the query that initiates it, or any statement that modifies the data in the table. It doesn't have to be the first query or data-modification statement. The rest of the queries will only view information that has not been modified by transactions that are committed after the snapshot. They still see information that was modified before the snapshot, even if it was by their own transaction.

This gives the report a stable snapshot of the data in the table in those queries. See [transaction setup](https://www.postgresql.org/docs/17/sql-set-transaction.html).

If you later add an `UPDATE` with a conflicting committed value, there will be `serialization_failure` with SQLSTATE `40001`. Abort and retry the whole transaction. This includes all of the logic for selecting which statements to query, and values, so just retrying only the erroneous update is not enough. Repeated retries can fail with another conflict. See [retry handling](https://www.postgresql.org/docs/17/mvcc-serialization-failure-handling.html).

A Repeatable Read transaction still shows anomalies of serialization. Having a stable snapshot does not ensure results that match those of two concurrent transactions one at a time. See [transaction isolation](https://www.postgresql.org/docs/17/transaction-iso.html).