import urllib.request
import urllib.parse
import urllib.error
import socket
import http.cookiejar
import urllib.parse


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


def request_with_cookies():
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print('{}={}'.format(item.name, item.value))


def request_with_cookies_save():
    filename = 'cookies.txt'
    cookie = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    cookie.save(ignore_discard=True, ignore_expires=True)


def request_with_cookies_load():
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('UTF-8'))


def request_urlparse():
    result = urllib.parse.urlparse('http://www.baidu.com/index.html;user?id=5#comment')
    print(type(result), result)
    data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
    print(urllib.parse.urlunparse(data))
    result = urllib.parse.urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
    print(type(result), result)
    data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
    print(urllib.parse.urlunsplit(data))


def request_urlparse_other():
    print(urllib.parse.urljoin('http://www.baidu.com', 'FAQ.html'))
    print(urllib.parse.urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
    print(urllib.parse.urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
    print(urllib.parse.urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
    print(urllib.parse.urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
    print(urllib.parse.urljoin('http://www.baidu.com', '?category=2#comment'))
    print(urllib.parse.urljoin('www.baidu.com', '?category=2#comment'))
    print(urllib.parse.urljoin('www.baidu.com#comment', '?category=2'))
    params = {
        'name': 'germey',
        'age': 22
    }
    base_url = 'http://www.baidu.com?'
    url = base_url + urllib.parse.urlencode(params)
    print(url)
    query = 'name=germey&age=22'
    print(urllib.parse.parse_qs(query))  # {'name': ['germey'], 'age': ['22']}
    print(urllib.parse.parse_qsl(query))  # [('name', 'germey'), ('age', '22')]
    keyword = '壁纸'
    url = 'https://www.baidu.com/s?wd=' + urllib.parse.quote(keyword)
    print(url)
    url = 'https://www.baidu.com/s?wd=%E5%A3%81%E7%BA%B8'
    print(urllib.parse.unquote(url))


request_urlparse_other()
