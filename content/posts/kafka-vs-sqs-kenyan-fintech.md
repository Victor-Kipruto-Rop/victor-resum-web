# Kafka vs SQS for a Kenyan Fintech with Intermittent Connectivity

Comparing Kafka and SQS for local fintechs:

- Kafka: great for high-throughput, low-latency systems; requires operational expertise and persistent brokers.
- SQS: managed, simpler but with limited ordering and delivery semantics.

When connectivity is intermittent:

- Prefer small durable local buffers with replay (Kafka or local disk buffer) and a robust retry/backoff strategy.
- Use SQS for simpler async workflows where exact ordering isn't critical.

Recommendation: start with SQS for lower ops cost, migrate to Kafka when ordering and throughput demands justify it.
