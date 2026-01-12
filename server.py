import socket
import threading
import signal
import sys

HOST = '127.0.0.1'
PORT = 1738

RUNNING = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def signal_shutdown(_sig, _frame) -> None:
    global RUNNING
    RUNNING = False

signal.signal(signal.SIGINT, signal_shutdown) # Catch CTRL+C
signal.signal(signal.SIGTERM, signal_shutdown) # Catch kill command

def handle_connection(connection: socket.socket) -> None: # make sure to close the connection!!!!
    ...

def main() -> None:
    with sock as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1.0)
        while RUNNING:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue

            connection_worker = threading.Thread(target=handle_connection, args=(conn,), daemon=True)
            connection_worker.start()

if __name__ == '__main__':
    main()