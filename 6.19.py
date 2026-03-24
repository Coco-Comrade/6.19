"""
Omer Attia
3/2/2026
Simple SYN port scanner using Scapy with threading.
Requires root/sudo privileges.
"""
import logging
import threading

from scapy.all import IP, TCP, conf, sr1

START_PORT: int = 1
END_PORT: int = 65535
TIMEOUT: float = 0.5
MAX_THREADS: int = 500

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def scan_port(ip: str, port: int, semaphore: threading.Semaphore) -> None:
    """Send a SYN packet and log the port if a SYN-ACK is received."""
    with semaphore:
        logger.debug("Scanning port %d", port)
        pkt = IP(dst=ip) / TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=TIMEOUT)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
            logger.info("Port %d is open", port)


def main() -> None:
    """Prompt for an IP address and scan all ports using threads."""
    conf.verb = 0

    ip: str = input("Enter IP address: ").strip()
    logger.info("Starting scan on %s (ports %d-%d)", ip, START_PORT, END_PORT)

    semaphore = threading.Semaphore(MAX_THREADS)
    threads = [
        threading.Thread(target=scan_port, args=(ip, port, semaphore))
        for port in range(START_PORT, END_PORT + 1)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    logger.info("Scan complete.")


if __name__ == "__main__":
    main()
