import datetime
import get_date

Dict = {'/create_html': 'Sat, 17 Oct 2020 20:16:53 IST', '/text1.txt': 'Sat, 17 Oct 2020 20:16:53 IST', '/text2.txt': 'Sat, 17 Oct 2020 20:16:53 IST', '/images/overcast.jpg': 'Sat, 17 Oct 2020 20:16:53 IST',
        '/images/snowfall.jpg': 'Sat, 17 Oct 2020 20:16:53 IST'}

def check_headers(headers):

    website_files = ['/', '/about', '/help', '/images/robot.png', '/images/weather.png', '/images/plain.jpg', '/access_log.txt', '/cookies.txt', '/post_log.txt', '/error_log.txt']
    check = 1
    valid = 1
    modified_since = 1

    cur_time = datetime.datetime.now()

    HOST = 0
    CONTENT_TYPE = '*/*'
    PROXY_AUTHORIZE = 0
    RANGE = 'none'
    ENCODING = 'identity'
    mod_date = ''
    IF_MOD_SINCE = -1
    IF_UNMOD_SINCE = -1

    request = headers[0].split(' ')
    uri = request[1]

    #validate the headers
    for line in headers:
        header = line.split(':')

        #validate the host header
        if header[0] == 'Host':
            if header[1].strip().replace('\r', '') == 'localhost':
                HOST = 1
        
        #check for the accept header
        if header[0] == 'Accept':
            CONTENT_TYPE = header[1].strip()
        
        #check for proxy authentication
        if header[0] == 'Proxy-Authorization':
            PROXY_AUTHORIZE = 1
        
        #check for the range header
        if header[0] == 'Range':
            temp = header[1].strip().split('=')
            RANGE = temp[1]
            
        #check for the accept-encoding header
        if header[0] == 'Accept-Encoding':
            ENCODING = header[1].strip()
        
        #check for the if-modified-since header
        if header[0] == 'If-Modified-Since' or header[0] == 'If-Unmodified-Since':
            if(header[0] == 'If-Unmodified-Since'):
                modified_since = 0

            mod_date = header[1].strip()
            mod_date += ':' + header[2]
            mod_date += ':' + header[3]

    if(mod_date != ''):     
        parts = mod_date.split(' ')
        req_day = int(parts[1])
        req_month = int(get_date.getMonth_2(parts[2]))
        req_year = int(parts[3])
        
        req_time = parts[4]
        time = req_time.split(':')
        req_hour = int(time[0])
        req_min = int(time[1])
        req_sec = int(time[2])
        
        d_req = datetime.datetime(req_year, req_month, req_day)
        d_cur = datetime.datetime(cur_time.year, cur_time.month, cur_time.day)

        if(d_req > d_cur):
            valid = 0
            IF_MOD_SINCE = 1
        
        elif(d_cur == d_req):
            if(req_hour > cur_time.hour):
                valid = 0
                IF_MOD_SINCE = 1
            elif(req_hour == cur_time.hour):
                if(req_min > cur_time.minute):
                    valid = 0
                    IF_MOD_SINCE = 1
                elif(req_min == cur_time.minute):
                    if(req_sec > cur_time.second):
                        valid = 0
                        IF_MOD_SINCE = 1

    for f in website_files:
        if f == uri:
            check = 0
            break

    if mod_date != '' and check == 1 and valid == 1:
        
        last_mod = Dict[uri]
        parts = last_mod.split(' ')
        dict_day = int(parts[1])
        dict_month = int(get_date.getMonth_2(parts[2]))
        dict_year = int(parts[3])
        
        dict_time = parts[4]
        time = dict_time.split(':')
        dict_hour = int(time[0])
        dict_min = int(time[1])
        dict_sec = int(time[2])

        d_dict =  datetime.datetime(dict_year, dict_month, dict_day)

        if(d_dict > d_req):
            IF_MOD_SINCE = 1
        
        elif(d_dict < d_req):
            IF_MOD_SINCE = 0
        
        elif(d_dict == d_req):
            if(dict_hour < req_hour):
                IF_MOD_SINCE = 0
            
            elif(dict_hour > req_hour):
                IF_MOD_SINCE = 1
            
            elif(dict_hour == req_hour):
                if(dict_min < req_min):
                    IF_MOD_SINCE = 0
            
                elif(dict_min > req_min):
                    IF_MOD_SINCE = 1
                
                elif(dict_min == req_min):
                    if(dict_sec < req_sec):
                        IF_MOD_SINCE = 0
            
                    elif(dict_sec > req_sec):
                        IF_MOD_SINCE = 1
    # elif(valid == 1):
    #     IF_MOD_SINCE = 0    
    
    if(modified_since == 0 and valid == 1):
        if(IF_MOD_SINCE == 1):
            IF_UNMOD_SINCE = 0
            IF_MOD_SINCE = -1
        else:
            IF_UNMOD_SINCE = 1
            IF_MOD_SINCE = -1
    
    return (HOST, CONTENT_TYPE, PROXY_AUTHORIZE, RANGE, ENCODING, IF_MOD_SINCE, IF_UNMOD_SINCE)