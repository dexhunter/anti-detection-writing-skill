`EXPOSE 8080` documents the intended container port; it does not publish a port on the host. Since your server already listens on the container's port 8080, run:

```sh
docker run -p 127.0.0.1:8080:8080 demo-web
```

Then open `http://127.0.0.1:8080`. This maps host loopback port 8080 to TCP port 8080 in the container. Keep `127.0.0.1` in the command: omitting it binds to all host addresses by default. With Docker Engine 28.0.0 or later and the default bridge/NAT and routing settings you described, the loopback binding restricts access to this published port to the host. See Docker's [port publishing documentation](https://docs.docker.com/engine/network/port-publishing/).
