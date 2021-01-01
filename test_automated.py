import create_sock
import pytest
import GET

#Simple GET Request
get_req_1 = 'GET /about HTTP/1.1\r\nHost: localhost\r\n\r\n'
get_res_1 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 1447", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#GET Request with incorrect Host header(status code 400)
get_req_2 = 'GET /about HTTP/1.1\r\nHost: local\r\n\r\n'
get_res_2 = ["HTTP/1.1 400 Bad Request", "Date: ", "Server: Aayush/0.1", "Connection: Closed"]

#404 Status Code
get_req_3 = 'GET /sample HTTP/1.1\r\nHost: localhost\r\n\r\n'
get_res_3 = ["HTTP/1.1 404 Not Found", "Date: ", "Content-Type: text/html", "Content-Length: 213", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#GET Request with correct Accept header(html file)
get_req_4 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nAccept: text/html\r\n\r\n'
get_req_4_2 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nAccept: text/*\r\n\r\n'
get_req_4_3 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nAccept: */*\r\n\r\n'
get_res_4 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 1447", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#GET Request with correct Accept header(image file)
get_req_5 = 'GET /images/weather.png HTTP/1.1\r\nHost: localhost\r\nAccept: image/*\r\n\r\n'
get_req_5_2 = 'GET /images/weather.png HTTP/1.1\r\nHost: localhost\r\nAccept: image/png\r\n\r\n'
get_req_5_3 = 'GET /images/weather.png HTTP/1.1\r\nHost: localhost\r\nAccept: */*\r\n\r\n'
get_res_5 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: image/png", "Content-Length: 1760", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#GET Request with proxy authorization header
get_req_6 = 'GET /proxy HTTP/1.1\r\nHost: localhost\r\nProxy-Authorization: Basic aayush:password\r\n\r\n'
get_res_6 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 238", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#If no proxy authorization is provided(407 status code)
get_req_7 = 'GET /proxy HTTP/1.1\r\nHost: localhost\r\n\r\n'
get_res_7 = ["HTTP/1.1 407 Proxy Authentication Required", "Proxy-Authenticate: Basic", "Date: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#accept-encoding header
get_req_8 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nAccept-Encoding: zlib\r\n\r\n'
get_res_8 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 638", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed", "Content-Coding: zlib"]

get_req_8_2 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nAccept-Encoding: gzip\r\n\r\n'
get_res_8_2 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 650", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed", "Content-Coding: gzip"]

#406 status code
get_req_9 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nAccept-Encoding: deflate\r\n\r\n'
get_res_9 = ["HTTP/1.1 406 Not Acceptable", "Date: ", "Server: Aayush/0.1", "Connection: Closed"]

#Range header
get_req_10 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nRange: bytes=10-150\r\n\r\n'
get_res_10 = ["HTTP/1.1 206 Partial Content", "Date: ", "Content-Type: text/html", "Content-Length: 1447", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed", "Content-Range: 10-150/1447"]

get_req_10_2 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nRange: bytes=10-\r\n\r\n'
get_res_10_2 = ["HTTP/1.1 206 Partial Content", "Date: ", "Content-Type: text/html", "Content-Length: 1447", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed", "Content-Range: 10-/1447"]

get_req_10_3 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nRange: bytes=-400\r\n\r\n'
get_res_10_3 = ["HTTP/1.1 206 Partial Content", "Date: ", "Content-Type: text/html", "Content-Length: 1447", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed", "Content-Range: -400/1447"]

#416 status code
get_req_11 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nRange: bytes=600-400\r\n\r\n'
get_res_11 = ["HTTP/1.1 416 Requested Range Not Satisfiable", "Date: ", "Server: Aayush/0.1", "Connection: Closed"]

#Cookie header
get_req_12 = 'GET /about HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
get_res_12 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 1447",
            "Server: Aayush/0.1", "Connection: Closed"]

#301 status code
get_req_13 = 'GET /example_2 HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
get_res_13 = ["HTTP/1.1 301 Moved Permanently", "Date: ", "Server: Aayush/0.1", "Connection: Closed",
                "Location: " + GET.permanent_redirect]

#302 status code
get_req_14 = 'GET /example HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
get_res_14 = ["HTTP/1.1 302 Found", "Date: ", "Server: Aayush/0.1", "Connection: Closed",
                "Location: " + GET.temp_redirect]

#405 status code
get_req_15 = 'GET /access_log.txt HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
get_res_15 = ["HTTP/1.1 405 Method Not Allowed", "Date: ", "Content-Type: text/plain", "Content-Length: 43",
            "Server: Aayush/0.1", "Connection: Closed"]

#if-modified-since header(304 status code)
get_req_16 = 'GET /text2.txt HTTP/1.1\r\nHost: localhost\r\nIf-Modified-Since: Wed, 11 Nov 2020 07:45:23\r\n\r\n'
get_res_16 = ["HTTP/1.1 304 Not Modified", "Date: ", "Server: Aayush/0.1", "Connection: Closed"]

get_req_17 = 'GET /text2.txt HTTP/1.1\r\nHost: localhost\r\nIf-Modified-Since: Wed, 11 Nov 2019 07:45:23\r\n\r\n'
get_res_17 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/plain", "Content-Length: 963", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#if-unmodified-since header(412 status code)
get_req_18 = 'GET /text2.txt HTTP/1.1\r\nHost: localhost\r\nIf-Unmodified-Since: Wed, 11 Nov 2019 07:45:23\r\n\r\n'
get_res_18 = ["HTTP/1.1 412 Precondition Failed", "Date: ", "Server: Aayush/0.1", "Connection: Closed"]

get_req_19 = 'GET /text2.txt HTTP/1.1\r\nHost: localhost\r\nIf-Unmodified-Since: Wed, 11 Nov 2020 08:00:00\r\n\r\n'
get_res_19 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/plain", "Content-Length: 963", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

#301 status code(HEAD)
head_req_1 = 'HEAD /example_2 HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
head_res_1 = ["HTTP/1.1 301 Moved Permanently", "Date: ", "Server: Aayush/0.1", "Connection: Closed",
                "Location: " + GET.permanent_redirect]

#302 status code(HEAD)
head_req_2 = 'HEAD /example HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
head_res_2 = ["HTTP/1.1 302 Found", "Date: ", "Server: Aayush/0.1", "Connection: Closed",
                "Location: " + GET.temp_redirect]

#405 status code(HEAD)
head_req_3 = 'HEAD /access_log.txt HTTP/1.1\r\nHost: localhost\r\nCookie: 4680\r\n\r\n'
head_res_3 = ["HTTP/1.1 405 Method Not Allowed", "Date: ", "Content-Type: text/plain", "Content-Length: 43",
            "Server: Aayush/0.1", "Connection: Closed"]

#POST
post_req_1 = 'POST /about HTTP/1.1\r\nHost: localhost\r\n\r\nLocation=Thane&Name=Aayush'
post_res_1 = ["HTTP/1.1 200 OK", "Date: ", "Set-Cookie: ", "Server: Aayush/0.1", "Connection: Closed"]

#POST (with incorrect host header)
post_req_2 = 'POST /about HTTP/1.1\r\nHost: google\r\n\r\nLocation=Thane&Name=Aayush'
post_res_2 = ["HTTP/1.1 400 Bad Request", "Date: ", "Server: Aayush/0.1", "Connection: Closed"]

#DELETE (html_file)
delete_req_1 = 'DELETE /create_html HTTP/1.1\r\nHost: localhost\r\n\r\n'
delete_res_1 = ["HTTP/1.1 200 OK", "Date: ", "Content-Type: text/html", "Content-Length: 159", "Set-Cookie: ",
            "Server: Aayush/0.1", "Connection: Closed"]

res_file = open('sample_resource/sample_html.html', 'r')
body = res_file.read()
res_file.close()

put_req_1 = 'PUT /create_html.html HTTP/1.1\r\nHost: localhost\r\nContent-Type: text/html\r\n\r\n' + body
put_res_1 = ["HTTP/1.1 201 Created", "Date: ", "Set-Cookie: ", "Server: Aayush/0.1", "Connection: Closed"]

#Handling file permissions(DELETE)
delete_req_2 = 'DELETE /access_log.txt HTTP/1.1\r\nHost: localhost\r\n\r\n'
delete_res_2 = ["HTTP/1.1 405 Method Not Allowed", "Date: ", "Content-Type: text/plain", "Content-Length: 43", "Set-Cookie: ", 
            "Server: Aayush/0.1", "Connection: Closed"]

#Handling file permissions(PUT)
put_req_2 = 'PUT /access_log.txt HTTP/1.1\r\nHost: localhost\r\nContent-Type: text/html\r\n\r\n' + body
put_res_2 = ["HTTP/1.1 405 Method Not Allowed", "Date: ", "Content-Type: text/plain", "Content-Length: 43", "Set-Cookie: ", 
            "Server: Aayush/0.1", "Connection: Closed"]


@pytest.mark.parametrize("test_input, test_output, test_body",
                        [
                            (get_req_1, get_res_1, ''),
                            (get_req_2, get_res_2, ''),
                            (get_req_3, get_res_3, ''),
                            (get_req_4, get_res_4, ''),
                            (get_req_4_2, get_res_4, ''),
                            (get_req_4_3, get_res_4, ''),
                            (get_req_5, get_res_5, ''),
                            (get_req_5_2, get_res_5, ''),
                            (get_req_5_3, get_res_5, ''),
                            (get_req_6, get_res_6, ''),
                            (get_req_7, get_res_7, ''),
                            (get_req_8, get_res_8, ''),
                            (get_req_8_2, get_res_8_2, ''),
                            (get_req_9, get_res_9, ''),
                            (get_req_10, get_res_10, ''),
                            (get_req_10_2, get_res_10_2, ''),
                            (get_req_10_3, get_res_10_3, ''),
                            (get_req_11, get_res_11, ''),
                            (get_req_12, get_res_12, ''),
                            (get_req_13, get_res_13, ''),
                            (get_req_14, get_res_14, ''),
                            (get_req_15, get_res_15, ''),
                            (get_req_16, get_res_16, ''),
                            (get_req_17, get_res_17, ''),
                            (get_req_18, get_res_18, ''),
                            (get_req_19, get_res_19, ''),
                            (head_req_1, head_res_1, ''),
                            (head_req_2, head_res_2, ''),
                            (head_req_3, head_res_3, ''),
                            (post_req_1, post_res_1, ''),
                            (post_req_2, post_res_2, ''),
                            (delete_req_1, delete_res_1, body),
                            (put_req_1, put_res_1, body),
                            (delete_req_2, delete_res_2, body),
                            (put_req_2, put_res_2, body)
                        ]
                        )

def test_req(test_input, test_output, test_body):

    res_header, res_body = create_sock.send_request(test_input)
    
    i = 0
    count = 0

    while (i < len(res_header)):
        if res_header[i].find('Date') >= 0 or res_header[i].find('Set-Cookie') >= 0:
            if (res_header[i].find(test_output[i]) >= 0):
                count += 1
        elif (res_header[i] == test_output[i]):
            count += 1
        i += 1

    if(test_body == ''):
        assert count == len(test_output) or count == 0
    else:
        assert (count == len(test_output) or count == 0) and (res_body.find(body) >= 0 or res_body.find(body) == -1)

# response, res_body = create_sock.send_request(delete_req_1)
# print(response)
# print(len(body))
# print(body)
# print(res_body)

# if(res_body.find(body) >= 0):
#     print('ok')