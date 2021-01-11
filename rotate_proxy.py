import requests
from lxml.html import fromstring
from itertools import cycle
import traceback

def get_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(), "yes")]'):
            proxy = ':'.join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

url = "https://httpbin.org/ip"
proxies = get_proxies()
proxy_pool = cycle(proxies)

for i in range(1, 11):
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        response = requests.get(url, proxies={'http': proxy, 'https': proxy})
        print(response.json())
    except:
        print("Skipping. Connection error")
