#!/usr/bin/env python3
# main.py - OTP BOMBER ULTIMATE v16.0
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
import platform
import os
import json
from colorama import Fore, Style, init
from datetime import datetime

# ==================== OBFUSCATED IMPORTS ====================
from db_cloud import UserManager as AuthSystem
from spam_engine import run_single_round, run_infinite, show_apis

init(autoreset=True)

# ==================== SESSION HANDLER ====================
SESSION_FILE = ".session"

def save_session(username, device_id):
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump({"username": username, "device_id": device_id, "time": datetime.now().isoformat()}, f)
        return True
    except:
        return False

def load_session():
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except:
        return None

def clear_session():
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        return True
    except:
        return False

# ==================== UI ====================
class Colors:
    HEADER = Fore.MAGENTA + Style.BRIGHT
    BLUE = Fore.CYAN + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL
    DIM = Fore.WHITE + Style.DIM
    CYAN = Fore.CYAN
    GOLD = Fore.YELLOW + Style.BRIGHT

C = Colors()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
  print(f"\n{C.CYAN}╔══════════════════════════════════════════╗")
    print(f"{C.CYAN}║{C.WHITE}          🔥 OTP BOMBER V16.0 - CLOUD EDITION        {C.CYAN}║")
    print(f"{C.CYAN}║{C.DIM}          30+ API - SECURE AUTH - ADMIN HIDDEN         {C.CYAN}║")
    print(f"{C.CYAN}╚══════════════════════════════════════════╝{C.RESET}\n")

def get_input(prompt, color=C.CYAN):
    return input(f"{color}[?] {prompt}: {C.WHITE}")

def get_password(prompt):
    import getpass
    return getpass.getpass(f"{C.CYAN}[?] {prompt}: {C.WHITE}")

def print_boxed(text, color=C.CYAN, width=50):
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    if max_len > width - 4:
        width = max_len + 4
    print(f"{color}┌{'─' * (width - 2)}┐")
    for line in lines:
        padding = width - len(line) - 4
        print(f"{color}│ {line}{' ' * padding} │")
    print(f"{color}└{'─' * (width - 2)}┘{C.RESET}")

def loading(text, duration=1.5):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f'\r{C.YELLOW}{chars[i % len(chars)]} {text}{C.RESET}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 50 + '\r')

# ==================== AUTH ====================
def auth_menu():
    clear_screen()
    print_header()
    print()
    print(f"  {C.GREEN}[1]{C.RESET} Login")
    print(f"  {C.GREEN}[2]{C.RESET} Register")
    print(f"  {C.GREEN}[3]{C.RESET} Exit")
    print()
    choice = get_input("Pilih menu (1/2/3)")
    
    if choice == "1":
        return login()
    elif choice == "2":
        return register()
    elif choice == "3":
        print(f"\n{C.GREEN}Goodbye!{C.RESET}")
        sys.exit(0)
    else:
        print(f"{C.RED}Invalid choice!{C.RESET}")
        time.sleep(1)
        return auth_menu()

def login():
    clear_screen()
    print_header()
    print_boxed("🔐 LOGIN", C.CYAN)
    print()
    
    username = get_input("Username")
    password = get_password("Password")
    device_id = platform.node()
    
    loading("Connecting to cloud...", 1.5)
    
    success, message = AuthSystem.login(username, password, device_id)
    
    if success:
        save_session(username, device_id)
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        time.sleep(1)
        return username
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

def register():
    clear_screen()
    print_header()
    print_boxed("📝 REGISTER", C.GREEN)
    print()
    
    username = get_input("Username (min 3 chars)")
    if len(username) < 3:
        print(f"{C.RED}Username minimal 3 karakter!{C.RESET}")
        time.sleep(1)
        return register()
    
    password = get_password("Password (min 4 chars)")
    if len(password) < 4:
        print(f"{C.RED}Password minimal 4 karakter!{C.RESET}")
        time.sleep(1)
        return register()
    
    confirm = get_password("Confirm Password")
    if password != confirm:
        print(f"{C.RED}Password tidak cocok!{C.RESET}")
        time.sleep(1)
        return register()
    
    device_id = platform.node()
    
    loading("Registering to cloud...", 1.5)
    
    success, message = AuthSystem.register(username, password, device_id)
    
    if success:
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk login...{C.RESET}")
        return login()
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

# ==================== MAIN MENU ====================
def main_menu(username):
    user = AuthSystem.get_user(username)
    if not user:
        clear_session()
        print(f"{C.RED}❌ User data corrupted!{C.RESET}")
        time.sleep(2)
        return auth_menu()
    
    is_admin = user.get('is_admin', False)
    is_premium = user.get('is_premium', False)
    quota = user.get('quota', 5)
    
    while True:
        clear_screen()
        print_header()
        
        # User info
        status_text = 'ADMIN' if is_admin else 'PREMIUM' if is_premium else 'TRIAL'
        status_color = C.RED if is_admin else C.GOLD if is_premium else C.YELLOW
        print(f"{C.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{C.CYAN}│{C.WHITE}  👤 {username}{' ' * (30 - len(username))}{C.CYAN}│")
        print(f"{C.CYAN}│{C.DIM}  Status: {status_color}{status_text}{C.DIM}  |  {C.GREEN}Quota: {quota}{' ' * (26 - len(str(quota)))}{C.CYAN}│")
        print(f"{C.CYAN}└─────────────────────────────────────────────────────────────┘{C.RESET}")
        print()
        
        # Stats
        try:
            total = AuthSystem.get_total_users()
            premium = AuthSystem.get_premium_count()
            print(f"{C.CYAN}📊 Total Users  : {C.WHITE}{total}")
            print(f"{C.CYAN}👑 Premium Users: {C.GOLD}{premium}{C.RESET}")
        except:
            print(f"{C.CYAN}📊 Total Users  : {C.WHITE}0{C.RESET}")
        print()
        
        # Menu
        if is_admin:
            print(f"{C.RED}👑 ADMIN MODE - Full Access{C.RESET}")
            print()
            print(f"  {C.GREEN}[1]{C.RESET} 🔥 Single Round")
            print(f"  {C.GREEN}[2]{C.RESET} 🔁 Infinite Loop")
            print(f"  {C.GREEN}[3]{C.RESET} 📊 Check APIs")
            print(f"  {C.GREEN}[4]{C.RESET} 👑 Admin Panel")
            print(f"  {C.GREEN}[5]{C.RESET} 🚪 Logout")
            print()
            choice = get_input("Pilih menu (1-5)")
            
            if choice == "1":
                phone = get_input("Nomor target")
                threads = get_thread_count()
                try:
                    run_single_round(phone, threads)
                except Exception as e:
                    print(f"{C.RED}Error: {e}{C.RESET}")
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "2":
                phone = get_input("Nomor target")
                try:
                    run_infinite(phone)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print(f"{C.RED}Error: {e}{C.RESET}")
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "3":
                show_apis()
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "4":
                admin_panel()
            elif choice == "5":
                clear_session()
                print(f"{C.GREEN}Logout!{C.RESET}")
                time.sleep(1)
                return auth_menu()
            else:
                print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
                time.sleep(1)
        else:
            status_text = 'PREMIUM' if is_premium else 'TRIAL'
            status_color = C.GOLD if is_premium else C.YELLOW
            print(f"{status_color}🆓 {status_text} MODE{C.RESET}")
            print()
            print(f"  {C.GREEN}[1]{C.RESET} 🔥 Single Round")
            print(f"  {C.GREEN}[2]{C.RESET} 📊 Check APIs")
            print(f"  {C.GREEN}[3]{C.RESET} 🚪 Logout")
            if not is_premium:
                print(f"  {C.GREEN}[4]{C.RESET} 🛒 Beli Premium")
            print()
            choice = get_input("Pilih menu (1-4)" if not is_premium else "Pilih menu (1-3)")
            
            if choice == "1":
                if quota <= 0 and not is_premium:
                    print(f"{C.RED}❌ Kuota habis! Beli premium.{C.RESET}")
                    time.sleep(2)
                    continue
                phone = get_input("Nomor target")
                try:
                    run_single_round(phone, 1)
                except Exception as e:
                    print(f"{C.RED}Error: {e}{C.RESET}")
                if not is_premium:
                    try:
                        AuthSystem.update_user(username, quota=quota-1)
                        quota -= 1
                    except:
                        pass
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "2":
                show_apis()
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "3":
                clear_session()
                print(f"{C.GREEN}Logout!{C.RESET}")
                time.sleep(1)
                return auth_menu()
            elif choice == "4" and not is_premium:
                show_buy_guide()
            else:
                print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
                time.sleep(1)

# ==================== ADMIN PANEL ====================
def admin_panel():
    while True:
        clear_screen()
        print_header()
        print(f"{C.RED}👑 ADMIN PANEL{C.RESET}\n")
        print(f"  {C.GREEN}[1]{C.RESET} 📋 List Users")
        print(f"  {C.GREEN}[2]{C.RESET} 👑 Activate Premium")
        print(f"  {C.GREEN}[3]{C.RESET} 🗑️  Delete User")
        print(f"  {C.GREEN}[4]{C.RESET} 🔄 Refresh")
        print(f"  {C.GREEN}[5]{C.RESET} ↩️  Back")
        print()
        choice = get_input("Pilih menu (1-5)")
        
        if choice == "1":
            try:
                users = AuthSystem.load_users()
                print(f"\n{C.CYAN}📋 USERS:{C.RESET}")
                print(f"{C.DIM}{'─' * 50}{C.RESET}")
                for u, data in users.items():
                    if u in ['admin', 'root']:
                        continue
                    prem = f"{C.GREEN}✅{C.RESET}" if data.get('is_premium') else f"{C.RED}❌{C.RESET}"
                    status = data.get('status', 'trial').upper()
                    quota = data.get('quota', 0)
                    print(f"  {u:15} | {status:8} | Quota: {quota:3} | {prem}")
                print(f"{C.DIM}{'─' * 50}{C.RESET}")
            except Exception as e:
                print(f"{C.RED}Error loading users: {e}{C.RESET}")
            input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            
        elif choice == "2":
            username = get_input("Username untuk activate premium")
            try:
                if AuthSystem.activate_premium(username):
                    print(f"{C.GREEN}✅ {username} activated!{C.RESET}")
                else:
                    print(f"{C.RED}❌ Failed! User not found.{C.RESET}")
            except Exception as e:
                print(f"{C.RED}Error: {e}{C.RESET}")
            time.sleep(1)
            
        elif choice == "3":
            username = get_input("Username untuk dihapus")
            if username in ['admin', 'root']:
                print(f"{C.RED}❌ Cannot delete admin!{C.RESET}")
                time.sleep(1)
                continue
            try:
                success, msg = AuthSystem.delete_user(username)
                print(f"{C.GREEN if success else C.RED}{'✅' if success else '❌'} {msg}{C.RESET}")
            except Exception as e:
                print(f"{C.RED}Error: {e}{C.RESET}")
            time.sleep(1)
            
        elif choice == "4":
            print(f"{C.GREEN}✅ Refreshed!{C.RESET}")
            time.sleep(1)
            
        elif choice == "5":
            return
        
        else:
            print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
            time.sleep(1)

# ==================== UTILITY ====================
def get_thread_count():
    print(f"\n{C.CYAN}Pilih thread:{C.RESET}")
    print(f"  {C.GREEN}[1]{C.RESET} 1  {C.DIM}(slow){C.RESET}")
    print(f"  {C.GREEN}[2]{C.RESET} 5  {C.DIM}(recommended){C.RESET}")
    print(f"  {C.GREEN}[3]{C.RESET} 10 {C.DIM}(fast){C.RESET}")
    print(f"  {C.GREEN}[4]{C.RESET} 20 {C.DIM}(ganas){C.RESET}")
    choice = get_input("Pilih (1-4)")
    mapping = {'1':1, '2':5, '3':10, '4':20}
    return mapping.get(choice, 5)

def show_buy_guide():
    clear_screen()
    print_header()
    print_boxed("🛒 BELI PREMIUM", C.GOLD)
    print()
    print(f"  {C.WHITE}Harga    : {C.GREEN}Rp 25.000{C.RESET}")
    print(f"  {C.WHITE}Admin WA : {C.GREEN}{AuthSystem.ADMIN_WA}{C.RESET}")
    print(f"  {C.WHITE}Device ID: {C.CYAN}{platform.node()}{C.RESET}")
    print()
    print(f"{C.YELLOW}🔗 https://wa.me/{AuthSystem.ADMIN_WA}{C.RESET}")
    print()
    input(f"{C.YELLOW}Tekan Enter...{C.RESET}")

# ==================== MAIN ====================
def main():
    try:
        # Cek session
        session = load_session()
        if session:
            username = session.get('username')
            device_id = session.get('device_id')
            if username and device_id == platform.node():
                user = AuthSystem.get_user(username)
                if user:
                    main_menu(username)
                    return
        
        # Start auth
        auth_menu()
        
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Exit by user...{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
