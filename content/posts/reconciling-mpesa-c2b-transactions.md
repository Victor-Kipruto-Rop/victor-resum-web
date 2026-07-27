# Reconciling M-Pesa C2B Transactions Against Your Ledger at Scale

Reconciling C2B transactions at scale requires careful batching, idempotency, and eventually-consistent design.

Key techniques:

- Partition reconciliation jobs by merchant or date to parallelize work
- Use a high-throughput dedupe index for transaction receipts
- Keep reconciliation logs separate from the primary ledger for visibility

Operational tips:

- Provide a manual reconciliation CLI for edge cases
- Track reconciliation latency as a metric and alert on increases
