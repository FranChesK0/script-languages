import socket

from util import Args, convert_proto, get_args


def get_log_message(ip: str, port: str, proto: str, data: str) -> str:
    return f"Data received from {ip}:{port} via {proto}: {data}"


def tcp_server(s: socket.socket, args: Args) -> None:
    s.listen(1)

    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        conn.sendall(data)
        print(get_log_message(addr[0], addr[1], args.PROTO, repr(data)))


def udp_server(s: socket.socket, args: Args) -> None:
    bytesAddr = s.recvfrom(1024)
    data = bytesAddr[0]
    addr = bytesAddr[1]
    s.sendto(data, addr)
    print(get_log_message(addr[0], addr[1], args.PROTO, repr(data)))


def main() -> None:
    args = get_args()

    with socket.socket(socket.AF_INET, convert_proto(args.PROTO)) as s:
        s.bind((args.HOST, args.PORT))
        if args.PROTO == "tcp":
            tcp_server(s, args)
        else:
            udp_server(s, args)


if __name__ == "__main__":
    main()
