#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
import platform
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

from license import (
    clear_screen, log_info, log_success, log_warning, log_error, log_input,
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, 
    get_active_apis, get_trial_quota, VERSION
)

# ================================================================
# FUNGSI BANTUAN
# ================================================================

def get_formatted_datetime():
    now = datetime.now()
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{days[now.weekday()]}, {now.day} {months[now.month-1]} {now.year}"

def show_buy_guide():
    clear_screen()
    print()
    print(f"{Fore.YELLOW}PANDUAN PEMBELIAN PREMIUM{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Harga{Style.RESET_ALL} : {Fore.GREEN}Rp. {get_license_price():,}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Keuntungan Premium:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Akses FULL semua API ({get_active_apis()} API)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Unlimited penggunaan")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} {Fore.YELLOW}Spam Call{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} {Fore.YELLOW}Spam SMS{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} {Fore.YELLOW}Spam WhatsApp{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  WhatsApp : {Fore.GREEN}{get_whatsapp_admin()}{Style.RESET_ALL}")
    print(f"  Telegram : {Fore.WHITE}{get_telegram_username()}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{get_device_id()}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali...")

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
    print(f"{Fore.CYAN}OTP SPAM{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Single Round")
    print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Infinite Loop")
    print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Custom Thread")
    print()
    
    if status == "premium":
        print(f"{Fore.YELLOW}PREMIUM FEATURES{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} {Fore.YELLOW}Spam Call{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} {Fore.YELLOW}Spam SMS{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[6]{Style.RESET_ALL} {Fore.YELLOW}Spam WhatsApp{Style.RESET_ALL}")
        print()
    
    print(f"{Fore.CYAN}LAINNYA{Style.RESET_ALL}")
    if status != "premium":
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Beli Premium")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Keluar")
    else:
        print(f"{Fore.GREEN}[7]{Style.RESET_ALL} Beli Premium")
        print(f"{Fore.GREEN}[8]{Style.RESET_ALL} Keluar")
    print()

def show_thread_menu():
    clear_screen()
    print()
    print(f"{Fore.CYAN}PILIH THREAD{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} 1 Thread")
    print(f"{Fore.GREEN}[2]{Style.RESET_ALL} 2 Thread")
    print(f"{Fore.GREEN}[3]{Style.RESET_ALL} 3 Thread")
    print(f"{Fore.GREEN}[4]{Style.RESET_ALL} 4 Thread")
    print(f"{Fore.GREEN}[5]{Style.RESET_ALL} 5 Thread {Fore.WHITE}(recommended){Style.RESET_ALL}")
    print(f"{Fore.GREEN}[6]{Style.RESET_ALL} 6 Thread")
    print(f"{Fore.GREEN}[7]{Style.RESET_ALL} 7 Thread")
    print(f"{Fore.GREEN}[8]{Style.RESET_ALL} 8 Thread")
    print(f"{Fore.GREEN}[9]{Style.RESET_ALL} 9 Thread")
    print(f"{Fore.GREEN}[10]{Style.RESET_ALL} 10 Thread")
    print()
    return log_input("Pilih (1-10, Enter=5): ").strip() or "5"

# ================================================================
# SPAM CALL/SMS (PREMIUM)
# ================================================================

def spam_call_number(phone):
    try:
        from handlers import send_spam_call_free
        print(f"[*] Spam Call ke {phone}...")
        resp = send_spam_call_free(phone)
        if resp and resp.status_code == 200:
            log_success("Call sent!")
        else:
            log_error(f"Call failed")
    except Exception as e:
        log_error(f"Error: {e}")

def spam_sms_number(phone):
    try:
        from handlers import send_spam_sms_free, send_spam_sms_callmebot_free
        print(f"[*] Spam SMS ke {phone}...")
        resp = send_spam_sms_free(phone)
        if resp and resp.status_code == 200:
            log_success("SMS sent via TextBelt")
        else:
            log_warning("TextBelt failed")
        resp2 = send_spam_sms_callmebot_free(phone)
        if resp2 and resp2.status_code == 200:
            log_success("SMS sent via CallMeBot")
        else:
            log_warning("CallMeBot failed")
    except Exception as e:
        log_error(f"Error: {e}")

def spam_whatsapp_number(phone):
    try:
        from handlers import send_spam_whatsapp_free
        print(f"[*] Spam WhatsApp ke {phone}...")
        resp = send_spam_whatsapp_free(phone)
        if resp and resp.status_code == 200:
            log_success("WhatsApp link opened!")
        else:
            log_error("WhatsApp failed")
    except Exception as e:
        log_error(f"Error: {e}")

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
        
        elif choice == "4" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_call_number(phone)
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "5" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_sms_number(phone)
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "6" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_whatsapp_number(phone)
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "4" and status != "premium":
            show_buy_guide()
            user = check_user(device_id)
            if user:
                quota = user.get("quota", 0)
        
        elif choice == "7" and status == "premium":
            show_buy_guide()
        
        elif (choice == "5" and status != "premium") or (choice == "8" and status == "premium"):
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
