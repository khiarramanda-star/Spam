#!/usr/bin/env python3
# utils.py - Utility Functions

import re
import uuid
import random
import string
import urllib.parse
import requests

from useragents import USER_AGENTS

def normalize(phone):
    n = phone.strip().replace(' ', '').replace('-', '').replace('+', '')
    if n.startswith('08'): return '62' + n[1:]
    if n.startswith('8'): return '62' + n
    if n.startswith('62'): return n
    return ''

def fmt_08(p):
    return '0' + p[2:] if p.startswith('62') else p

def fmt_nocode(p):
    return p[2:]

def fmt_plus(p):
    return '+' + p

def fmt_phone_only(p):
    return p[2:]

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return '127.0.0.1'

def extract_csrf(html):
    patterns = [
        r'<meta name="csrf-token" content="([^"]+)"',
        r'<meta name="csrf_token" content="([^"]+)"',
        r'<input type="hidden" name="_token" value="([^"]+)"',
        r'csrf_token\s*=\s*"([^"]+)"',
    ]
    for p in patterns:
        m = re.search(p, html, re.I)
        if m:
            return m.group(1)
    return None

def generate_multipart(data, boundary):
    body = ""
    for key, val in data.items():
        body += f"--{boundary}\r\n"
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
        body += f"{val}\r\n"
    body += f"--{boundary}--\r\n"
    return body

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_headers_with_random_ua(custom_headers=None):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
    }
    if custom_headers:
        headers.update(custom_headers)
    return headers
