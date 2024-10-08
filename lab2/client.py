import socket

from util import convert_proto, get_args


def main() -> None:
    args = get_args()

    with socket.socket(socket.AF_INET, convert_proto(args.PROTO)) as s:
        s.connect((args.HOST, args.PORT))
        s.sendall(bytes(args.MESSAGE, "utf-8"))
        data = s.recv(1024)

    print("Data received: ", repr(data))


if __name__ == "__main__":
    main()
