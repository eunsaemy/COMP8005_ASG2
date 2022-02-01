# COMP8005_ASG2

## COMP 8005 - Assignment 2

A secure chat client/server application with SSL network communications. The server accepts connections on a specified port and echoes whatever it receives to all other connected clients.

### To run server.py:

python server.py

### To run client.py:

python client.py

### To run client2.py:

python client2.py

### SSL Socket Client/Server Examples

- [SSL Socket](https://gist.github.com/Oborichkin/d8d0c7823fd6db3abeb25f69352a5299)
- [Generate SSL Keys using OpenSSL](https://www.cockroachlabs.com/docs/stable/create-security-certificates-openssl.html)

```sh
openssl req -newkey rsa:2048 -nodes -keyout privkey.pem -x509 -days 36500 -out certificate.pem
```
