#!/usr/bin/env python3
# main_engine.py - OTP Spammer Engine (FULL 100+ API)

import sys
import time
import random
import threading
import signal
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

from license import log_info, log_success, log_warning, log_error, log_input, is_admin_number
from utils import normalize, get_random_user_agent
from handlers import get_all_handlers  # <--- PAKE INI

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

def run_handler(handler_name, handler_func, phone, idx, total):
    global stop_flag
    if stop_flag:
        return False
    
    name = handler_name
    status_text = "FAIL"
    detail = ""
    success = False

    try:
        resp = handler_func(phone)
        
        if resp is not None:
            if isinstance(resp, tuple):
                if len(resp) >= 2:
                    code, text = resp[0], resp[1]
                    if code and code < 400:
                        status_text = "SUCCESS"
                        detail = "OTP sent"
                        success = True
                    elif code == 429:
                        status_text = "LIMITED"
                        detail = "Rate limit"
                    else:
                        detail = f"({code}) {str(text)[:60] if text else ''}"
                else:
                    status_text = "SUCCESS" if resp[0] else "FAIL"
                    success = True if resp[0] else False
            elif hasattr(resp, 'status_code'):
                if resp.status_code < 400:
                    status_text = "SUCCESS"
                    detail = "OTP sent"
                    success = True
                elif resp.status_code == 429:
                    status_text = "LIMITED"
                    detail = "Rate limit"
                elif resp.status_code == 403:
                    status_text = "BLOCKED"
                    detail = "Forbidden"
                else:
                    detail = f"({resp.status_code})"
            elif isinstance(resp, bool):
                status_text = "SUCCESS" if resp else "FAIL"
                success = resp
            else:
                status_text = "SUCCESS" if resp else "FAIL"
                success = True if resp else False
        else:
            status_text = "ERROR"
            detail = "No response"
    except TypeError:
        try:
            resp = handler_func()
            if resp:
                status_text = "SUCCESS"
                detail = "OTP sent"
                success = True
            else:
                status_text = "FAIL"
                detail = "Failed"
        except Exception as e:
            status_text = "ERROR"
            detail = str(e)[:40]
    except Exception as e:
        status_text = "ERROR"
        detail = str(e)[:40]

    log_target(idx, total, name, status_text, detail)
    return success

def run_single_round(phone, threads=1):
    global stop_flag
    stop_flag = False
    
    handlers = get_all_handlers()  # <--- PAKE INI
    total = len(handlers)
    
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total}{Fore.CYAN} API{Style.RESET_ALL}")
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
    
    handlers = get_all_handlers()  # <--- PAKE INI
    total = len(handlers)
    
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total}{Fore.CYAN} API{Style.RESET_ALL}")
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
            
            with ThreadPoolExecutor(max_workers=5) as executor:
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
        log_warning("Proses dihentikan user!")
        log_info(f"Total success: {total_success} | fail: {total_fail}")

def run_custom_thread(phone, threads=5):
    global stop_flag
    stop_flag = False
    
    handlers = get_all_handlers()  # <--- PAKE INI
    total = len(handlers)
    
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total}{Fore.CYAN} API{Style.RESET_ALL}")
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
