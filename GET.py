from pathlib import Path
import os
import datetime
import calendar
import get_date
import cookie
import headers
import log_file_entry as log 
import gzip
import zlib

config = open('server.conf', 'r')
lines = config.readlines()

for line in lines:
    if line.find('DocumentRoot') >= 0:
        doc_root = line.split(' ')
    
    if line.find('Redirect permanent') >= 0:
        doc_redirect_301 = line.split(' ')
        permanent_redirect = doc_redirect_301[3].replace('\n', '')
        permanent_redirect = permanent_redirect.replace('/301', '')

    elif line.find('Redirect') >= 0:
        doc_redirect_302 = line.split(' ')
        temp_redirect = doc_redirect_302[2].replace('\n', '')
        temp_redirect = temp_redirect.replace('/302', '')
    
    if(line.find('AccessLog') >= 0):
        doc_access = line.split(' ')
    
    if(line.find('PostLog') >= 0):
        doc_post = line.split(' ')
        
    
    if(line.find('ErrorLog') >= 0):
        doc_error = line.split(' ')
    
    if(line.find('Cookies') >= 0):
        doc_cookie = line.split(' ')
    
    if(line.find('Port') >= 0):
        server_port = line.split(' ')
    
    if(line.find('MaxSimultaneousConnections') >= 0):
        simul_connections = line.split(' ')
    
    if(line.find('LogLevel') >= 0):
        log_level = line.split(' ')
        

# document_root = Path('html/')
# images_folder = Path('html/images/')

document_root = doc_root[1].replace('\n', '')

images_folder = document_root + '/images'

permanent_redirect += document_root + '/301'

temp_redirect += document_root + '/302'

access_log = doc_access[1].replace('\n', '')
post_log = doc_post[1].replace('\n', '')
error_log = doc_error[1].replace('\n', '')

stored_cookies = doc_cookie[1].replace('\n', '')

port = server_port[1].replace('\n', '')

max_connections = simul_connections[1].replace('\n', '')

level = log_level[1].replace('\n', '')

#accept list for different types
html_list = ['', '*/*', 'text/*', 'text/html', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']
plain_list = ['', '*/*', 'text/*', 'text/plain', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']
png_list = ['', '*/*', 'image/*', 'image/png', 'image/webp,*/*', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']
jpg_list = ['', '*/*', 'image/*', 'image/jpeg', 'image/webp,*/*', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']

#confidential files
website_files = ['/access_log.txt', '/cookies.txt', '/post_log.txt']

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

def get(req, address):
    #get all the files and folders in the root
    files = os.listdir(document_root)
    
    request = req[0].split(' ')
    uri = request[1]

    cur_time = datetime.datetime.now()
    cur_day = get_date.getday(str(cur_time.day) + " " + str(cur_time.month) + " " + str(cur_time.year))
    cur_month = get_date.getMonth(str(cur_time.month))
    cur_day = str(cur_day)

    #validate the header
    host, type, proxy_auth, range, encoding, if_mod_since, if_unmod_since = headers.check_headers(req)

    if host == 0:

        data = "HTTP/1.1 400 Bad Request\r\n"
        status_code = 400
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += '\r\n'
        log.make_entry(address, req[0], cur_time, cur_month, status_code, 0, '', 'error', 'Bad request')

        return data

    if if_mod_since == 0:
        data = "HTTP/1.1 304 Not Modified\r\n"
        status_code = 304
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += '\r\n'
        log.make_entry(address, req[0], cur_time, cur_month, status_code, 0)

        return data
    
    if if_unmod_since == 0:
        data = "HTTP/1.1 412 Precondition Failed\r\n"
        status_code = 412
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += '\r\n'
        log.make_entry(address, req[0], cur_time, cur_month, status_code, 0)

        return data

    #check if the request contains cookie header
    cookie_id = cookie.generate_cookie(req)

    if cookie_id == False:
        set_cookie_header = 0
    else:
        set_cookie_header = 1
    
    for f in website_files:
        if f == uri:
            content = "You are not authorized to access the file\r\n"
            data = "HTTP/1.1 405 Method Not Allowed\r\n"
            status_code = 405
            data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
            data += "Content-Type: text/plain\r\n"  
            data += "Content-Length: " + str(len(content)) + "\r\n"
            
            if set_cookie_header == 1:
                data += "Set-Cookie: " + str(cookie_id) + '\r\n'

            data += "Server: Aayush/0.1\r\n"
            data += "Connection: Closed\r\n"
            data += "\r\n"
            data += content + "\r\n"
            
            log.make_entry(address, req[0], cur_time, cur_month, status_code, len(content), '', 'warn', 'Client not allowed to access the file')
            return data

    #if requested URL is root document
    if uri == '/':
        accept = 0
        for element in html_list:
            if element == type:
                accept = 1
                break
        
        if accept == 0:
            data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
            return data

        res_file = open(str(document_root) + '/index.html', 'r')
        file_stats = os.stat(str(document_root) + '/index.html')

        data = "HTTP/1.1 200 OK\r\n"
        status_code = 200
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Content-Type: text/html\r\n"
        data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
        
        if set_cookie_header == 1:
            data += "Set-Cookie: " + str(cookie_id) + '\r\n'
                
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"

        if range == 'none':
            data += '\r\n' + res_file.read()
        else:
            data += 'Content-Range: ' + range + '/' + str(file_stats.st_size) + '\r\n\r\n'

            partial_data = res_file.read()
            byte_pos = range.split('-')

            if byte_pos[0] == '':
                data += partial_data[file_stats.st_size - int(byte_pos[1]):]
            elif byte_pos[1] == '':
                data += partial_data[int(byte_pos[0]):]
            elif int(byte_pos[0]) > int(byte_pos[1]):
                data = unsatisfiable_range(address, req[0], cur_day, cur_time, cur_month)
                return data
            else:
                data += partial_data[int(byte_pos[0]):int(byte_pos[1])]
            
            data = data.replace('200', '206')
            data = data.replace('OK','Partial Content')

        if (encoding == 'gzip, deflate'):
            log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
            res_file.close()

        elif (encoding != 'identity'):
            if (encoding == 'gzip'):
                entity = data.split('\r\n\r\n')
                encoded_entity = gzip.compress(entity[1].encode())
                entity[0] = entity[0].replace(str(file_stats.st_size), str(len(encoded_entity)))
                entity[0] += '\r\nContent-Coding: gzip'
                data = entity[0].encode() + '\r\n\r\n'.encode() + encoded_entity
                
            elif (encoding == 'zlib'):
                entity = data.split('\r\n\r\n')
                encoded_entity = zlib.compress(entity[1].encode())
                entity[0] = entity[0].replace(str(file_stats.st_size), str(len(encoded_entity)))
                entity[0] += '\r\nContent-Coding: zlib'
                data = entity[0].encode() + '\r\n\r\n'.encode() + encoded_entity
                
            else:
                data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                
            log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
            res_file.close()

        return data

    if (uri == '/example'):
        data = "HTTP/1.1 302 Found\r\n"
        status_code = 302
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "Location: " + temp_redirect + '\r\n'
        data += '\r\n'
        data += temp_redirect + '\r\n'
        log.make_entry(address, req[0], cur_time, cur_month, status_code, len('http://localhost:2000/302\r\n'))

        return data

    if (uri == '/example_2'):
        data = "HTTP/1.1 301 Moved Permanently\r\n"
        status_code = 301
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "Location: " + permanent_redirect + '\r\n'
        data += '\r\n'
        data += permanent_redirect + '\r\n'
        log.make_entry(address, req[0], cur_time, cur_month, status_code, len('http://localhost:2000/301\r\n'))

        return data
    
    uri = uri.split('/')
    uri_page = uri[len(uri) - 1]
    uri_page += ".html"

    #check if the requested URL exists or not(files)
    for file in files:
        if uri_page != str(file):
            found_file = 0
            found = 0
        else:
            found_file = 1
            found = 1
            break
    
    if found_file == 0:
        uri_page = uri_page.replace('.html', '')

    #check for text files 
    for file in files:
        if uri_page != str(file):
            found_file = 0
            found = 0
        else:
            found_file = 1
            found = 1
            break

    image_files = os.listdir(images_folder)

    #check for the images
    if found_file == 0:
        for image in image_files:
            if uri_page == str(image):
                found = 1
                uri_page = "images/" + uri_page
                break
            else:
                found = 0

    #if the requested document is not found
    if found == 0:
        res_file = open(str(document_root) + '/404.html', 'r')
        file_stats = os.stat(str(document_root) + '/404.html')

        data = "HTTP/1.1 404 Not Found\r\n"
        status_code = 404
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Content-Type: text/html\r\n"
        data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
        
        if set_cookie_header == 1:
                data += "Set-Cookie: " + str(cookie_id) + '\r\n'
                
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "\r\n"
        data += res_file.read()
        data += '\r\n\r\n'

        log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size, '', 'error', 'File was not found')
        res_file.close()

        return data

    else:
        
        data = "HTTP/1.1 200 OK\r\n"
        status_code = 200
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        
        if found_file == 1:
            
            if uri_page.find('.txt') >= 0:
                accept = 0
                for element in plain_list:
                    if element == type.strip():
                        accept = 1
                        break
        
                if accept == 0:
                    data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                    return data

                data += "Content-Type: text/plain\r\n"

            else:
                accept = 0
                for element in html_list:
                    if element == type.strip():
                        accept = 1
                        break
        
                if accept == 0:
                    data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                    return data
                
                if uri_page.find('proxy.html') >= 0:
                    if (proxy_auth == 0):
                        data = proxy_auth_req(address, req[0], cur_day, cur_time, cur_month)
                        return data

                data += "Content-Type: text/html\r\n"
            
            res_file = open(str(document_root) + '/' + uri_page, 'r')
            file_stats = os.stat(str(document_root) + '/' + uri_page)

            data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
            
            if set_cookie_header == 1:
                data += "Set-Cookie: " + str(cookie_id) + '\r\n'
                
            data += "Server: Aayush/0.1\r\n"
            data += "Connection: Closed\r\n"

            if range == 'none':
                data += '\r\n' + res_file.read()
            else:
                data += 'Content-Range: ' + range + '/' + str(file_stats.st_size) + '\r\n'
                data += "\r\n"

                partial_data = res_file.read()
                byte_pos = range.split('-')

                if byte_pos[0] == '':
                    data += partial_data[file_stats.st_size - int(byte_pos[1]):]
                elif byte_pos[1] == '':
                    data += partial_data[int(byte_pos[0]):]
                elif int(byte_pos[0]) > int(byte_pos[1]):
                    data = unsatisfiable_range(address, req[0], cur_day, cur_time, cur_month)
                    return data
                else:
                    data += partial_data[int(byte_pos[0]):int(byte_pos[1])]

                data = data.replace('200', '206')
                data = data.replace('OK','Partial Content')

            data += "\r\n"

            if (encoding == 'gzip, deflate'):
                log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
                res_file.close()

            elif (encoding != 'identity'):
                if (encoding == 'gzip'):
                    entity = data.split('\r\n\r\n')
                    encoded_entity = gzip.compress(entity[1].encode())
                    entity[0] = entity[0].replace(str(file_stats.st_size), str(len(encoded_entity)))
                    entity[0] += '\r\nContent-Coding: gzip'
                    data = entity[0].encode() + '\r\n\r\n'.encode() + encoded_entity
                    
                elif (encoding == 'zlib'):
                    entity = data.split('\r\n\r\n')
                    encoded_entity = zlib.compress(entity[1].encode())
                    entity[0] = entity[0].replace(str(file_stats.st_size), str(len(encoded_entity)))
                    entity[0] += '\r\nContent-Coding: zlib'
                    data = entity[0].encode() + '\r\n\r\n'.encode() + encoded_entity
                    
                else:
                    data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                    return data

                log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
                res_file.close()
            
            else:
                log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
                res_file.close()
                
            return data

        else:
            
            if uri_page.find('.jpg') >= 0:
                accept = 0
                for element in jpg_list:
                    if element == type.strip():
                        accept = 1
                        break
        
                if accept == 0:
                    data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                    return data

                data += "Content-Type: image/jpeg\r\n"
            
            elif uri_page.find('.png') >= 0:
                accept = 0
                for element in png_list:
                    if element == type.strip():
                        accept = 1
                        break
                #print(type.strip())
                if accept == 0:
                    data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                    return data

                data += "Content-Type: image/png\r\n"
            
            res_file = open(str(document_root) + '/' + uri_page, 'rb')
            file_stats = os.stat(str(document_root) + '/' + uri_page)

            data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
            
            if set_cookie_header == 1:
                data += "Set-Cookie: " + str(cookie_id) + '\r\n'
                
            data += "Server: Aayush/0.1\r\n"
            data += "Connection: Closed\r\n"
            
            if range == 'none':
                bin_data = res_file.read()
            else:
                data += 'Content-Range: ' + range + '/' + str(file_stats.st_size) + '\r\n'
                
                partial_data = res_file.read()
                byte_pos = range.split('-')

                if byte_pos[0] == '':
                    bin_data = partial_data[file_stats.st_size - int(byte_pos[1]):]
                elif byte_pos[1] == '':
                    bin_data = partial_data[int(byte_pos[0]):]
                elif int(byte_pos[0]) > int(byte_pos[1]):
                    data = unsatisfiable_range(address, req[0], cur_day, cur_time, cur_month)
                    return data
                else:
                    bin_data = partial_data[int(byte_pos[0]):int(byte_pos[1])]

                data = data.replace('200', '206')
                data = data.replace('OK','Partial Content')
            
            image_body = bin_data
            
            if (encoding == 'gzip, deflate'):
                log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
                res_file.close()

            elif (encoding != 'identity'):
                if (encoding == 'gzip'):
                    data += 'Content-Coding: gzip\r\n'
                    image_body = gzip.compress(bin_data)
                    data = data.replace(str(file_stats.st_size), str(len(image_body)))
                    
                elif (encoding == 'zlib'):
                    data += 'Content-Coding: zlib\r\n'
                    image_body = zlib.compress(bin_data)
                    data = data.replace(str(file_stats.st_size), str(len(image_body)))
                    
                else:
                    data = not_acceptable(address, req[0], cur_day, cur_time, cur_month)
                    return data

            data += '\r\n'
            log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
            res_file.close()

    return (data, image_body)

def not_acceptable(address, req, cur_day, cur_time, cur_month):
    data = 'HTTP/1.1 406 Not Acceptable\r\n'
    status_code = 406
    data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
    data += "Server: Aayush/0.1\r\n"
    data += "Connection: Closed\r\n"
    data += "\r\n"

    log.make_entry(address, req, cur_time, cur_month, status_code, 0, '', 'error', 'Header value not acceptable')
    return data

def proxy_auth_req(address, req, cur_day, cur_time, cur_month):
    data = "HTTP/1.1 407 Proxy Authentication Required\r\n"
    status_code = 407
    data += "Proxy-Authenticate: Basic\r\n"
    data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
    data += "Server: Aayush/0.1\r\n"
    data += "Connection: Closed\r\n"
    data += "\r\n"

    log.make_entry(address, req, cur_time, cur_month, status_code, 0, '', 'warn', 'Proxy authentication required')
    return data

def unsatisfiable_range(address, req, cur_day, cur_time, cur_month):
    data = 'HTTP/1.1 416 Requested Range Not Satisfiable\r\n'
    status_code = 416
    data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
    data += "Server: Aayush/0.1\r\n"
    data += "Connection: Closed\r\n"
    data += "\r\n"

    log.make_entry(address, req, cur_time, cur_month, status_code, 0, '', 'error', 'Range header field value not satisfiable')
    return data
