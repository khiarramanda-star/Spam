#!/usr/bin/env python3
# main.py - Main Menu + Auth + UI

import sys
import time
import platform
import os
from colorama import Fore, Style, init

# ==================== OBFUSCATED IMPORTS ====================
# Original: from firebase import AuthSystem
# Obfuscated: dari file "db_cloud.py" import "UserManager"
from db_cloud import UserManager as AuthSystem

# Original: from main_engine import run_single_round, run_infinite, show_apis
from spam_engine import run_single_round, run_infinite, show_apis

init(autoreset=True)

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

def print_banner():
    banner = f"""
{C.HEADER}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {C.GREEN}██████╗ ████████╗██████╗     ██████╗  ██████╗ ███╗   ███╗{C.HEADER}   ║
║   {C.GREEN}██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██╔═══██╗████╗ ████║{C.HEADER}   ║
║   {C.GREEN}██████╔╝   ██║   ██████╔╝    ██████╔╝██║   ██║██╔████╔██║{C.HEADER}   ║
║   {C.GREEN}██╔═══╝    ██║   ██╔══██╗    ██╔══██╗██║   ██║██║╚██╔╝██║{C.HEADER}   ║
║   {C.GREEN}██║        ██║   ██║  ██║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║{C.HEADER}   ║
║   {C.GREEN}╚═╝        ╚═╝   ╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝{C.HEADER}   ║
║                                                                   ║
║            {C.YELLOW}🔥 OTP BOMBER V14.0 - CLOUD SYSTEM {C.HEADER}            ║
║            {C.WHITE}🔥 30+ API - SECURE AUTH - ADMIN PANEL {C.HEADER}         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{C.RESET}
    """
    print(banner)

def get_input(prompt):
    return input(f"{C.CYAN}[?] {prompt}: {C.WHITE}")

def get_password(prompt):
    import getpass
    return getpass.getpass(f"{C.CYAN}[?] {prompt}: {C.WHITE}")

# ==================== AUTH ====================
def auth_menu():
    clear_screen()
    print_banner()
    print()
    print(f"  {C.GREEN}[1]{C.RESET} Login")
    print(f"  {C.GREEN}[2]{C.RESET} Register")
    print(f"  {C.GREEN}[3]{C.RESET} Register as Admin {C.RED}(with code){C.RESET}")
    print(f"  {C.GREEN}[4]{C.RESET} Exit")
    print()
    choice = get_input("Pilih menu (1/2/3/4)")
    
    if choice == "1":
        return login()
    elif choice == "2":
        return register()
    elif choice == "3":
        return register_admin()
    elif choice == "4":
        print(f"\n{C.GREEN}Goodbye!{C.RESET}")
        sys.exit(0)
    else:
        print(f"{C.RED}Invalid choice!{C.RESET}")
        time.sleep(1)
        return auth_menu()

def login():
    clear_screen()
    print_banner()
    print()
    username = get_input("Username")
    password = get_password("Password")
    device_id = platform.node()
    
    success, message = AuthSystem.login(username, password, device_id)
    if success:
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        time.sleep(1)
        return username
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

def register():
    clear_screen()
    print_banner()
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
    success, message = AuthSystem.register(username, password, device_id)
    
    if success:
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk login...{C.RESET}")
        return login()
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

def register_admin():
    clear_screen()
    print_banner()
    print()
    admin_code = get_input("Admin Code")
    if admin_code != AuthSystem.ADMIN_CODE:
        print(f"{C.RED}❌ Invalid admin code!{C.RESET}")
        time.sleep(2)
        return auth_menu()
    
    username = get_input("Admin Username (min 3 chars)")
    if len(username) < 3:
        print(f"{C.RED}Username minimal 3 karakter!{C.RESET}")
        time.sleep(1)
        return register_admin()
    
    password = get_password("Admin Password (min 4 chars)")
    if len(password) < 4:
        print(f"{C.RED}Password minimal 4 karakter!{C.RESET}")
        time.sleep(1)
        return register_admin()
    
    confirm = get_password("Confirm Password")
    if password != confirm:
        print(f"{C.RED}Password tidak cocok!{C.RESET}")
        time.sleep(1)
        return register_admin()
    
    device_id = platform.node()
    success, message = AuthSystem.register(username, password, device_id, admin_code)
    
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
        return auth_menu()
    
    is_admin = user.get('is_admin', False)
    is_premium = user.get('is_premium', False)
    quota = user.get('quota', 5)
    
    while True:
        clear_screen()
        print_banner()
        
        print(f"{C.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{C.CYAN}│{C.WHITE}  👤 {username}{' ' * (30 - len(username))}{C.CYAN}│")
        print(f"{C.CYAN}│{C.DIM}  Status: {C.GREEN}{'ADMIN' if is_admin else 'PREMIUM' if is_premium else 'TRIAL'}{C.DIM}  |  {C.GREEN}Quota: {quota}{' ' * (26 - len(str(quota)))}{C.CYAN}│")
        print(f"{C.CYAN}└─────────────────────────────────────────────────────────────┘{C.RESET}")
        print()
        
        print(f"{C.CYAN}📊 Total Users: {C.WHITE}{AuthSystem.get_total_users()}{C.RESET}")
        print(f"{C.CYAN}👑 Premium Users: {C.GOLD}{AuthSystem.get_premium_count()}{C.RESET}")
        print()
        
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
                run_single_round(phone, threads)
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "2":
                phone = get_input("Nomor target")
                run_infinite(phone)
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "3":
                show_apis()
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "4":
                admin_panel()
            elif choice == "5":
                print(f"{C.GREEN}Logout!{C.RESET}")
                time.sleep(1)
                return auth_menu()
        else:
            print(f"{C.YELLOW}🆓 {'PREMIUM' if is_premium else 'TRIAL'} MODE{C.RESET}")
            print()
            print(f"  {C.GREEN}[1]{C.RESET} 🔥 Single Round")
            print(f"  {C.GREEN}[2]{C.RESET} 📊 Check APIs")
            print(f"  {C.GREEN}[3]{C.RESET} 🚪 Logout")
            if not is_premium:
                print(f"  {C.GREEN}[4]{C.RESET} 🛒 Beli Premium")
            print()
            choice = get_input("Pilih menu (1-3)")
            
            if choice == "1":
                if quota <= 0 and not is_premium:
                    print(f"{C.RED}❌ Kuota habis! Beli premium.{C.RESET}")
                    time.sleep(2)
                    continue
                phone = get_input("Nomor target")
                run_single_round(phone, 1)
                if not is_premium:
                    AuthSystem.update_user(username, quota=quota-1)
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "2":
                show_apis()
                input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
            elif choice == "3":
                print(f"{C.GREEN}Logout!{C.RESET}")
                time.sleep(1)
                return auth_menu()
            elif choice == "4" and not is_premium:
                show_buy_guide()

# ==================== ADMIN PANEL ====================
def admin_panel():
    clear_screen()
    print_banner()
    print(f"{C.RED}👑 ADMIN PANEL{C.RESET}\n")
    print(f"  {C.GREEN}[1]{C.RESET} 📋 List Users")
    print(f"  {C.GREEN}[2]{C.RESET} 👑 Activate Premium")
    print(f"  {C.GREEN}[3]{C.RESET} 🗑️  Delete User")
    print(f"  {C.GREEN}[4]{C.RESET} 🔄 Refresh")
    print(f"  {C.GREEN}[5]{C.RESET} ↩️  Back")
    print()
    choice = get_input("Pilih menu (1-5)")
    
    if choice == "1":
        users = AuthSystem.load_users()
        print(f"\n{C.CYAN}📋 USERS:{C.RESET}")
        for u, data in users.items():
            prem = "✅" if data.get('is_premium') else "❌"
            print(f"  {u} | {data.get('status','trial')} | {data.get('quota',0)} | {prem}")
        input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")
        return admin_panel()
    elif choice == "2":
        username = get_input("Username untuk activate premium")
        if AuthSystem.activate_premium(username):
            print(f"{C.GREEN}✅ {username} activated!{C.RESET}")
        else:
            print(f"{C.RED}❌ Failed!{C.RESET}")
        time.sleep(1)
        return admin_panel()
    elif choice == "3":
        username = get_input("Username untuk dihapus")
        success, msg = AuthSystem.delete_user(username)
        print(f"{C.GREEN if success else C.RED}{'✅' if success else '❌'} {msg}{C.RESET}")
        time.sleep(1)
        return admin_panel()
    elif choice == "4":
        print(f"{C.GREEN}✅ Refreshed!{C.RESET}")
        time.sleep(1)
        return admin_panel()
    else:
        return

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
    print_banner()
    print(f"{C.GOLD}🛒 BELI PREMIUM{C.RESET}\n")
    print(f"  {C.WHITE}Harga: {C.GREEN}Rp 25.000{C.RESET}")
    print(f"  {C.WHITE}Admin WA: {C.GREEN}{AuthSystem.ADMIN_WA}{C.RESET}")
    print(f"  {C.WHITE}Device ID: {C.CYAN}{platform.node()}{C.RESET}")
    input(f"\n{C.YELLOW}Tekan Enter...{C.RESET}")

# ==================== MAIN ====================
def main():
    try:
        AuthSystem.load_users()
        main_menu("root")  # Hidden admin
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Exit...{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
