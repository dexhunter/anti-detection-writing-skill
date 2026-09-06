TLS uses the connect timeout, but it is a separate timeout scope from TCP connection establishment. In httpcore 1.0.9, both operations receive the configured `connect` value; setup can therefore exceed that value in total, and configured connection retries can extend it further.

DNS depends on the network backend. The [AnyIO backend](https://github.com/encode/httpcore/blob/1.0.9/httpcore/_backends/anyio.py) wraps its connection operation, including resolution, in `anyio.fail_after(timeout)`. That bounds the async operation's wait; it does not promise to stop every underlying resolver activity.

The synchronous backend uses `socket.create_connection()`. CPython resolves the hostname before applying the socket timeout to connection attempts, so a blocking resolver is not reliably bounded by that setting. Custom backends can differ too.

HTTPX does not expose a separate DNS timeout in its [timeout configuration](https://www.python-httpx.org/advanced/timeouts/). If you need an overall deadline, it must cover the appropriate backend and all setup stages; the connect value is not one shared end-to-end timer. These are source-inspected behaviors, not measurements of a stalled DNS server or TLS handshake.
