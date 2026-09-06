A request hook cannot guarantee a fresh timestamp when bytes reach the server. In HTTPX 0.28.1, the hook runs before the client enters the transport; connection acquisition happens later in httpcore. A signature created in the hook can age during that wait.

Limit application concurrency before entering HTTPX so admission waiting happens before signing. Set a short [pool timeout](https://www.python-httpx.org/advanced/timeouts/#fine-tuning-the-configuration) to bound each wait for an available connection. After `PoolTimeout`, retry only if the operation and request body are safe to repeat, and create and sign a fresh attempt.

The pool timeout does not bound the full interval from signing to server receipt. Connection setup, TLS, writes and internal reacquisition can add time. Signing strictly after pool acquisition requires a service-specific transport design; the public request hook alone cannot provide it.

This explanation follows the [client implementation](https://github.com/encode/httpx/blob/0.28.1/httpx/_client.py). It does not reproduce or establish the cause of the reported high-volume 401s.
