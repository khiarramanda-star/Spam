#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp (FULL VERSION)
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
import platform
import os
from datetime import datetime
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

# ================================================================
# IMPORT DARI LICENSE
# ================================================================

from license import (
    clear_screen, log_info, log_success, log_warning, log_error, log_input,
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, 
    get_active_apis, is_maintenance, get_maintenance_message, 
    get_trial_quota, get_total_users, get_user_stats,
    VERSION, TOOLS_NAME, BANNER
)

# ================================================================
# FUNGSI BANTUAN
# ================================================================

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

def show_user_stats():
    premium, trial = get_user_stats()
    total = premium + trial
    print(f"{Fore.CYAN}Total Pengguna  : {Fore.WHITE}{total}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}├─ Premium      : {Fore.GREEN}{premium}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└─ Trial        : {Fore.YELLOW}{trial}{Style.RESET_ALL}")

def show_buy_guide():
    clear_screen()
    log_header()
    license_price = get_license_price()
    whatsapp_admin = get_whatsapp_admin()
    telegram_username = get_telegram_username()
    total_apis = get_active_apis()
    
    print(f"{Fore.CYAN}PANDUAN PEMBELIAN LISENSI PREMIUM{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Keuntungan Premium:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Akses FULL semua API ({total_apis} API)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Unlimited penggunaan (tanpa batas kuota)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Mendapat update tools terbaru")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Mendapat API baru jika ditambahkan")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Dukungan prioritas dari admin")
    print()
    print(f"{Fore.CYAN}Harga: {Fore.GREEN}Rp. {license_price:,}{Style.RESET_ALL} (sekali bayar, akses selamanya)")
    print()
    print(f"{Fore.YELLOW}Cara Pembelian:{Style.RESET_ALL}")
    print(f"  1. Chat admin via WhatsApp atau Telegram")
    print(f"  2. Kirim Device ID Anda")
    print(f"  3. Lakukan pembayaran via QRIS (akan diberikan admin)")
    print(f"  4. Tunggu aktivasi")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  WhatsApp : {Fore.GREEN}{whatsapp_admin}{Style.RESET_ALL}")
    print(f"  Telegram : {Fore.WHITE}{telegram_username}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID Anda:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{get_device_id()}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali ke menu utama...")

# ================================================================
# MENU UTAMA
# ================================================================

def show_menu(status, quota, device_id):
    clear_screen()
    print("="*60)
    print(f"{Fore.CYAN}🔥 SPAM OTP ENGINE {Fore.WHITE}v{VERSION}{Style.RESET_ALL}")
    print("="*60)
    print(f"{Fore.CYAN}[*] Status : {Fore.GREEN}{status.upper()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Quota  : {Fore.WHITE}{quota}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Device : {Fore.WHITE}{device_id[:16]}...{Style.RESET_ALL}")
    print("="*60)
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Single Round (1x spam)")
    print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Infinite Loop (terus menerus)")
    print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Custom Thread")
    print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Beli Premium")
    print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Keluar")
    print("="*60)
    print()

def show_thread_menu():
    clear_screen()
    log_header()
    print(f"{Fore.CYAN}Pilih Jumlah Thread (default 1){Style.RESET_ALL}")
    print()
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} 1 Thread (slow)")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} 2 Thread")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} 3 Thread")
    print(f"  {Fore.GREEN}[4]{Style.RESET_ALL} 4 Thread")
    print(f"  {Fore.GREEN}[5]{Style.RESET_ALL} 5 Thread (recommended)")
    print(f"  {Fore.GREEN}[6]{Style.RESET_ALL} 6 Thread")
    print(f"  {Fore.GREEN}[7]{Style.RESET_ALL} 7 Thread")
    print(f"  {Fore.GREEN}[8]{Style.RESET_ALL} 8 Thread")
    print(f"  {Fore.GREEN}[9]{Style.RESET_ALL} 9 Thread")
    print(f"  {Fore.GREEN}[10]{Style.RESET_ALL} 10 Thread (fast)")
    print()
    return log_input("Pilih thread (1-10, enter untuk default 1): ").strip()

# ================================================================
# MAIN
# ================================================================

def main():
    # Check license
    status, quota, device_id = check_license()
    
    if status not in ["premium", "trial"]:
        log_error("License tidak valid!")
        sys.exit(1)
    
    while True:
        show_menu(status, quota, device_id)
        
        choice = log_input("Pilih menu (1/2/3/4/5): ").strip()
        
        # ========================================
        # MENU 1: SINGLE ROUND
        # ========================================
        if choice == "1":
            # Cek quota untuk trial
            if status == "trial" and quota <= 0:
                log_warning("⚠️ Kuota trial habis!")
                log_info("Silakan beli lisensi premium untuk melanjutkan.")
                print()
                input("Tekan Enter untuk melihat panduan pembelian...")
                show_buy_guide()
                # Refresh user
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            thread_choice = show_thread_menu()
            try:
                threads = int(thread_choice) if thread_choice.strip() else 1
                if threads < 1: threads = 1
                elif threads > 10: threads = 10
            except:
                threads = 1
            
            from main_engine import run_single_round
            run_single_round(threads=threads)
            
            # Kurangi quota kalo trial
            if status == "trial":
                if use_quota(device_id):
                    user = check_user(device_id)
                    if user:
                        quota = user.get("quota", 0)
                        log_info(f"Sisa kuota: {quota}")
                else:
                    log_error("Gagal mengurangi kuota!")
            
            log_info("Tekan Enter untuk kembali...")
            input()
        
        # ========================================
        # MENU 2: INFINITE LOOP
        # ========================================
        elif choice == "2":
            if status == "trial" and quota <= 0:
                log_warning("⚠️ Kuota trial habis!")
                log_info("Silakan beli lisensi premium untuk melanjutkan.")
                print()
                input("Tekan Enter untuk melihat panduan pembelian...")
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            from main_engine import run_infinite_loop
            run_infinite_loop()
            log_info("Tekan Enter untuk kembali...")
            input()
        
        # ========================================
        # MENU 3: CUSTOM THREAD
        # ========================================
        elif choice == "3":
            if status == "trial" and quota <= 0:
                log_warning("⚠️ Kuota trial habis!")
                log_info("Silakan beli lisensi premium untuk melanjutkan.")
                print()
                input("Tekan Enter untuk melihat panduan pembelian...")
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            threads = log_input("Jumlah thread (default 5): ").strip()
            try:
                threads = int(threads) if threads else 5
                if threads < 1: threads = 1
            except:
                threads = 5
            
            from main_engine import run_single_round
            run_single_round(threads=threads)
            
            if status == "trial":
                if use_quota(device_id):
                    user = check_user(device_id)
                    if user:
                        quota = user.get("quota", 0)
                        log_info(f"Sisa kuota: {quota}")
                else:
                    log_error("Gagal mengurangi kuota!")
            
            log_info("Tekan Enter untuk kembali...")
            input()
        
        # ========================================
        # MENU 4: BELI PREMIUM
        # ========================================
        elif choice == "4":
            show_buy_guide()
            user = check_user(device_id)
            if user:
                quota = user.get("quota", 0)
        
        # ========================================
        # MENU 5: KELUAR
        # ========================================
        elif choice == "5":
            log_info("Keluar...")
            sys.exit(0)
        
        else:
            log_warning("Pilihan tidak valid. Tekan Enter...")
            input()

# ================================================================
# RUN
# ================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Dibatalkan.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
