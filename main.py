#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

from license import (
    clear_screen, log_info, log_success, log_warning, log_error, log_input,
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, 
    get_active_apis, get_trial_quota, VERSION
)

# ================================================================
# MENU UTAMA
# ================================================================

def show_menu(status, quota, device_id):
    clear_screen()
    print()
    print(f"SPAM OTP ENGINE v{VERSION}")
    print()
    print(f"Status : {status.upper()}")
    print(f"Quota  : {quota}")
    print(f"Device : {device_id[:16]}...")
    print()
    print("[1] Single Round")
    print("[2] Infinite Loop")
    print("[3] Custom Thread")
    print("[4] Beli Premium")
    print("[5] Keluar")
    print()

def show_thread_menu():
    clear_screen()
    print()
    print("PILIH THREAD")
    print()
    print("[1] 1 Thread  (slow)")
    print("[2] 2 Thread")
    print("[3] 3 Thread")
    print("[4] 4 Thread")
    print("[5] 5 Thread  (recommended)")
    print("[6] 6 Thread")
    print("[7] 7 Thread")
    print("[8] 8 Thread")
    print("[9] 9 Thread")
    print("[10] 10 Thread (fast)")
    print()
    return log_input("Pilih (1-10, Enter=5): ").strip() or "5"

def show_buy_guide():
    clear_screen()
    print()
    print("PANDUAN PEMBELIAN PREMIUM")
    print()
    print(f"Harga : Rp. {get_license_price():,}")
    print()
    print("Kontak Admin:")
    print(f"  WhatsApp : {get_whatsapp_admin()}")
    print(f"  Telegram : {get_telegram_username()}")
    print()
    print(f"Device ID: {get_device_id()}")
    print()
    input("Tekan Enter untuk kembali...")

# ================================================================
# MAIN
# ================================================================

def main():
    status, quota, device_id = check_license()
    
    if status not in ["premium", "trial"]:
        log_error("License tidak valid!")
        sys.exit(1)
    
    while True:
        show_menu(status, quota, device_id)
        choice = log_input("Pilih menu: ").strip()
        
        if choice == "1":
            if status == "trial" and quota <= 0:
                log_warning("Kuota trial habis!")
                input("Tekan Enter...")
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            threads = int(show_thread_menu())
            from main_engine import run_single_round
            run_single_round(threads=threads)
            
            if status == "trial" and use_quota(device_id):
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                    log_info(f"Sisa kuota: {quota}")
            
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "2":
            if status == "trial" and quota <= 0:
                log_warning("Kuota trial habis!")
                input("Tekan Enter...")
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            from main_engine import run_infinite_loop
            run_infinite_loop()
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "3":
            if status == "trial" and quota <= 0:
                log_warning("Kuota trial habis!")
                input("Tekan Enter...")
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            try:
                threads = int(log_input("Jumlah thread (default 5): ").strip() or "5")
                if threads < 1: threads = 1
            except:
                threads = 5
            
            from main_engine import run_single_round
            run_single_round(threads=threads)
            
            if status == "trial" and use_quota(device_id):
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                    log_info(f"Sisa kuota: {quota}")
            
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "4":
            show_buy_guide()
            user = check_user(device_id)
            if user:
                quota = user.get("quota", 0)
        
        elif choice == "5":
            print("\nTerima kasih!")
            sys.exit(0)
        
        else:
            log_warning("Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDibatalkan.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
