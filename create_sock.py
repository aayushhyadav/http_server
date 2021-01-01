import socket
import time

def send_request(method):

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 3000))

    client_sock.settimeout(5)

    cmd = method.encode()
    client_sock.sendall(cmd)

    data = b''
    BUFF_SIZE = 4096

    try:
        while True:
            parts = client_sock.recv(BUFF_SIZE)
            data += parts
            if len(parts) < BUFF_SIZE:
                break
    except socket.timeout:
        pass

    client_sock.close()
    headers = data.split('\r\n\r\n'.encode())

    header = headers[0].decode().split('\r\n')
    try:
        body = headers[1].decode()
        return header, body

    except (UnicodeDecodeError, IndexError):
        if(len(headers) == 2):
            return header, headers[1]
        
        return header, ''