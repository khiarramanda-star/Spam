#!/usr/bin/env python3
# main.py - Spammer OTP WhatsApp (FULL)
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
import platform
import os
import json
import re
import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

from utils import fmt_08, get_random_user_agent

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
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} {Fore.YELLOW}Spam WA Code{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} {Fore.YELLOW}Spam Panggilan WA{Style.RESET_ALL}")
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
        print(f"{Fore.GREEN}[6]{Style.RESET_ALL} {Fore.YELLOW}Spam WA Code{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[C]{Style.RESET_ALL} {Fore.YELLOW}📞 Spam Panggilan WA{Style.RESET_ALL}")
        print()
        print(f"{Fore.GREEN}[0]{Style.RESET_ALL} {Fore.RED}Spam All{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[I]{Style.RESET_ALL} {Fore.RED}♾️ Spam All Infinity{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[S]{Style.RESET_ALL} {Fore.RED}🔥 Spam All Direct{Style.RESET_ALL}")
        print()
        print(f"{Fore.GREEN}[K]{Style.RESET_ALL} {Fore.RED}💬 Spam Kode WA Infinity{Style.RESET_ALL}")
        print()
    
    print(f"{Fore.CYAN}TOOLS{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[9]{Style.RESET_ALL} {Fore.MAGENTA}Buat API Baru{Style.RESET_ALL}")
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
# SPAM FUNCTIONS
# ================================================================

def spam_call_number(phone):
    try:
        from handlers import spam_call_all
        success = spam_call_all(phone)
        log_success(f"Call: {success} method(s)")
    except Exception as e:
        log_error(f"Error: {e}")

def spam_sms_number(phone):
    try:
        from handlers import spam_sms_all
        success = spam_sms_all(phone)
        log_success(f"SMS: {success} method(s)")
    except Exception as e:
        log_error(f"Error: {e}")

def spam_wa_code_number(phone):
    try:
        from handlers import spam_wa_code_all
        success = spam_wa_code_all(phone)
        log_success(f"WA Code: {success} method(s)")
    except Exception as e:
        log_error(f"Error: {e}")

def spam_wa_call(phone):
    try:
        from handlers import spam_wa_call_all
        success = spam_wa_call_all(phone)
        log_success(f"WA Call: {success} method(s)")
    except Exception as e:
        log_error(f"Error: {e}")

def spam_all(phone):
    print()
    log_info(f"Menjalankan SPAM ALL ke {phone}...")
    print()
    
    log_info("1. OTP Spam...")
    try:
        from main_engine import run_single_round
        run_single_round(threads=5)
    except Exception as e:
        log_error(f"OTP error: {e}")
    
    print()
    
    log_info("2. Spam Call...")
    spam_call_number(phone)
    
    print()
    
    log_info("3. Spam SMS...")
    spam_sms_number(phone)
    
    print()
    
    log_info("4. Spam WA Code...")
    spam_wa_code_number(phone)
    
    print()
    
    log_info("5. Spam Panggilan WA...")
    spam_wa_call(phone)
    
    print()
    log_success("SPAM ALL SELESAI!")

def spam_all_infinity():
    clear_screen()
    print()
    print(f"{Fore.RED}SPAM ALL INFINITY{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Jalan terus sampai di-stop (Ctrl+C){Style.RESET_ALL}")
    print()
    
    phone = log_input("Nomor target (08xx): ").strip()
    if not phone:
        log_error("Nomor tidak boleh kosong!")
        return
    
    phone = fmt_08(phone)
    print()
    log_info(f"Target: {phone}")
    log_info("Memulai SPAM ALL INFINITY...")
    log_info("Tekan Ctrl+C untuk berhenti")
    print()
    
    round_num = 1
    try:
        while True:
            print()
            log_info(f"Round {round_num} dimulai...")
            spam_all(phone)
            log_info(f"Round {round_num} selesai. Menunggu 10 detik...")
            for _ in range(10):
                time.sleep(1)
            round_num += 1
    except KeyboardInterrupt:
        print()
        log_warning("SPAM ALL INFINITY dihentikan!")
        log_info(f"Total round: {round_num-1}")

def spam_all_direct():
    clear_screen()
    print()
    print(f"{Fore.RED}SPAM ALL DIRECT{Style.RESET_ALL}")
    print()
    
    phone = log_input("Nomor target (08xx): ").strip()
    if not phone:
        log_error("Nomor tidak boleh kosong!")
        return
    
    phone = fmt_08(phone)
    spam_all(phone)
    print()
    input("Tekan Enter untuk kembali...")

def spam_wa_code_infinity():
    clear_screen()
    print()
    print(f"{Fore.RED}SPAM KODE WA INFINITY{Style.RESET_ALL}")
    print()
    
    phone = log_input("Nomor target (08xx): ").strip()
    if not phone:
        log_error("Nomor tidak boleh kosong!")
        return
    
    phone = fmt_08(phone)
    print()
    log_info(f"Target: {phone}")
    log_info("Memulai SPAM KODE WA INFINITY...")
    log_info("Tekan Ctrl+C untuk berhenti")
    print()
    
    count = 0
    try:
        while True:
            count += 1
            log_info(f"Round {count}...")
            spam_wa_code_number(phone)
            time.sleep(3)
    except KeyboardInterrupt:
        print()
        log_warning("SPAM KODE WA dihentikan!")
        log_info(f"Total round: {count}")

# ================================================================
# BUAT API BARU (MANUAL)
# ================================================================

def buat_api_baru():
    clear_screen()
    print()
    print(f"{Fore.MAGENTA}BUAT API OTP BARU (MANUAL){Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Masukkan detail API baru:{Style.RESET_ALL}")
    print()
    
    nama = log_input("Nama API: ").strip()
    if not nama:
        log_error("Nama tidak boleh kosong!")
        return
    
    url = log_input("URL Endpoint: ").strip()
    if not url:
        log_error("URL tidak boleh kosong!")
        return
    
    print()
    print(f"{Fore.CYAN}Pilih Method:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} POST (JSON)")
    print(f"{Fore.GREEN}[2]{Style.RESET_ALL} POST (Form)")
    print(f"{Fore.GREEN}[3]{Style.RESET_ALL} GET")
    method_choice = log_input("Pilih (1/2/3): ").strip()
    
    if method_choice == "1":
        method = "POST"
        content_type = "application/json"
        post_type = "json"
    elif method_choice == "2":
        method = "POST"
        content_type = "application/x-www-form-urlencoded"
        post_type = "form"
    elif method_choice == "3":
        method = "GET"
        content_type = "application/json"
        post_type = "get"
    else:
        method = "POST"
        content_type = "application/json"
        post_type = "json"
    
    print()
    print(f"{Fore.CYAN}Payload:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Gunakan {Fore.YELLOW}{{phone}}{Fore.WHITE} untuk nomor telepon{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Gunakan {Fore.YELLOW}{{rand}}{Fore.WHITE} untuk random{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Gunakan {Fore.YELLOW}{{uuid}}{Fore.WHITE} untuk UUID{Style.RESET_ALL}")
    print()
    
    default_payload = '{"phone": "{phone}", "type": "whatsapp"}'
    payload = log_input(f"Payload (Enter untuk default): ").strip()
    if not payload:
        payload = default_payload
    
    print()
    header_input = log_input("Header tambahan (JSON, Enter skip): ").strip()
    if header_input:
        try:
            headers = json.loads(header_input)
        except:
            headers = {}
    else:
        headers = {}
    
    print()
    keywords_input = log_input("Keyword sukses (pisah koma): ").strip()
    if keywords_input:
        success_keywords = [k.strip().lower() for k in keywords_input.split(',') if k.strip()]
    else:
        success_keywords = ['success', 'otp', 'berhasil', 'sent']
    
    func_name = f"send_{nama.lower().replace(' ', '_')}_otp"
    
    if post_type == "json":
        code = f'''
def {func_name}(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "{url}"
        payload = {payload}
        payload = payload.replace('{{phone}}', phone_plus)
        payload = payload.replace('{{rand}}', str(random.randint(100000,999999)))
        payload = payload.replace('{{uuid}}', str(uuid.uuid4()))
        payload = payload.replace('{{email}}', f"user{{random.randint(1000,9999)}}@mailnesia.com")
        try:
            payload = json.loads(payload)
        except:
            pass
        headers = {headers}
        headers['Content-Type'] = '{content_type}'
        headers['User-Agent'] = get_random_user_agent()
        resp = requests.{method.lower()}("{url}", json=payload, headers=headers, timeout=10)
        return resp
    except:
        return None
'''
    elif post_type == "form":
        code = f'''
def {func_name}(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "{url}"
        payload = {payload}
        payload = payload.replace('{{phone}}', phone_plus)
        payload = payload.replace('{{rand}}', str(random.randint(100000,999999)))
        payload = payload.replace('{{uuid}}', str(uuid.uuid4()))
        payload = payload.replace('{{email}}', f"user{{random.randint(1000,9999)}}@mailnesia.com")
        headers = {headers}
        headers['Content-Type'] = '{content_type}'
        headers['User-Agent'] = get_random_user_agent()
        resp = requests.{method.lower()}("{url}", data=payload, headers=headers, timeout=10)
        return resp
    except:
        return None
'''
    else:
        code = f'''
def {func_name}(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "{url}"
        params = {payload}
        params = params.replace('{{phone}}', phone_plus)
        params = params.replace('{{rand}}', str(random.randint(100000,999999)))
        params = params.replace('{{uuid}}', str(uuid.uuid4()))
        params = params.replace('{{email}}', f"user{{random.randint(1000,9999)}}@mailnesia.com")
        try:
            params = json.loads(params)
        except:
            pass
        headers = {headers}
        headers['User-Agent'] = get_random_user_agent()
        resp = requests.{method.lower()}("{url}", params=params, headers=headers, timeout=10)
        return resp
    except:
        return None
'''
    
    print()
    print(f"{Fore.GREEN}[+] API Baru Berhasil Dibuat!{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Nama API  : {Fore.WHITE}{nama}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Function  : {Fore.WHITE}{func_name}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Keyword   : {Fore.WHITE}{', '.join(success_keywords)}{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Kode API:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{code}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Simpan kode ini ke {Fore.WHITE}handlers.py{Fore.CYAN} dan tambahkan ke ALL_HANDLERS{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Contoh tambahkan ke ALL_HANDLERS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}    '{nama.lower()}': {func_name},{Style.RESET_ALL}")
    print()
    
    simpan = log_input("Simpan otomatis ke handlers.py? (y/n): ").strip().lower()
    if simpan == 'y':
        try:
            with open('handlers.py', 'a', encoding='utf-8') as f:
                f.write(code)
                f.write(f"\n# ===== {nama} =====\n")
            log_success(f"API {nama} berhasil disimpan ke handlers.py")
            log_info("Jangan lupa tambahkan ke ALL_HANDLERS")
        except Exception as e:
            log_error(f"Gagal menyimpan: {e}")
    
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
        
        # ========================================
        # SPAM ALL
        # ========================================
        if choice == "0" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_all(phone)
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # SPAM ALL INFINITY
        # ========================================
        elif choice.upper() == "I" and status == "premium":
            spam_all_infinity()
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # SPAM ALL DIRECT
        # ========================================
        elif choice.upper() == "S" and status == "premium":
            spam_all_direct()
        
        # ========================================
        # SPAM KODE WA INFINITY
        # ========================================
        elif choice.upper() == "K" and status == "premium":
            spam_wa_code_infinity()
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # SPAM PANGGILAN WA
        # ========================================
        elif choice.upper() == "C" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_wa_call(phone)
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # MENU 1: SINGLE ROUND
        # ========================================
        elif choice == "1":
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
        
        # ========================================
        # MENU 2: INFINITE LOOP
        # ========================================
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
        
        # ========================================
        # MENU 3: CUSTOM THREAD
        # ========================================
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
                threads = 1000
            
            from main_engine import run_single_round
            run_single_round(threads=threads)
            
            if status == "trial" and use_quota(device_id):
                user = check_user(device_id)
                if user:
                    quota = user.get("quota", 0)
                    log_info(f"Sisa kuota: {quota}")
            
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # MENU 4: SPAM CALL (PREMIUM ONLY)
        # ========================================
        elif choice == "4" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_call_number(phone)
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # MENU 5: SPAM SMS (PREMIUM ONLY)
        # ========================================
        elif choice == "5" and status == "premium":
            phone = log_input("Nomor target (08xx): ").strip()
            if phone:
                phone = fmt_08(phone)
                spam_sms_number(phone)
            input("\nTekan Enter untuk kembali...")
        
        # ========================================
        # MENU 9: BUAT API BARU
        # ========================================
        elif choice == "9":
            buat_api_baru()
        
        # ========================================
        # MENU BELI PREMIUM (TRIAL USER)
        # ========================================
        elif choice == "4" and status != "premium":
            show_buy_guide()
            user = check_user(device_id)
            if user:
                quota = user.get("quota", 0)
        
        # ========================================
        # MENU BELI PREMIUM (PREMIUM USER)
        # ========================================
        elif choice == "7" and status == "premium":
            show_buy_guide()
        
        # ========================================
        # MENU KELUAR
        # ========================================
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
