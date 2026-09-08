Your server is already listening on port 8080 inside the container. To reach it from the host at `http://127.0.0.1:8080`, run:

```sh
docker run -p 127.0.0.1:8080:8080 demo-web
```

This maps host loopback port 8080 to container port 8080. With the Engine 28+ default bridge configuration you described, the published port is available only from the host. Keep `127.0.0.1` in the mapping: omitting the address publishes on all host interfaces by default.

The Dockerfile's `EXPOSE 8080` does not create this mapping; it only documents the intended container port. See [Docker's port-publishing documentation](https://docs.docker.com/engine/network/port-publishing/).