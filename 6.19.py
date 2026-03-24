"""
Omer Attia
3/2/2026
Simple SYN port scanner using Scapy with threading. Sorry for the inconvenience.
What happend was that I forgot to publish this version on github sorry!
"""
import threading
from scapy.all import IP, TCP, sr1, conf

START_PORT: int = 1
END_PORT: int = 65535
TIMEOUT: float = 0.5
MAX_THREADS: int = 500

conf.verb = 0
print_lock = threading.Lock()
semaphore = threading.Semaphore(MAX_THREADS)


def scan_port(ip: str, port: int) -> None:
    with semaphore:
        resp = sr1(IP(dst=ip) / TCP(dport=port, flags="S"), timeout=TIMEOUT)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
            with print_lock:
                print(f"Port {port} is open!")


def main() -> None:
    ip = input("Enter IP address: ").strip()
    threads = [threading.Thread(target=scan_port, args=(ip, port))
               for port in range(START_PORT, END_PORT + 1)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Done.")


if __name__ == "__main__":
    main()