import argparse
import socket
from typing import NamedTuple


class Args(NamedTuple):
    HOST: str
    PORT: int
    PROTO: str
    MESSAGE: str


def convert_proto(proto: str) -> socket.SocketKind:
    return {
        "tcp": socket.SOCK_STREAM,
        "udp": socket.SOCK_DGRAM,
    }[proto]


def get_args() -> Args:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="IP-address for connection, default is 0.0.0.0",
    )
    parser.add_argument(
        "--port", type=int, default=52025, help="Port for connection, default is 52025"
    )
    parser.add_argument(
        "--proto",
        type=str,
        choices=["tcp", "udp"],
        required=True,
        help="Protocol for connection, allowed tcp or udp values",
    )
    parser.add_argument(
        "-m", "--message", type=str, default="", help="Message to send from client"
    )

    args = parser.parse_args()
    return Args(HOST=args.host, PORT=args.port, PROTO=args.proto, MESSAGE=args.message)
