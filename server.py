import socket
import GET
import HEAD
import DELETE
import PUT
import POST
import log_file_entry as log 
import get_date
import datetime
from _thread import *


#creating a socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = int(GET.port)
connections = int(GET.max_connections)

#binding the server to the specified port
server.bind(('localhost', PORT))

cur_time = datetime.datetime.now()
cur_day = get_date.getday(str(cur_time.day) + " " + str(cur_time.month) + " " + str(cur_time.year))
cur_month = get_date.getMonth(str(cur_time.month))
cur_day = str(cur_day)

server.listen(100)

list_of_clients = []

def recvall(sock):
    BUFF_SIZE = 1024
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

def clientThread(clientSocket, address):
    
    doc_type = ''
    while True:
        
        msg = recvall(clientSocket)
        msg_data = msg.split('\r\n\r\n'.encode())
        headers = msg_data[0]

        try:
            header = headers.decode()
        except UnicodeDecodeError:
            pass
                
        try:
            pieces = header.split('\n')
        except AttributeError:
            pass

        if len(msg) != 0:
            if len(pieces) > 0:
                request = pieces[0].split(' ')
            
            #GET request
            if request[0] == 'GET':
                for line in pieces:
                    header = line.split(':')
                    if header[0] == 'Accept-Encoding':
                        encoding = header[1].strip()
                        break
                    else:
                        encoding = ''
                
                if request[1].find('.png') == -1 and request[1].find('.jpg') == -1:
                    response_html = GET.get(pieces, address)
                    
                    try:
                        if((encoding == 'zlib' or encoding == 'gzip') and response_html.find('404') < 0 and response_html.find('406') < 0):
                            clientSocket.sendall(response_html)
                        else:
                            clientSocket.sendall(response_html.encode())

                    except (TypeError, BrokenPipeError):
                        try:
                            clientSocket.sendall(response_html)
                        except TypeError:
                            clientSocket.sendall(response_html.encode())

                else:
                    try:
                        response_html, response_image = GET.get(pieces, address)
                        try:
                            clientSocket.sendall(response_html.encode() + response_image)
                        except BrokenPipeError:
                            pass

                    except ValueError:
                        response_html = GET.get(pieces, address)
                        try:
                            clientSocket.sendall(response_html.encode())
                        except BrokenPipeError:
                            pass

            #HEAD request
            elif request[0] == 'HEAD':
                response_html = HEAD.head(pieces, address)
                clientSocket.sendall(response_html.encode())
                    
            #DELETE request
            elif request[0] == 'DELETE':
                if request[1].find('.png') == -1 and request[1].find('.jpg') == -1:
                    response_html = DELETE.delete(pieces, address)
                    try:
                        clientSocket.sendall(response_html.encode())
                    except BrokenPipeError:
                        pass

                else:
                    try:
                        response_html, response_image = DELETE.delete(pieces, address)
                        try:
                            clientSocket.sendall(response_html.encode() + response_image)
                        except BrokenPipeError:
                            pass
                        
                    except ValueError:
                        response_html = DELETE.delete(pieces, address)
                        try:
                            clientSocket.sendall(response_html.encode())
                        except BrokenPipeError:
                            pass


            elif request[0] == 'PUT':
                for line in pieces:
                    header = line.split(':')
                    if header[0] == 'Content-Type':
                        doc_type = header[1]
                        break

                if doc_type.find('html') >= 0 or doc_type.find('plain') >= 0:
                    payload = msg_data[1].decode()
                    response_html = PUT.put(pieces, address, payload)
                    try:
                        clientSocket.sendall(response_html.encode())
                    except BrokenPipeError:
                        pass

                else:
                    try:
                        payload = msg_data[1]
                    except IndexError:
                        pass
                            
                    try:
                        response_html, response_image = PUT.put(pieces, address, payload)
                        try:
                            clientSocket.sendall(response_html.encode() + response_image)
                        except BrokenPipeError:
                            pass
                        
                    except ValueError:
                        response_html = PUT.put(pieces, address, '')
                        try:
                            clientSocket.sendall(response_html.encode())
                        except BrokenPipeError:
                            pass

            elif request[0] == 'POST':
                
                payload = msg_data[1].decode()
                response_html = POST.post(pieces, address, payload)
                try:
                    clientSocket.sendall(response_html.encode())
                except BrokenPipeError:
                    pass
            try:
                clientSocket.shutdown(socket.SHUT_RDWR)
            except OSError:
                #Transport endpoint not connected
                pass
        else:
            clientSocket.close()
            remove(clientSocket)
            break

#removes the client from the list of clients 
def remove(connection):
    if (connection in list_of_clients):
        list_of_clients.remove(connection)

while True:
    
    if len(list_of_clients) <= connections:

        #this accepts a connection from the client
        #it returns a socket object and address bound to the socket on the client side
        connection, address = server.accept()

        #add the user to the list of users
        list_of_clients.append(connection)

        #creating a new thread for each  user
        start_new_thread(clientThread, (connection, address))
    
    else:
        log.make_entry('127.0.0.1', '', cur_time, cur_month, 0, 0, '', 'notice', 'Max simultaneous connections exceeded')
        break

server.close()
exit()