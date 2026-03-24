"""
Omer Attia
3/2/2026
Simple port scanner using Scapy. Scans ports 1-1024 on localhost
and prints which ones are open.
"""
import logging

from scapy.all import IP, TCP, conf, sr1

# Scan range
START_PORT: int = 1
END_PORT: int = 1024

# How long to wait for a response before giving up
TIMEOUT: float = 0.5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def scan_port(ip: str, port: int) -> bool:
    """Send a SYN packet to the given port, return True if it's open."""
    pkt = IP(dst=ip) / TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=TIMEOUT)

    # A SYN-ACK response (flags=0x12) means the port is open
    if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
        return True

    return False


def main() -> None:
    conf.verb = 0  # Suppress Scapy output
    ip: str = "127.0.0.1"

    logger.info("Starting scan on %s (ports %d-%d)", ip, START_PORT, END_PORT)

    open_ports: list[int] = []

    for port in range(START_PORT, END_PORT + 1):
        if scan_port(ip, port):
            logger.info("Port %d is open", port)
            open_ports.append(port)

    logger.info("Scan complete. Open ports: %s", open_ports)


if __name__ == "__main__":
    main()