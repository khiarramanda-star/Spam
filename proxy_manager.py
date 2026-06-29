#!/usr/bin/env python3
# proxy_manager.py - Proxy dengan Fallback Direct

import requests
import random
import time
import re
import os
from urllib.parse import urlparse

# ==================== PROXY SOURCES ====================
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
]
# ==================== PROXY MANAGER ====================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.failed_proxies = set()
        self.used_proxies = set()
        self.last_refresh = 0
        self.refresh_interval = 300
        self.current_index = 0
        self.lock = False
        self.use_proxy = True  # Bisa dimatiin kalo semua proxy gagal
    
    def load_proxies(self, force=False):
        if self.lock:
            return self.proxies
        
        self.lock = True
        try:
            if not force and time.time() - self.last_refresh < self.refresh_interval:
                self.lock = False
                return self.proxies
            
            all_proxies = []
            for url in PROXY_SOURCES:
                try:
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        for line in resp.text.splitlines():
                            line = line.strip()
                            if line and not line.startswith('#'):
                                if '://' in line:
                                    proxy = line
                                elif re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', line):
                                    proxy = f"http://{line}"
                                else:
                                    continue
                                if self._validate_proxy(proxy):
                                    all_proxies.append(proxy)
                    time.sleep(0.3)
                except:
                    continue
            
            all_proxies = list(dict.fromkeys(all_proxies))
            self.proxies = [p for p in all_proxies if p not in self.failed_proxies]
            
            if not self.proxies:
                self.proxies = DEFAULT_PROXIES.copy()
            
            if len(self.proxies) > 50:
                self.proxies = [p for p in self.proxies if p not in self.used_proxies]
            
            if not self.proxies:
                self.proxies = DEFAULT_PROXIES.copy()
                self.used_proxies.clear()
                self.failed_proxies.clear()
            
            self.last_refresh = time.time()
            self.use_proxy = True
            
        except:
            if not self.proxies:
                self.proxies = DEFAULT_PROXIES.copy()
        
        self.lock = False
        return self.proxies
    
    def _validate_proxy(self, proxy):
        try:
            parsed = urlparse(proxy)
            if parsed.scheme in ['http', 'https', 'socks4', 'socks5'] and parsed.netloc:
                return True
            return False
        except:
            return False
    
    def get_proxy(self):
        """Get next proxy, return None if should use direct"""
        if not self.use_proxy:
            return None
        
        if not self.proxies:
            self.load_proxies()
        
        if not self.proxies:
            return None
        
        for _ in range(min(10, len(self.proxies))):
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            if proxy not in self.failed_proxies and proxy not in self.used_proxies:
                self.used_proxies.add(proxy)
                return proxy
        
        self.used_proxies.clear()
        if self.proxies:
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            return proxy
        
        return None
    
    def mark_failed(self, proxy):
        if proxy:
            self.failed_proxies.add(proxy)
            if proxy in self.proxies:
                self.proxies.remove(proxy)
            # Jika semua proxy gagal, matikan proxy
            if len(self.proxies) == 0 and len(self.failed_proxies) > 10:
                self.use_proxy = False
                print(f"{Fore.YELLOW}[!] Semua proxy gagal, beralih ke direct connection{Style.RESET_ALL}")
    
    def mark_success(self, proxy):
        if proxy and proxy in self.failed_proxies:
            self.failed_proxies.remove(proxy)
        self.use_proxy = True
    
    def get_proxy_dict(self, proxy_url):
        if not proxy_url:
            return None
        parsed = urlparse(proxy_url)
        scheme = parsed.scheme or 'http'
        return {
            'http': f"{scheme}://{parsed.netloc}",
            'https': f"{scheme}://{parsed.netloc}"
        }
    
    def get_stats(self):
        return {
            'total': len(self.proxies),
            'failed': len(self.failed_proxies),
            'used': len(self.used_proxies),
            'use_proxy': self.use_proxy,
            'last_refresh': self.last_refresh
        }

# ==================== SINGLETON ====================
_proxy_manager = None

def get_proxy_manager():
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def safe_request(method, url, **kwargs):
    pm = get_proxy_manager()
    timeout = kwargs.pop('timeout', 15)
    headers = kwargs.pop('headers', {})
    data = kwargs.pop('data', None)
    json_data = kwargs.pop('json', None)
    cookies = kwargs.pop('cookies', None)
    
    # Coba pake proxy
    for attempt in range(2):
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
                pm.mark_success(proxy)
                return resp
            else:
                pm.mark_failed(proxy)
        except:
            pm.mark_failed(proxy)
            continue
    
    # FALLBACK: Direct connection (tanpa proxy)
    try:
        req_kwargs = {
            'headers': headers,
            'timeout': timeout,
            'verify': False,
        }
        if cookies: req_kwargs['cookies'] = cookies
        if data is not None: req_kwargs['data'] = data
        elif json_data is not None: req_kwargs['json'] = json_data
        
        if method.upper() == 'GET':
            resp = requests.get(url, **req_kwargs)
        else:
            resp = requests.post(url, **req_kwargs)
        
        return resp
    except:
        return None
