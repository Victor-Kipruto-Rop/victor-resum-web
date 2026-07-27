# What Breaks When You Scale a Daraja Integration from 100 to 100k Transactions/Day

Scaling Daraja integrations introduces challenges around:

- Endpoint throughput and callback concurrency
- Retry storm behavior from Safaricom
- Database locks and idempotency at scale

Mitigations:

- Use queue-based ingestion and processing workers
- Separate callback acknowledgement from business processing
- Scale reads and writes independently with sharding and partitioning
