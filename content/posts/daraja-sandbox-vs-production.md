# Daraja Sandbox vs Production: The Gotchas Nobody Documents

This note collects behavioral differences between Daraja sandbox and production environments:

- Sandbox may not simulate latency and retry behaviors accurately
- Test credentials and callback endpoints are different; ensure callback validation logic adapts
- Some APIs have stricter rate limits in production

Checklist before cutover:

1. Validate certificate and callback URL handling
2. Run traffic with a staged domain and monitor retries
3. Ensure logging and alerts are in place for failed callbacks
