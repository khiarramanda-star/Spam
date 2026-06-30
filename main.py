#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp

import sys
import time
import platform
from datetime import datetime
from colorama import Fore, Style

from license import (
    clear_screen, log_info, log_success, log_warning, log_error, log_input, log_header,
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, get_active_apis,
    is_maintenance, get_maintenance_message, get_trial_quota, get_total_users,
    VERSION, TOOLS_NAME, BANNER, get_user_stats
)

def get_formatted_datetime():
    now = datetime.now()
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    day_name = days[now.weekday()]
    day = now.day
    month = months[now.month - 1]
    year = now.year
    return f"{day_name}, {day} {month} {year}"

def get_device_name():
    try:
        return platform.node()
    except:
        return "Unknown Device"

def show_menu():
    print(f"{Fore.CYAN}Menu Utama{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Single Round (1x spam)")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Infinite Loop (terus menerus)")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Custom Thread")
    print(f"  {Fore.GREEN}[4]{Style.RESET_ALL} Keluar")
    print()

def main():
    status, quota, device_id = check_license()
    
    # KALO LICENSE OK, LANJUT KE MENU
    if status in ["premium", "trial"]:
        while True:
            clear_screen()
            log_header()
            print(f"{Fore.CYAN}{get_formatted_datetime()} | {Fore.WHITE}{get_device_name()}{Style.RESET_ALL}")
            print()
            
            if status == "premium":
                print(f"{Fore.GREEN}🌟 PREMIUM ACTIVE - Full Unlimited Access{Style.RESET_ALL}")
            else:
                trial_quota = get_trial_quota()
                print(f"{Fore.YELLOW}📱 TRIAL MODE - Sisa kuota: {quota}/{trial_quota}{Style.RESET_ALL}")
            print()
            
            show_menu()
            
            choice = log_input("Pilih menu (1/2/3/4): ").strip()
            
            if choice == "1":
                from main_engine import run_single_round
                run_single_round(threads=5)
                log_info("Tekan Enter untuk kembali...")
                input()
            
            elif choice == "2":
                from main_engine import run_infinite_loop
                run_infinite_loop()
                log_info("Tekan Enter untuk kembali...")
                input()
            
            elif choice == "3":
                threads = log_input("Jumlah thread (default 5): ").strip()
                threads = int(threads) if threads else 5
                from main_engine import run_single_round
                run_single_round(threads=threads)
                log_info("Tekan Enter untuk kembali...")
                input()
            
            elif choice == "4":
                log_info("Keluar...")
                sys.exit(0)
            
            else:
                log_warning("Pilihan tidak valid. Tekan Enter...")
                input()
    else:
        log_error("License tidak valid!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Jalankan license check dulu
        status, quota, device_id = check_license()
        
        # KALO LICENSE OK, MASUK MENU
        if status in ["premium", "trial"]:
            from main_engine import run_single_round, run_infinite_loop
            from handlers import get_all_handlers
            
            print("\n" + "="*50)
            print("📱 SPAM OTP MENU")
            print("="*50)
            print(f"[*] Status: {status.upper()}")
            print(f"[*] Quota: {quota}")
            print(f"[*] Device ID: {device_id}")
            print("="*50)
            print("[1] Single Round (1x spam)")
            print("[2] Infinite Loop (terus menerus)")
            print("[3] Custom Thread")
            print("[4] Keluar")
            print("="*50)
            
            choice = input("\nPilih menu (1/2/3/4): ").strip()
            
            if choice == "1":
                run_single_round()
            elif choice == "2":
                run_infinite_loop()
            elif choice == "3":
                threads = input("Jumlah thread (default 5): ").strip()
                threads = int(threads) if threads else 5
                run_single_round(threads=threads)
            else:
                print("Keluar...")
                sys.exit(0)
        else:
            print("❌ License tidak valid!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[!] Dibatalkan.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
