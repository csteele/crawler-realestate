from realestate.proxy import PROXIES
from realestate.agents import AGENTS
from scrapy import log
import random

"""
Custom proxy provider.
"""
DEPTH = 1
PERCENTAGE = 3

class CustomHttpProxyMiddleware(object):
    def __init__(self):
        self.proxies=PROXIES
        self.currentProxy= self.proxies[0]

    def process_request(self, request, spider):
        if self.change_proxy(request):
            self.currentProxy = random.choice(self.proxies)
        try:
            request.meta['proxy'] = "http://%s" % self.currentProxy['ip_port']
        except Exception as e:
            log.msg("Exception %s" % e, _level=log.CRITICAL)


    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        else:
            proxy = request.meta['proxy']
            try:
                self.proxies = [i for i in self.proxies if i.get("ip_port") != proxy]
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


"""
change request header nealy every time
"""


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
