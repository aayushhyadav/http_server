import socket
import threading

def send_request(method):
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('127.0.0.1', 3000))
    
    except ConnectionRefusedError:
        print('Connection was refused!')

    client_sock.settimeout(5)

    cmd = method.encode()
    client_sock.send(cmd)
    
    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) < 1:
                break
        
            print(data.decode(), end = '')
    except (socket.timeout, ConnectionResetError):
        pass
    
    client_sock.close()
    print('\n\n')
    
GET_1 = 'GET /about HTTP/1.1\r\nHost: localhost\r\n\r\n'
GET_2 = 'GET /help HTTP/1.1\r\nHost: localhost\r\n\r\n'
GET_3 = 'GET /create_html HTTP/1.1\r\nHost: localhost\r\n\r\n'
GET_4 = 'GET /proxy HTTP/1.1\r\nHost: localhost\r\nProxy-Authorization: Basic aayush:aayu\r\n\r\n'

HEAD_1 = 'HEAD /about HTTP/1.1\r\nHost: localhost\r\n\r\n'
HEAD_2 = 'HEAD /help HTTP/1.1\r\nHost: localhost\r\n\r\n'
HEAD_3 = 'HEAD /create_html HTTP/1.1\r\nHost: localhost\r\n\r\n'
HEAD_4 = 'HEAD /proxy HTTP/1.1\r\nHost: localhost\r\nProxy-Authorization: Basic aayush:aayu\r\n\r\n'

DELETE_1 = 'DELETE /text1.txt HTTP/1.1\r\nHost: localhost\r\n\r\n'

res_file = open('sample_resource/sample.txt', 'r')
body = res_file.read()
res_file.close()

PUT_1 = 'PUT /text3.txt HTTP/1.1\r\nHost: localhost\r\nContent-Type: text/plain\r\n\r\n' + body
POST_1 = 'POST /about HTTP/1.1\r\nHost: localhost\r\n\r\nLocation=Thane&Name=Aayush'

t1 = threading.Thread(target = send_request, args = (GET_1,)).start()
t2 = threading.Thread(target = send_request, args = (GET_2,)).start()
t3 = threading.Thread(target = send_request, args = (GET_3,)).start()
t4 = threading.Thread(target = send_request, args = (GET_4,)).start()
t5 = threading.Thread(target = send_request, args = (HEAD_1,)).start()
t6 = threading.Thread(target = send_request, args = (HEAD_2,)).start()
t7 = threading.Thread(target = send_request, args = (HEAD_3,)).start()
t8 = threading.Thread(target = send_request, args = (HEAD_4,)).start()
t9 = threading.Thread(target = send_request, args = (DELETE_1,)).start()
t10 = threading.Thread(target = send_request, args = (PUT_1,)).start()
t11 = threading.Thread(target = send_request, args = (POST_1,)).start()