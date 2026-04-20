# python-network-client-server
Python client-server networking project supporting TCP, UDP, multicast and broadcast communication over IPv4 and IPv6.
This project is a simple networking application written in Python.

It includes a server and a client that support:

- TCP communication
- UDP communication
- IPv4 and IPv6
- multicast messaging
- broadcast messaging

## Files

- `server.py` – starts the TCP, UDP, multicast and broadcast receivers
- `client.py` – allows the user to connect and send messages using different modes

## Features

- TCP echo communication
- UDP message exchange
- IPv4 and IPv6 support
- multicast sender/receiver
- broadcast sender/receiver
- basic multithreading on the server side

## How to run

### Run the server
```bash id="umtbfr"
python server.py
