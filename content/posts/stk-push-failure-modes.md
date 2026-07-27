# STK Push Failure Modes and Designing for Production

STK Push is a powerful flow, but there are several failure modes you should design for:

- Timeout or no response from the customer's phone
- User cancels the payment at the prompt
- Network errors between Safaricom and your callback endpoint
- Duplicate or delayed callbacks

Design patterns:

- Immediate client-side acknowledgement and background reconciliation
- Exponential backoff for retries in the reconciliation job
- Clear SLA expectations and compensating transactions when necessary

Example: mark STK push as `pending` and reconcile with a background job that queries the transaction status after 30s, 5m, and 1h.
