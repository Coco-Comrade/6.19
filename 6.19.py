"""
Omer Attia
3/2/2026
Port scanner using socket-based TCP connect scan (single-threaded).
Auto-detects and scans the local machine's IP address.
"""
import logging
import socket

START_PORT: int = 1
END_PORT: int = 1024
TIMEOUT: float = 0.5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_local_ip() -> str:
    """Automatically detect the local machine's IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def scan_port(ip: str, port: int) -> bool:
    """Attempt a TCP connection; return True if port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            return s.connect_ex((ip, port)) == 0
    except OSError:
        return False


def main() -> None:
    ip = get_local_ip()
    logger.info("Detected local IP: %s", ip)
    logger.info("Starting scan on %s (ports %d-%d)", ip, START_PORT, END_PORT)

    open_ports = []
    for port in range(START_PORT, END_PORT + 1):
        if scan_port(ip, port):
            logger.info("Port %d is open", port)
            open_ports.append(port)

    logger.info("Scan complete. Open ports: %s", open_ports)


if __name__ == "__main__":
    main()