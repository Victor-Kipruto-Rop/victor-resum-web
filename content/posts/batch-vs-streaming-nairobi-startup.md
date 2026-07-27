# Batch vs Streaming: When a Nairobi Startup Should Use Flink

Streaming is attractive but brings operational cost. Criteria to choose Flink:

- Need real-time SLA (< 1s) or continuous aggregation
- High event throughput where latency matters
- Stateful event processing with windowing semantics

Otherwise, batch + micro-batch pipelines are simpler and cheaper. Consider hybrid approaches.
