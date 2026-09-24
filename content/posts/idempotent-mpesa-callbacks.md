# Building an Idempotent M-Pesa Callback Handler

When integrating with Safaricom's Daraja, one of the most important operational considerations is handling retries and duplicate callbacks. This article explains patterns to make your callback handler idempotent and resilient.

## Why Safaricom Retries Happen

Safaricom may retry webhooks when it does not receive an HTTP 200 response, or when it observes a network error. Retrying is necessary but can lead to duplicate processing unless handled carefully.

## Idempotency Strategies

- Use a durable deduplication store keyed by the transaction ID (e.g., `ConversationID` or `TransactionReceipt`).
- Persist a processing status (received / processing / completed / failed) and use conditional updates to prevent double-processing.
- Use database transactions and optimistic concurrency to ensure only one successful commit wins.

## Example: PostgreSQL upsert pattern

```sql
INSERT INTO mpesa_callbacks(id, payload, status)
VALUES($1, $2, 'received')
ON CONFLICT(id) DO UPDATE SET payload = EXCLUDED.payload
RETURNING status;
```

## Defensive coding

- Treat duplicate notifications as no-ops if the ledger already reflects the transaction.
- Emit events for any unexpected state transitions and alert on them.

## Conclusion

Idempotency is both a design and operational concern. With a small set of patterns, durable keys, conditional updates, and clear status transitions, you can make Daraja callbacks safe to retry.
