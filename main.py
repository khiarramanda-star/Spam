#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp (UI BARU)
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
import platform
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ================================================================
# IMPORT DARI LICENSE
# ================================================================

from license import (
    clear_screen, log_info, log_success, log_warning, log_error, log_input,
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, 
    get_active_apis, get_trial_quota, get_total_users, get_user_stats,
    VERSION, BANNER
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

def get_device_name():
    try:
        return platform.node()
    except:
        return "Unknown Device"

def show_buy_guide():
    clear_screen()
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Spammer OTP WhatsApp v.{VERSION}{Style.RESET_ALL}")
    print()
    print("="*60)
    print(f"{Fore.YELLOW}💎 PANDUAN PEMBELIAN LISENSI PREMIUM{Style.RESET_ALL}")
    print("="*60)
    print()
    print(f"{Fore.WHITE}Keuntungan Premium:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Akses FULL semua API ({get_active_apis()} API)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Unlimited penggunaan (tanpa batas)")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Update tools terbaru")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Dukungan prioritas")
    print()
    print(f"{Fore.CYAN}Harga: {Fore.GREEN}Rp. {get_license_price():,}{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Cara Pembelian:{Style.RESET_ALL}")
    print(f"  1. Chat admin via WhatsApp/Telegram")
    print(f"  2. Kirim Device ID Anda")
    print(f"  3. Lakukan pembayaran")
    print(f"  4. Tunggu aktivasi")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  WhatsApp : {Fore.GREEN}{get_whatsapp_admin()}{Style.RESET_ALL}")
    print(f"  Telegram : {Fore.WHITE}{get_telegram_username()}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID Anda:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{get_device_id()}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali...")

# ================================================================
# MENU UTAMA (UI BARU)
# ================================================================

def show_menu(status, quota, device_id):
    clear_screen()
    
    # HEADER
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Spammer OTP WhatsApp v.{VERSION}{Style.RESET_ALL}")
    print()
    
    # STATUS BAR
    print("="*60)
    print(f" {Fore.CYAN}📱 Status{Style.RESET_ALL} : {Fore.GREEN if status == 'premium' else Fore.YELLOW}{status.upper()}{Style.RESET_ALL}")
    print(f" {Fore.CYAN}📊 Quota {Style.RESET_ALL} : {Fore.WHITE}{quota}{Style.RESET_ALL}")
    print(f" {Fore.CYAN}🆔 Device{Style.RESET_ALL} : {Fore.WHITE}{device_id[:20]}...{Style.RESET_ALL}")
    print(f" {Fore.CYAN}📅 Date  {Style.RESET_ALL} : {Fore.WHITE}{get_formatted_datetime()}{Style.RESET_ALL}")
    print("="*60)
    print()
    
    # MENU
    print(f" {Fore.GREEN}[1]{Style.RESET_ALL}  Single Round  {Fore.WHITE}(1x spam){Style.RESET_ALL}")
    print(f" {Fore.GREEN}[2]{Style.RESET_ALL}  Infinite Loop {Fore.WHITE}(terus menerus){Style.RESET_ALL}")
    print(f" {Fore.GREEN}[3]{Style.RESET_ALL}  Custom Thread {Fore.WHITE}(atur thread){Style.RESET_ALL}")
    print(f" {Fore.GREEN}[4]{Style.RESET_ALL}  💎 Beli Premium")
    print(f" {Fore.GREEN}[5]{Style.RESET_ALL}  🚪 Keluar")
    print()
    print("="*60)
    print()

def show_thread_menu():
    clear_screen()
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Spammer OTP WhatsApp v.{VERSION}{Style.RESET_ALL}")
    print()
    print("="*60)
    print(f"{Fore.YELLOW}⚙️  PILIH JUMLAH THREAD{Style.RESET_ALL}")
    print("="*60)
    print()
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL}  1 Thread  {Fore.WHITE}(slow){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL}  2 Thread")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL}  3 Thread")
    print(f"  {Fore.GREEN}[4]{Style.RESET_ALL}  4 Thread")
    print(f"  {Fore.GREEN}[5]{Style.RESET_ALL}  5 Thread  {Fore.WHITE}(recommended){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[6]{Style.RESET_ALL}  6 Thread")
    print(f"  {Fore.GREEN}[7]{Style.RESET_ALL}  7 Thread")
    print(f"  {Fore.GREEN}[8]{Style.RESET_ALL}  8 Thread")
    print(f"  {Fore.GREEN}[9]{Style.RESET_ALL}  9 Thread")
    print(f"  {Fore.GREEN}[10]{Style.RESET_ALL} 10 Thread {Fore.WHITE}(fast){Style.RESET_ALL}")
    print()
    print("="*60)
    print()
    return log_input("Pilih thread (1-10, Enter=1): ").strip() or "1"

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
        choice = log_input("Pilih menu (1/2/3/4/5): ").strip()
        
        # --- MENU 1: SINGLE ROUND ---
        if choice == "1":
            if status == "trial" and quota <= 0:
                log_warning("⚠️ Kuota trial habis!")
                input("Tekan Enter untuk lihat panduan pembelian...")
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
            
            input("Tekan Enter untuk kembali...")
        
        # --- MENU 2: INFINITE LOOP ---
        elif choice == "2":
            if status == "trial" and quota <= 0:
                log_warning("⚠️ Kuota trial habis!")
                input("Tekan Enter untuk lihat panduan pembelian...")
                show_buy_guide()
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                continue
            
            from main_engine import run_infinite_loop
            run_infinite_loop()
            input("Tekan Enter untuk kembali...")
        
        # --- MENU 3: CUSTOM THREAD ---
        elif choice == "3":
            if status == "trial" and quota <= 0:
                log_warning("⚠️ Kuota trial habis!")
                input("Tekan Enter untuk lihat panduan pembelian...")
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
            
            input("Tekan Enter untuk kembali...")
        
        # --- MENU 4: BELI PREMIUM ---
        elif choice == "4":
            show_buy_guide()
            user = check_user(device_id)
            if user:
                quota = user.get("quota", 0)
        
        # --- MENU 5: KELUAR ---
        elif choice == "5":
            print("\n" + "="*60)
            print(f"{Fore.GREEN}Terima kasih sudah menggunakan Spammer OTP WhatsApp!{Style.RESET_ALL}")
            print("="*60)
            sys.exit(0)
        
        else:
            log_warning("Pilihan tidak valid!")
            time.sleep(1)

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
