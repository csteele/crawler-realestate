import pickle
from realestate.agents import AGENTS
import random

"""
Custom proxy provider.
"""
DEPTH = 1
PERCENTAGE = 3
PROXIES_PATH = "ProxySpider_items.p"

class CustomHttpProxyMiddleware(object):
    def __init__(self):
        self.proxies=self.get_proxies(PROXIES_PATH)
        self.currentProxy= self.proxies[0]

    def process_request(self, request, spider):
        print('start %i' % len(self.proxies))
        if request.meta.get('proxy',0)!= 0:
            self.currentProxy = request.meta.get('proxy')
        else:
            if self.change_proxy(request):
                self.currentProxy = random.choice(self.proxies)
        try:
            print(self.currentProxy)
            request.meta['proxy'] = "http://%s" % self.currentProxy['ip_port']
        except Exception as e:
            spider.logger.info("Exception {0}".format(e))

    def process_response(self, request, response, spider):
        if response.status!=200:
            r = request.meta
            proxy=r['proxy']
            try:
                self.proxies = [i for i in self.proxies if "http://%s" % i.get("ip_port") != proxy]
                print(len(self.proxies))
            except KeyError:
                pass
            p = random.choice(self.proxies)
            r['proxy'] = p
            r['retry_times'] = 0
            return request.replace(meta=r)
        return response

    def process_exception(self, request, exception, spider):
        if 'proxy' in request.meta:
            return
        else:
            proxy = request.meta['proxy']
            try:
                self.proxies = [i for i in self.proxies if "http://%s" % i.get("ip_port") != proxy]
                print(len(self.proxies))
            except KeyError:
                pass
            p = random.choice(self.proxies)
            r = request.meta
            r['proxy']=p
            r['retry_times']=0
            return request.replace(meta=r)

    def change_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if "depth" in request.meta and int(request.meta['depth']) <= DEPTH:
            return False
        i = random.randint(1, 10)
        return i <= PERCENTAGE-1

    def load_pickle(self,filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def get_proxies(self, proxies_path):
        items=self.load_pickle(proxies_path)
        try:
            proxies=[{"ip_port": "{0}:{1}".format(proxyItem['ip'],proxyItem['port'])} for proxyItem in items]
        except Exception as e:
            raise SystemExit(0)
        return proxies

"""
change request header nealy every time
"""
class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent


