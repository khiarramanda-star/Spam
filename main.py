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
    print(f"{Fore.CYAN}SPAM OTP ENGINE v{VERSION}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Status{Style.RESET_ALL} : {Fore.GREEN if status == 'premium' else Fore.YELLOW}{status.upper()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Quota{Style.RESET_ALL}  : {Fore.WHITE}{quota}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Device{Style.RESET_ALL} : {Fore.WHITE}{device_id[:16]}...{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Single Round")
    print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Infinite Loop")
    print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Custom Thread")
    print(f"{Fore.GREEN}[4]{Style.RESET_ALL} {Fore.YELLOW}Beli Premium{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Keluar")
    print()

def show_thread_menu():
    clear_screen()
    print()
    print(f"{Fore.CYAN}PILIH THREAD{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} 1 Thread  {Fore.WHITE}(slow){Style.RESET_ALL}")
    print(f"{Fore.GREEN}[2]{Style.RESET_ALL} 2 Thread")
    print(f"{Fore.GREEN}[3]{Style.RESET_ALL} 3 Thread")
    print(f"{Fore.GREEN}[4]{Style.RESET_ALL} 4 Thread")
    print(f"{Fore.GREEN}[5]{Style.RESET_ALL} 5 Thread  {Fore.WHITE}(recommended){Style.RESET_ALL}")
    print(f"{Fore.GREEN}[6]{Style.RESET_ALL} 6 Thread")
    print(f"{Fore.GREEN}[7]{Style.RESET_ALL} 7 Thread")
    print(f"{Fore.GREEN}[8]{Style.RESET_ALL} 8 Thread")
    print(f"{Fore.GREEN}[9]{Style.RESET_ALL} 9 Thread")
    print(f"{Fore.GREEN}[10]{Style.RESET_ALL} 10 Thread {Fore.WHITE}(fast){Style.RESET_ALL}")
    print()
    return log_input("Pilih (1-10, Enter=5): ").strip() or "5"

def show_buy_guide():
    clear_screen()
    print()
    print(f"{Fore.YELLOW}PANDUAN PEMBELIAN PREMIUM{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Harga{Style.RESET_ALL} : {Fore.GREEN}Rp. {get_license_price():,}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}WhatsApp{Style.RESET_ALL} : {Fore.GREEN}{get_whatsapp_admin()}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Telegram{Style.RESET_ALL} : {Fore.WHITE}{get_telegram_username()}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID{Style.RESET_ALL} : {Fore.WHITE}{get_device_id()}{Style.RESET_ALL}")
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
            print(f"\n{Fore.GREEN}Terima kasih!{Style.RESET_ALL}")
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
