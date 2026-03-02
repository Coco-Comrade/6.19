"""
Omer Attia
3/2/2026
This script demonstrates a simple TCP connectivity check using Python's
standard library. It attempts to connect to a specified IP address and
port range and reports which ports accept a full TCP connection. This
example is for educational use on networks you own or have permission
to test.
"""

from typing import Optional
import socket


START_PORT: int = 20
END_PORT: int = 1024
TIMEOUT: float = 0.5


def is_port_open(ip_address: str, port: int) -> bool:
    """Return True if a TCP connection can be established."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        try:
            sock.connect((ip_address, port))
            return True
        except (socket.timeout, OSError):
            return False


def main() -> None:
    """Prompt for an IP address and scan a port range."""
    ip_address: str = input("Type an IP address:\n").strip()

    for port in range(START_PORT, END_PORT + 1):
        if is_port_open(ip_address, port):
            print(f"The port {port} is open!")

    print("Done.")


if __name__ == "__main__":
    main()