import random
import GET

def generate_cookie(req):
    # res_file = open('./html/cookies.txt', 'r+')
    res_file = open(GET.stored_cookies, 'r+')
    contents = res_file.read()
    cookies = contents.split(',')

    flag = 1

    for line in req:
        header = line.split(':')
        if header[0] == 'Cookie':
            return False
    

    while True:
        cookie_id = random.randint(1000, 9999)

        for id in cookies:
            if str(cookie_id) == id:
                flag = 0
                break 
        
        if flag == 1:
            
            res_file.write(str(cookie_id) + ',')
            res_file.close()

            return cookie_id
        else:
            flag = 0