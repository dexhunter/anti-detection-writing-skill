Your two report queries can see different committed data in the same Read Committed transaction. Each ordinary `SELECT` gets a new snapshot, so a commit between the queries can appear in the second result.

For a stable view across the report queries, start the transaction this way before running them:

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
```

The first query or data-modification statement establishes the Repeatable Read snapshot; `BEGIN` alone does not. Queries then exclude later commits by other transactions, while still seeing any earlier writes from their own transaction. See [transaction setup](https://www.postgresql.org/docs/17/sql-set-transaction.html).

That stable view does not guarantee a result equivalent to running concurrent transactions one at a time. Repeatable Read still permits serialization anomalies. See the [isolation documentation](https://www.postgresql.org/docs/17/transaction-iso.html).

If you later add an `UPDATE`, a conflicting committed update can cause `serialization_failure` with SQLSTATE `40001`. Abort and retry the whole transaction, including the logic that chose the statements and values; retrying only the failed update is insufficient. A retry can encounter another conflict. See [retry handling](https://www.postgresql.org/docs/17/mvcc-serialization-failure-handling.html).