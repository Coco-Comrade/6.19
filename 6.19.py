"""
Omer Attia
3/2/2026
This script demonstrates a simple TCP connectivity check using Python's
standard library. It attempts to connect to a specified IP address and
port range and reports which ports accept a full TCP connection. This
example is for educational use on networks you own or have permission
to test. Utilizes threading in order to make the process faster.
"""
import socket
import threading

START_PORT: int = 1
END_PORT: int = 65535
TIMEOUT: float = 0.5
MAX_THREADS: int = 500

print_lock = threading.Lock()

def is_port_open(ip_address: str, port: int) -> bool:
    """Return True if a TCP connection can be established."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        try:
            sock.connect((ip_address, port))
            return True
        except (socket.timeout, OSError):
            return False

def scan_port(ip_address: str, port: int) -> None:
    """Scan a single port and print if open."""
    if is_port_open(ip_address, port):
        with print_lock:
            print(f"The port {port} is open!")

def main() -> None:
    """Prompt for an IP address and scan all ports using threads."""
    ip_address: str = input("Type an IP address:\n").strip()

    semaphore = threading.Semaphore(MAX_THREADS)
    threads: list[threading.Thread] = []

    def throttled_scan(port: int) -> None:
        with semaphore:
            scan_port(ip_address, port)

    for port in range(START_PORT, END_PORT + 1):
        t = threading.Thread(target=throttled_scan, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Done.")

if __name__ == "__main__":
    main()