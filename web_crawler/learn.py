import urllib.request
import urllib.parse
import urllib.error
import socket


def simple_request():
    response = urllib.request.urlopen('https://www.python.org')
    print(type(response))
    print(response.status)
    print(response.getheaders())
    print(response.getheader('Server'))


def request_carry_data():
    data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='UTF-8')
    try:
        response = urllib.request.urlopen('http://httpbin.org/post', data=data, timeout=10)
        print(response.read())
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print('Time Out')


def request_complex():
    url = 'http://httpbin.org/post'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host': 'httpbin.org'
    }
    params = {'name': 'Germey'}
    data = bytes(urllib.parse.urlencode(params), encoding='UTF-8')
    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    req.add_header('Accept-Encoding', 'UTF-8')
    res = urllib.request.urlopen(req)
    print(res.read().decode('UTF-8'))


request_complex()
