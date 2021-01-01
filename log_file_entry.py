import datetime
import GET

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

def make_entry(address, req, cur_time, cur_month, status_code, content_length, post_entry = '', error = '', description = ''):
    method = ''
    if(status_code != 0):
        res_file = open(GET.access_log, 'a')
        res_file.write(str(address[0]) + ' - - ')
        res_file.write('[' + str(cur_time.day) + '/' + str(cur_time.month) + '/' + str(cur_time.year)
                        + ':' + str(cur_time.hour) + ':' + str(cur_time.minute) + ':' + str(cur_time.second)
                        + ' ' + str(LOCAL_TIMEZONE) + ']')

        request = req.split(' ')
        method = request[0]
        uri = request[1]

        res_file.write(' ' + '\"' + method + ' ' + uri + ' HTTP/1.1' + '\"')
        res_file.write(' ' + str(status_code) + ' ' + str(content_length) + '\n')

        res_file.close()

    if(method == 'POST' and post_entry != ''):
        # res_file = open('html/post_log.txt', 'a')
        res_file = open(GET.post_log, 'a')
        res_file.write(str(address[0]) + ' - - ')
        res_file.write('[' + str(cur_time.day) + '/' + str(cur_time.month) + '/' + str(cur_time.year)
                    + ':' + str(cur_time.hour) + ':' + str(cur_time.minute) + ':' + str(cur_time.second)
                    + ' ' + str(LOCAL_TIMEZONE) + ']')
        
        fields = str(post_entry).split('&')

        res_file.write(' ' + 'Data: ')
        
        for field in fields:
            res_file.write(field + ' ')
        
        res_file.write('\n')
        res_file.close()

    if(error == GET.level):

        res_file = open(GET.error_log, 'a')
        res_file.write('[' + str(cur_time.day) + '/' + str(cur_time.month) + '/' + str(cur_time.year)
                    + ':' + str(cur_time.hour) + ':' + str(cur_time.minute) + ':' + str(cur_time.second)
                    + ' ' + str(LOCAL_TIMEZONE) + ']')
        res_file.write('[ ' + error + ' ]')
        
        if(error == 'notice'):
            res_file.write('[ client 127.0.0.1'  + ' ]')
        else:
            res_file.write('[ client ' + str(address[0]) + ' ]')
        
        res_file.write(' ' + description + ': ')
        
        if(error == 'notice'):
            res_file.write('-' + '\n')
        else:
            res_file.write(uri + '\n')
        
        res_file.close()
        
    return 