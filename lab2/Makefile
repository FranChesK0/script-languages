.PHONY: tcp-server
tcp-server:
	python ./server.py --host 127.0.0.1 --proto tcp

.PHONY: tcp-client
tcp-client:
	python ./client.py --host 127.0.0.1 --proto tcp --message="Hello World!"

.PHONY: udp-server
udp-server:
	python ./server.py --host 127.0.0.1 --proto udp

.PHONY: udp-client
udp-client:
	python ./client.py --host 127.0.0.1 --proto udp --message="Hello World!"
