import pickle
from realestate.agents import AGENTS
import random
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

"""
Custom proxy provider.
"""
DEPTH = 2
PERCENTAGE = 7
PROXIES_PATH = "ProxySpider_items.p"

class CustomHttpProxyMiddleware(object):

    def process_request(self, request, spider):
        print('start %i' % len(spider.proxies))
        if request.meta.get('proxy',0)==0:
            currentProxy=random.choice(spider.proxies)
        else:
            currentProxy={'ip_port':request.meta['proxy'].replace('http://','')}
            if self.change_proxy(request):
                currentProxy = random.choice(spider.proxies)
        print(currentProxy)
        request.meta['proxy'] = "http://%s" % currentProxy['ip_port']

    def process_response(self, request, response, spider):
        if response.status==407:
            newRequest = self.replace_request_proxy(request, spider)
            return newRequest
        return response

    def process_exception(self, request, exception, spider):
        if 'proxy' in request.meta:
            return
        else:
            newRequest = self.replace_request_proxy(request, spider)
            return newRequest

    def change_proxy(self, request):
        if "depth" in request.meta and int(request.meta['depth']) <= DEPTH:
            return False
        i = random.randint(1, 10)
        return i <= PERCENTAGE-1

    def replace_request_proxy(self,request,spider):
        proxy = request.meta['proxy']
        try:
            spider.proxies = [i for i in spider.proxies if "http://%s" % i.get("ip_port") != proxy]
            print(len(spider.proxies))
        except KeyError:
            pass
        p = random.choice(spider.proxies)
        r = request.meta
        r['proxy'] = p
        r['retry_times'] = 0
        return request.replace(meta=r)

"""
change request header nealy every time
"""
class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent

class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self,request,response,spider):
        pass