from pathlib import Path
import os
import datetime
import calendar
import get_date
import cookie
import headers
import GET
import log_file_entry as log 

document_root = GET.document_root
images_folder = GET.images_folder
permanent_redirect = GET.permanent_redirect
temp_redirect = GET.temp_redirect

#confidential files
website_files = ['/access_log.txt', '/cookies.txt', '/post_log.txt']

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

def head(req, address):
    #get all the files and folders in the root
    files = os.listdir(document_root)
    
    request = req[0].split(' ')
    uri = request[1]

    cur_time = datetime.datetime.now()
    cur_day = get_date.getday(str(cur_time.day) + " " + str(cur_time.month) + " " + str(cur_time.year))
    cur_month = get_date.getMonth(str(cur_time.month))
    cur_day = str(cur_day)

    #validate the headers
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
            
            log.make_entry(address, req[0], cur_time, cur_month, status_code, 0, '', 'warn', 'Client not allowed to access the file')
            return data

    #if requested URL is root document
    if uri == '/':
        res_file = open(str(document_root) + '/index.html', 'r')
        file_stats = os.stat(str(document_root) + '/index.html')

        data = "HTTP/1.1 200 OK\r\n"
        status_code = 200
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
         
        if set_cookie_header == 1:
            data += "Cookie: " + str(cookie_id) + '\r\n'

        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "\r\n"
        
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
        log.make_entry(address, req[0], cur_time, cur_month, status_code, 0)

        return data

    if (uri == '/example_2'):
        data = "HTTP/1.1 301 Moved Permanently\r\n"
        status_code = 301
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "Location: " + permanent_redirect + '\r\n'
        data += '\r\n'
        log.make_entry(address, req[0], cur_time, cur_month, status_code, 0)

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
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
         
        if set_cookie_header == 1:
            data += "Set-Cookie: " + str(cookie_id) + '\r\n'

        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "\r\n"
        
        log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size, '', 'error', 'File was not found')
        res_file.close()
        return data

    else:
        
        data = "HTTP/1.1 200 OK\r\n"
        status_code = 200
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
        
        if found_file == 1:
            res_file = open(str(document_root) + '/' + uri_page, 'r')
            file_stats = os.stat(str(document_root) + '/' + uri_page)

            if(uri_page.find('.txt') >= 0):
                data += "Content-Type: text/plain\r\n"
            
            else:
                if uri_page.find('proxy.html') >= 0:
                    if (proxy_auth == 0):
                        data = proxy_auth_req(address, req[0], cur_day, cur_time, cur_month)
                        return data

                data += "Content-Type: text/html\r\n"

            data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
             
            if set_cookie_header == 1:
                data += "Set-Cookie: " + str(cookie_id) + '\r\n'

            data += "Server: Aayush/0.1\r\n"
            data += "Connection: Closed\r\n"
            data += "\r\n"

            res_file.close()
            
            log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
            return data

        else:
            res_file = open(str(document_root) + '/' + uri_page, 'rb')
            file_stats = os.stat(str(document_root) + '/' + uri_page)

            if(uri_page.find('.png') >= 0):
                data += "Content-Type: image/png\r\n"
            elif(uri_page.find('.jpg') >= 0):
                data += "Content-Type: image/jpeg\r\n"

            data += "Content-Length: " + str(file_stats.st_size) + "\r\n"
             
            if set_cookie_header == 1:
                data += "Set-Cookie: " + str(cookie_id) + '\r\n'

            data += "Server: Aayush/0.1\r\n"
            data += "Connection: Closed\r\n"
            data += "\r\n"

            log.make_entry(address, req[0], cur_time, cur_month, status_code, file_stats.st_size)
            res_file.close()

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
