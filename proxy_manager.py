#!/usr/bin/env python3
# proxy_manager.py - Proxy Rotation & Management

import requests
import random
import time
from urllib.parse import urlparse

PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
]

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.failed_proxies = set()
        self.last_refresh = 0
    
    def load_proxies(self, force=False):
        if force or time.time() - self.last_refresh > 300:
            all_proxies = []
            for url in PROXY_SOURCES:
                try:
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        for line in resp.text.splitlines():
                            line = line.strip()
                            if line and not line.startswith('#'):
                                if '://' not in line:
                                    all_proxies.append(f"http://{line}")
                                else:
                                    all_proxies.append(line)
                except:
                    pass
            
            if not all_proxies:
                all_proxies = [
                    "http://103.175.42.147:80", "http://103.175.42.157:80",
                    "http://103.175.42.155:80", "http://103.146.145.142:8080",
                    "http://103.158.188.12:8000", "http://103.158.188.13:8000",
                ]
            
            self.proxies = [p for p in all_proxies if p not in self.failed_proxies]
            if not self.proxies:
                self.failed_proxies.clear()
                self.proxies = all_proxies
            self.last_refresh = time.time()
        return self.proxies
    
    def get_proxy(self):
        self.load_proxies()
        if not self.proxies:
            return None
        for _ in range(min(5, len(self.proxies))):
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            if proxy not in self.failed_proxies:
                return proxy
        return None
    
    def mark_failed(self, proxy):
        if proxy and proxy in self.proxies:
            self.proxies.remove(proxy)
            self.failed_proxies.add(proxy)
    
    def get_proxy_dict(self, proxy):
        if not proxy:
            return None
        return {'http': proxy, 'https': proxy.replace('http://', 'https://')}

_proxy_manager = None

def get_proxy_manager():
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def safe_request(method, url, **kwargs):
    """Send request with proxy fallback"""
    pm = get_proxy_manager()
    timeout = kwargs.pop('timeout', 15)
    headers = kwargs.pop('headers', {})
    data = kwargs.pop('data', None)
    json_data = kwargs.pop('json', None)
    cookies = kwargs.pop('cookies', None)
    
    for attempt in range(3):
        proxy = pm.get_proxy()
        proxy_dict = pm.get_proxy_dict(proxy)
        
        try:
            req_kwargs = {
                'headers': headers,
                'timeout': timeout,
                'verify': False,
                'allow_redirects': True,
            }
            if cookies: req_kwargs['cookies'] = cookies
            if proxy_dict: req_kwargs['proxies'] = proxy_dict
            if data is not None: req_kwargs['data'] = data
            elif json_data is not None: req_kwargs['json'] = json_data
            
            if method.upper() == 'GET':
                resp = requests.get(url, **req_kwargs)
            elif method.upper() == 'POST':
                resp = requests.post(url, **req_kwargs)
            else:
                resp = requests.request(method, url, **req_kwargs)
            
            if resp.status_code < 500:
                return resp
            pm.mark_failed(proxy)
        except:
            pm.mark_failed(proxy)
            continue
    
    # Fallback tanpa proxy
    try:
        req_kwargs = {'headers': headers, 'timeout': timeout, 'verify': False}
        if cookies: req_kwargs['cookies'] = cookies
        if data is not None: req_kwargs['data'] = data
        elif json_data is not None: req_kwargs['json'] = json_data
        
        if method.upper() == 'GET':
            return requests.get(url, **req_kwargs)
        else:
            return requests.post(url, **req_kwargs)
    except:
        return None
