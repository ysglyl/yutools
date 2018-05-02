import requests
import re


def requests_ops():
    r = requests.get('https://www.baidu.com/')
    # r = requests.post('http://httpbin.org/post')
    print(type(r))
    print(r.status_code)
    print(type(r.text))
    print(r.text)
    print(r.cookies)
    print(r.headers)
    print(r.url)
    print(r.history)

    data = {
        "name": "test",
        "age": 1
    }
    r = requests.get('http://httpbin.org/get', params=data)
    print(r.text)
    print(r.json())
    print(r.content)


def fetch_zhihu_explore():
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = requests.get('https://www.zhihu.com/explore', headers=headers)
    pattern = re.compile(
        'explore-feed feed-item.*?question_link.*?>(.+?)</a>.*?zm-item-vote-count.*?>(\w+)</a>',
        re.S)
    articles = re.findall(pattern, res.text)
    for article in articles:
        print(article)


def fetch_image():
    url = 'http://pics.sc.chinaz.com/files/pic/pic9/201804/wpic666.jpg'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    with open('image.jpg', 'wb') as f:
        f.write(res.content)


def post_file():
    try:
        files = {'file': open('image.jpg', 'rb')}
        r = requests.post('http://httpbin.org/post', files=files)
        print(r.text)
    except Exception as e:
        print(e)


def use_session():
    s = requests.session()
    r1 = s.get('http://www.baidu.com')
    print(r1.cookies)
    r2 = s.get('http://www.baidu.com')
    print(r2.cookies)


def verify_false():
    r = requests.get('https://www.12306.cn', verify=False)
    print(r.status_code)


def request_via_proxy():
    proxies = {
        'http': 'www-proxy.ericsson.se:8080'
    }
    r = requests.get('http://hk.youtube.com/', proxies=proxies)
    print(r.status_code)


request_via_proxy()
