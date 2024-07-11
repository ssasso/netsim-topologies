# Edgeshark integration

**Edgeshark** is Web UI that displays every interface of every container and can start a wireshark session by a click of a button.

That means it is capable of capturing traffic from any interface in your virtual lab. Moreover, it plugs into wireshark natively, using an installable extension (see below).

## Start Edgeshark

From this directory, execute:

```
docker compose up -d
```

This will deploy the edgeshark containers and expose the Web UI on the host's port *8080*: you can open the Web UI (`http://<host-address>:8080`) in your browser and see the Edgeshark UI.

## Stop Edgeshark

From this directory, execute:

```
docker compose down
```

## Wireshark extension

There is a small price one needs to pay to make integrate Edgeshark with Wireshark:

* Download and install wireshark
* Download and install the client agent, that can be found at: https://github.com/siemens/cshargextcap/releases/tag/v0.10.7

This will allow you to remotely perform live capture of the traffic flows just clicking on a WebUI button.
