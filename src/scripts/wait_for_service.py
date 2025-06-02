import socket
import time
import sys

def wait_for_service(host, port, timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=5):
                print(f"{host}:{port} is up!")
                return True
        except (socket.timeout, ConnectionRefusedError):
            if time.time() - start_time > timeout:
                print(f"Timeout waiting for {host}:{port}", file=sys.stderr)
                sys.exit(1)
            print(f"Waiting for {host}:{port}...")
            time.sleep(1)

if __name__ == "__main__":
    services = [
        ("database", 5432),
        ("queue", 5672),
        ("minio", 9000),
    ]
    for host, port in services:
        wait_for_service(host, port)