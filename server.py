import socket
import threading
import signal

from exceptions import ParseError
from utilities import get_headers, get_request_line

HOST = '127.0.0.1'
PORT = 1738

RUNNING = True

REQUIRED_HEADERS = ['host']
DISPATCH_DICTIONARY = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def signal_shutdown(_sig, _frame) -> None:
    global RUNNING
    RUNNING = False

signal.signal(signal.SIGINT, signal_shutdown) # Catch CTRL+C
signal.signal(signal.SIGTERM, signal_shutdown) # Catch kill command

def handle_connection(connection: socket.socket) -> None:
    with connection as s:
        buffer = bytearray()
        header_delimiter = b'\r\n\r\n'

        while header_delimiter not in buffer:
            chunk = s.recv(1024)
            if not chunk:
                print('Client closed before sending full headers')
                # maybe send a response here too
                return
            buffer.extend(chunk)
        
        head_raw, _, remaining_bytes = buffer.partition(header_delimiter) # partition returns (before, delimiter, after)
        head = head_raw.decode('utf-8')

        try:
            (method, path, protocol_version), remaining_head = get_request_line(head)
        except ParseError:
            return # sendall bad request

        if protocol_version != 'HTTP/1.1':
            return # sendall incorrect version 505

        if method not in DISPATCH_DICTIONARY.keys():
            return # sendall 405 method not allowed

        try:
            headers = get_headers(remaining_head)
        except ParseError:
            return # sendall bad request 

        if not all(k in headers for k in REQUIRED_HEADERS):
            return #sendall bad request

        try:
            content_length = int(headers.get('Content-Length', 0)) # important, read this from the headers
        except ValueError:
            return # sendall bad request

        body = bytearray(remaining_bytes)

        while len(body) < content_length:
            bytes_to_read = content_length - len(body)
            chunk = s.recv(min(bytes_to_read, 4096))
            if not chunk:
                print('Connection lost while reading body')
                return # send failure back ?, maybe internal server error ?
            body.extend(chunk)

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
    print('Server started')
    main()
    print('Server closed')