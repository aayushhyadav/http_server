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

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

def post(req, address, msg):
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

    #check if the request contains cookie header
    cookie_id = cookie.generate_cookie(req)

    if cookie_id == False:
        set_cookie_header = 0
    else:
        set_cookie_header = 1

    if uri == '/':
        data = "HTTP/1.1 200 OK\r\n"
        status_code = 200
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
         
        if set_cookie_header == 1:
            data += "Set-Cookie: " + str(cookie_id) + '\r\n'

        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "\r\n"

        log.make_entry(address, req[0], cur_time, cur_month, status_code, len(msg), msg)
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

    if found == 0:
        data = "HTTP/1.1 404 Not Found\r\n"
        status_code = 404
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
         
        if set_cookie_header == 1:
            data += "set-Cookie: " + str(cookie_id) + '\r\n'

        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "\r\n"

        log.make_entry(address, req[0], cur_time, cur_month, status_code, len(msg))

        return data 
    
    else:
        data = "HTTP/1.1 200 OK\r\n"
        status_code = 200
        data += "Date: " + cur_day[0:3] + ", " + str(cur_time.day) + " " + cur_month + " " + str(cur_time.year) + " " + str(cur_time.hour) + ":" + str(cur_time.minute) + ":" + str(cur_time.second) + " " + str(LOCAL_TIMEZONE) + "\r\n"
         
        if set_cookie_header == 1:
            data += "Set-Cookie: " + str(cookie_id) + '\r\n'

        data += "Server: Aayush/0.1\r\n"
        data += "Connection: Closed\r\n"
        data += "\r\n"

        log.make_entry(address, req[0], cur_time, cur_month, status_code, len(msg), msg)

        return data 